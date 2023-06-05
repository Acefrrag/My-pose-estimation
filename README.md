# My pose estimation
This repository contains the code developed as my internship work at Polytechnic Marche University during the A.Y. 2017/2018 as partial fulfillment of the requirement for my Bachelor's degree.

## Duties

The pose estimation of the Adafruit 9DOF IMU Breakout Board was performed accomplishing the following tasks:

1. Driver Development
2. Raw data acquisition, data formatting, conversion to SI values
3. Data Calibration and Offset Computation
4. ***Sensor Fusion and Attitude Estimation***
5. Pose Visualizer on remote machine

## Driver

Adafruit provides embedded programmer with a C++ [Adafruit Unified Sensor Library](https://github.com/adafruit/Adafruit_Sensor). I wanted to try to develop my own one-off driver to practice driver development but the Unified Driver still remain the best choice. More details can be found [here](https://learn.adafruit.com/using-the-adafruit-unified-sensor-driver/introduction)

## Hardware

<p align="center">
<img src=https://github.com/Acefrrag/My-pose-estimation/assets/59066474/5091b578-ea42-462f-ad95-1bd6ef2f5839 width="50%">
</p>

***Adafruit 9 DOF IMU Breakout Board*** embedding:
* L3DG20H
* LSM303DLHC

***Raspeberry Pi 3 Model B***

***Remote Laptop***

## Software

Python

Matlab

## Protocols

The communication with 9DOF Breakout Board takes place with an I2C protocol. Raspbian-enviornment Python provides the ***smbus*** library to enable data writing and reading of the I2C sensors registers.

The comunication between Raspberry Pi and the Remote Desktop is implemeted using an UDP protocol. The Raspberry Python client includes the package socket to implement a UDP protocol. The Matlab remote Server uses a UDP buffer to asynchronously read the (Roll, Pitch, Yaw) data.

## Sensor Fusion Algorithm

These algorithm try to get the most from every sensor used in attitude estimation.

### "Stamdard"

This is the most naive sensor fusion algorithm implemented. It does not exists in the literature and it does not have a real name. The concept consists in appling a low-pass filter and high-pass filter with the same cut-off frequency F_{c} respectively to the gyro and to the accelerometer and magnetometer.

### Complementary Filter

The complementary filter is characterized by a parameter $\alpha$ (which can be empirically assosicated to a Standard Filter cut-off frequency)

### Corrected Complementary Filter

For the speci

### Final Filter

The final filter consisted in the combination of the Corrected Complementary Filter and the Standard filter.



