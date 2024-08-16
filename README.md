# ViFi (Visualize gestures with WiFi)
<img src="https://github.com/user-attachments/assets/d2bca8d5-6e5f-4240-9033-10ef52e83c3a" alt="vifi" width="400" height="400">

This project is under the course of "Deep Learning 046211" By the, [Technion ECE Department](https://ece.technion.ac.il/).

## Submitted by 
Boris Nesterenko, ECE Student.

Snir Carmeli - Bs.c in Mechanical Engineering.

## Table of contents
- [Project Overview](https://github.com/BorisNes/ViFi/tree/main?tab=readme-ov-file#overview)

- [Background](https://github.com/BorisNes/ViFi/tree/main?tab=readme-ov-file#overview)

- [Data acquisition](https://github.com/BorisNes/ViFi/blob/main/README.md#data-acquisition)

## Overview
This project was heavily inspired by [This paper](https://arxiv.org/pdf/2203.03980).
We aim to use WiFi signals, specifically Channel State Information ([CSI](https://en.wikipedia.org/wiki/Channel_state_information)), to monitor heart rate and respiration rate in human subjects. 
This will be achieved by leveraging the IEEE 802.11n WiFi standard, which includes MIMO and [OFDM](https://en.wikipedia.org/wiki/Orthogonal_frequency-division_multiplexing) technologies, which captures detailed signal information through CSI. 
By inputting CSI data into a Convolutional Neural Network ([CNN](https://en.wikipedia.org/wiki/Convolutional_neural_network)), we aim to detect vital signs by analyzing changes in subcarrier signal strengths. 
Despite challenges such as dataset assumptions and signal noise, the goal is to develop a technology that can be integrated into smartphones and home routers for non-invasive health monitoring.

## Background

Interest in using CSI for healthcare began in the 2010s with advancements in WiFi standards like IEEE 802.11n. Researchers explored CSI for vital sign monitoring, leading to promising prototypes, and the integration of machine learning, especially deep learning, in the late 2010s improved analysis accuracy. This progress has sparked significant commercial and practical interest, paving the way for CSI-based health monitoring in consumer devices.

Nowadays, WiFi is a large part of our everyday lives. In every location, hotspots and [Wifi radio waves](https://en.wikipedia.org/wiki/Wi-Fi#Waveband) are present.
Before the beginning of the semester, some spare time has led us to become aware of CSI and the great potential it has. After some homemade research, the field of CSI in clinical setups has been studied but has yet to be widely adopted by clinicians and healthcare personell. 

Traditional methods like [ECG](https://en.wikipedia.org/wiki/Electrocardiography) and [Echocardiography](https://en.wikipedia.org/wiki/Echocardiography) are still preferred by cardiologists and healthcare personell due to their high accuracy and their proven medical efficacy over decades.

By using WiFi we hope to contribute to the medical field by bringing awareness to the technology, by trying to develop and bring a user friendly hardware-software combination to clinical setups and learn a new thing or two.

## Data acquisition

Due to time constraints, we shall use a [dataset](https://github.com/Gi-z/CSI-Data/tree/main/Internal/intel/Heart%20Rate) published by [Gi-z](https://github.com/Gi-z) and contains CSI data from various human activities, accuired using specific WiFi adapters that allow for CSI extraction (Most routers and smartphones do not allow access to CSI data due to security reasons).

For those who are intersted, CSI data can be extracted from an ESP32 SoC by flashing it with special firmware. More detailed information about the process can be found [here](https://stevenmhernandez.github.io/ESP32-CSI-Tool/). 

Here's a heatmap of a test we conducted 6 months ago ![image](https://github.com/user-attachments/assets/a83df65f-366f-44df-81ab-bc23c47e7df4)

It was obtained by connecting a smartphone to the ESP32 acting as an Access Point, and continuously sending [ping](https://en.wikipedia.org/wiki/Ping_(networking_utility)) requests to ensure continuous transmittion and acquisition from the ESP32. The scenario behind the graph is holding the smartphone in the same room as the ESP32 (which can be seen by the blue smear along the subcarriers in frames 20-40, meaning the WiFi indeed sensed some obstacles between the smartphone and the ESP32, resulting in decreased signal strength), and later returning to the room and bringing the phone in contact with the ESP32, as depicted with a yellow smear across all the subcarriers, meaning the signal is strong.

