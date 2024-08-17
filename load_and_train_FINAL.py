# Loads the dataset using pandas, feeds it into the RNN and trains.
# Slow runtime due to 40k data files, approx. 11 mins for loading from M2 SATA and 1 min for training on 4070TI, 25 epochs.
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from concurrent.futures import ThreadPoolExecutor

import torch
from torch.utils.data import Dataset, DataLoader

import torch.nn as nn
import torch.optim as optim

from torch.utils.tensorboard import SummaryWriter


# Function to load and preprocess data from a single CSV file
def load_csv_file(file_path):
    try:
        data = pd.read_csv(file_path, header=None, sep=',', dtype=str)
        data = data.replace({',': ' '}, regex=True).astype(np.float32)
    except ValueError as e:
        print(f"Error processing file {file_path}: {e}")
        return None
    return data.values

# Function to create sequences from the data
def create_sequences(data, seq_length):
    sequences = []
    for i in range(len(data) - seq_length):
        seq = data[i:i + seq_length]
        sequences.append(seq)
    return np.array(sequences, dtype=np.float32)  # Ensure sequences are float32

# Function to process a single folder
def process_folder(movement_path, movement_folder, seq_length, max_files):
    sequences = []
    labels = []
    file_count = 0

    for file_name in os.listdir(movement_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(movement_path, file_name)

            # Load the CSV file
            data = load_csv_file(file_path)
            if data is None:
                continue  # Skip if there was an error in loading

            # Create sequences from the data
            seqs = create_sequences(data, seq_length)

            # Append sequences and labels
            sequences.extend(seqs)
            labels.extend([movement_folder] * len(seqs))

            # Increment file counter
            file_count += 1
            if file_count >= max_files:
                break  # Stop after loading the specified number of files

    return sequences, labels

# Dataset class
class CSIDataset(Dataset):
    def __init__(self, sequences, labels):
        self.sequences = np.array(sequences, dtype=np.float32)  # Ensure sequences are float32
        self.labels = np.array(labels, dtype=np.int64)  # Ensure labels are int64

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        sequence = torch.tensor(self.sequences[idx], dtype=torch.float32)
        label = torch.tensor(self.labels[idx], dtype=torch.long)
        return sequence, label

# Model class
class RWKVModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(RWKVModel, self).__init__()
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.rnn.num_layers, x.size(0), self.rnn.hidden_size).to(x.device)
        out, _ = self.rnn(x, h0)
        out = self.fc(out[:, -1, :])
        return out

# Training code wrapped in a main guard
if __name__ == "__main__":
    data_path = r'C:\Users\Grillex\Desktop\Widardata\Widardata\train'  # Update this path to your data location
    # Initialize TensorBoard writer
    log_dir = r'C:\Users\Grillex\PycharmProjects\Widar-DL-Project\logs'
    writer = SummaryWriter(log_dir=log_dir)

    # Parameters
    SEQ_LENGTH = 20
    MAX_FILES_PER_FOLDER = 2000  # Limit the number of files to load from each folder
    NUM_WORKERS = 8  # Number of threads for parallel processing

    all_sequences = []
    all_labels = []

    # Using ThreadPoolExecutor for parallel processing of folders
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = []
        for movement_folder in os.listdir(data_path):
            movement_path = os.path.join(data_path, movement_folder)
            if os.path.isdir(movement_path):
                futures.append(
                    executor.submit(process_folder, movement_path, movement_folder, SEQ_LENGTH, MAX_FILES_PER_FOLDER)
                )

        for future in futures:
            sequences, labels = future.result()
            all_sequences.extend(sequences)
            all_labels.extend(labels)

    # Convert to numpy arrays
    all_sequences = np.array(all_sequences)
    all_labels = np.array(all_labels)

    print("Data loaded and processed. Shape of sequences:", all_sequences.shape)
    print("Number of labels:", len(all_labels))

    # Encode Labels
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(all_labels)

    print("Labels encoded. Example mapping:", dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))))

    # Check if CUDA is available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')

    # Create dataset and dataloader
    dataset = CSIDataset(all_sequences, encoded_labels)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # Parameters
    input_size = all_sequences.shape[2]
    hidden_size = 64
    num_layers = 2
    output_size = len(np.unique(encoded_labels))

    # Initialize the model and move it to the GPU
    model = RWKVModel(input_size, hidden_size, num_layers, output_size).to(device)
    criterion = nn.CrossEntropyLoss().to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training loop
    num_epochs = 25

    for epoch in range(num_epochs):
        running_loss = 0.0
        for i, (inputs, targets) in enumerate(dataloader):
            # Move inputs and targets to the GPU
            inputs, targets = inputs.to(device), targets.to(device)

            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, targets)

            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            # Perform optimization step
            optimizer.step()

            # Accumulate loss
            running_loss += loss.item()

        # Calculate average loss for the epoch
        avg_loss = running_loss / len(dataloader)

        # Log loss to TensorBoard
        writer.add_scalar('Training Loss', avg_loss, epoch)
        print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {avg_loss}')

    # Save the model
    directory = r'C:\Users\Grillex\PycharmProjects\Widar-DL-Project'
    file_name = 'rnn_model_olddataset.pth'
    file_path = os.path.join(directory, file_name)

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Save the model's state dictionary
    torch.save(model.state_dict(), file_path)
    writer.close()

    print(f'Model saved to {file_path}')
