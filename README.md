# ViFi (Visualize gestures with WiFi)

<img src="https://github.com/user-attachments/assets/8557a4ca-8686-4031-9ffb-77b901989143" alt="vifi" width="400" height="400">

This project is under the course of "Deep Learning 046211" By the, [Technion ECE Department](https://ece.technion.ac.il/).

## Submitted by 
Boris Nesterenko, ECE Student.

Snir Carmeli - Bs.c in Mechanical Engineering, MSc. in ECE

## Table of contents
- [Project Overview](https://github.com/BorisNes/ViFi/tree/main?tab=readme-ov-file#overview)

- [Background](https://github.com/BorisNes/ViFi/tree/main?tab=readme-ov-file#overview)

- [Data acquisition](https://github.com/BorisNes/ViFi/blob/main/README.md#data-acquisition)

## Overview

This project is inspired by advancements in wireless sensing and deep learning. We aim to develop a system for recognizing hand gestures using WiFi signals, leveraging the Widar 3.0 dataset and Recurrent Neural Networks (RNNs). WiFi Channel State Information (CSI) provides a detailed understanding of how signals propagate through space, and by analyzing variations in these signals, our model can distinguish between different hand gestures.
In a test conducted a few months ago due to personal interest, we used an ESP32 module to visualize how WiFi signals change with different hand positions and movements. The heatmap below illustrates signal variations detected by the ESP32 as it responds to changes in the environment. This experiment highlights the potential of WiFi-based gesture recognition, which we aim to refine and expand upon using the Widar 3.0 dataset and advanced neural networks.
![image](https://github.com/user-attachments/assets/a83df65f-366f-44df-81ab-bc23c47e7df4)

The ultimate goal is to create a non-invasive, accurate gesture recognition system that could be integrated into existing WiFi infrastructures. More information on the topic can be found in [this](https://arxiv.org/pdf/2207.07859) paper.


## Background

The use of WiFi signals for gesture recognition is a relatively new field that has gained traction in recent years. With the growing interest in human-computer interaction and smart environments, the ability to recognize gestures using existing WiFi infrastructure is particularly appealing. This approach bypasses the need for additional hardware like cameras or wearable devices, making it both cost-effective and privacy-preserving.

The Widar 3.0 dataset is a significant resource in this field, providing extensive data on human gestures captured through WiFi CSI. By utilizing this dataset and applying deep learning techniques, specifically RNNs, we aim to achieve robust gesture recognition. This project builds on previous research but shifts the focus towards practical implementation using RNNs, which are well-suited for sequential data like WiFi signals.

## Data acquisition

For this project, we are utilizing the Widar 3.0 dataset, which includes a wide variety of hand gestures captured using WiFi signals. The dataset was collected in controlled environments, ensuring high-quality data for training and evaluation. It was preprocessed into .csv format by [xyanchen](https://github.com/xyanchen/WiFi-CSI-Sensing-Benchmark)

The Widar 3.0 dataset contains CSI data recorded with specific WiFi Network Interface Controllers (NICs) that can extract detailed signal information. This data is ideal for training our RNN model to recognize different gestures based on the subtle variations in signal patterns caused by hand movements.



## Architecture

We have chosen to use an RNN to process the data and classify the input into one of 22 possible classes, each class being a hand gesture.

Our choice for the network was due the fact that RNN's are great for processing sequential data.

An outline of the network can be seen in the image below: ![pn2g](https://github.com/user-attachments/assets/23b26074-8d16-4896-8d52-feb1a0e27065)


## Results

During training, we used tensorboard to keep track of the average loss each epoch :
![image](https://github.com/user-attachments/assets/f476e61a-f9f1-4eba-a9d7-d8864298ce17)
One line was trained on 600 samples per folder, and the other one was trained on all data. Resulting Accuracy: 64.388%
And to try and make it overfit, we ran it for 200 epochs:
![image](https://github.com/user-attachments/assets/797622b8-166b-4cfb-bcfd-de6a0dfe375b)
Resulting Accuracy: 63.603%
We also tried a different architecture, by changing the number of neurons in the hidden layer to 128 and have 3 hidden layers.
This time, overfitting occured when training for 50 epochs:
![image](https://github.com/user-attachments/assets/4f5cf6cf-3337-4be1-9b45-dcc531b16790)

## Running the code

Our code was run inside of a virtual environment created by PyCharm. The model was trained on my trusty yet pricey Nvidia 4070 Ti. Currently CUDA compatible, training can run off of a CPU but it's not advisable due to long runtimes. An AMD or Intel backend might be implemented in the future, just for the sake of battling Nvidia's monopoly.
- Install all requirements for this code, which are specified in the requirements.txt file
- Download the Widar Data from [xyanchen](https://github.com/xyanchen/WiFi-CSI-Sensing-Benchmark) (or just click [this](https://drive.google.com/drive/folders/1R0R8SlVbLI1iUFQCzh_mH90H_4CW2iwt?usp=sharing) link). Make sure you only use the WidarData folder.
- In the "load_and_train_FINAL.py" code, change line #94 to the path of the root of the folder containing the WidarData dataset.
- The code loads the dataset (MAY TAKE VERY LONG, ABOUT 12 MINS) and caches the processed numpy strings into a .npy file in a specified directory (line 96), to save time if you just want to retrain the model using different hyperparameters without waiting for all data to be loaded. Tensorboard(python package) can be used to view the training process
- (optional) Change the hyperparameters of the neural network in the code. Default is 2 hidden layers, each with a size of 64, and run for 25 epochs.
- After training is done, the weights are saved to a .pth file, in the directory specified in line #184. Copy the path of the .pth file (life hack- shift+right click adds a "copy as path" option in the dropdown menu, thank me later) and change line number #25 in the "inference_FINAL.py" file to specify the directory of the weights file. Of course also change line number #33 of "inference_FINAL.py" to specify the location of the dataset, for loading of the test folder.
- Run "inference_FINAL.py", the resulting model accuracy should pop up after the execution.
