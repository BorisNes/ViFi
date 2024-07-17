# ViFi (Vital signs with WiFi)
<img src="https://github.com/user-attachments/assets/d2bca8d5-6e5f-4240-9033-10ef52e83c3a" alt="vifi" width="400" height="400">

This project is under the course of "Deep Learning 046211" By the, [Technion ECE Department](https://ece.technion.ac.il/).

## Submitted by 
Boris Nesterenko, ECE Student.

Snir Carmeli - Bs.c in Mechanical Engineering.

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
