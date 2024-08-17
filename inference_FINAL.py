#Loads test data onto GPU and evaluates model accuracy
import torch
from torch.utils.data import DataLoader
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder

# Import your model class and any necessary data processing functions
from load_and_train import RWKVModel, CSIDataset, load_csv_file, create_sequences

# Parameters
SEQ_LENGTH = 20
BATCH_SIZE = 32
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Define your model architecture (use the same as during training)
input_size = 400  # Update this based on your actual input size
hidden_size = 64
num_layers = 2
output_size = 22  # Update this to match the number of classes

model = RWKVModel(input_size, hidden_size, num_layers, output_size).to(DEVICE)

# Load the saved model weights
model.load_state_dict(torch.load(r'C:\Users\Grillex\PycharmProjects\Widar-DL-Project\rnn_model_olddataset.pth', map_location=DEVICE))
model.eval()

# Load your test data
def load_test_data():
    test_sequences = []
    test_labels = []

    test_data_path = r'C:\Users\Grillex\Desktop\Widardata\Widardata\test'  # Update this path to your test data location

    for movement_folder in os.listdir(test_data_path):
        movement_path = os.path.join(test_data_path, movement_folder)

        if os.path.isdir(movement_path):
            label = movement_folder  # Use the folder name as the label

            for file_name in os.listdir(movement_path):
                if file_name.endswith('.csv'):
                    file_path = os.path.join(movement_path, file_name)

                    # Load the CSV file
                    data = load_csv_file(file_path)
                    if data is None:
                        continue  # Skip if there was an error in loading

                    # Create sequences from the data
                    sequences = create_sequences(data, SEQ_LENGTH)

                    # Append sequences and labels
                    test_sequences.extend(sequences)
                    test_labels.extend([label] * len(sequences))

    # Convert to numpy arrays
    test_sequences = np.array(test_sequences)
    test_labels = np.array(test_labels)

    return test_sequences, test_labels

# Load the test data
test_sequences, test_labels = load_test_data()

# Use LabelEncoder to convert labels to the same format used during training
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(test_labels)

# Create dataset and dataloader
test_dataset = CSIDataset(test_sequences, encoded_labels)
test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

# Evaluate the model
with torch.no_grad():
    correct = 0
    total = 0
    for inputs, targets in test_dataloader:
        inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
        outputs = model(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += targets.size(0)
        correct += (predicted == targets).sum().item()

    print(f'Accuracy: {100 * correct / total}%')
