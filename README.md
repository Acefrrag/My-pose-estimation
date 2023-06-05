# My pose estimation
This repository contains the code developed during my internship work at Polytechnic Marche University during the A.Y. 2017/2018 as partial fulfillment of the requirement for my Bachelor's degree.

## Duties

The pose estimation of the Adafruit 9DOF IMU Breakout Board was performed accomplishing the following tasks:

1. Driver Development
2. Raw data acquisition, data formatting, conversion to SI values
3. Data Calibration and Offset Computation
4. ***Sensor Fusion and Attitude Estimation***
5. Pose Visualizer on remote machine

## Driver

Adafruit provides embedded programmer with an Arduino C++ [Adafruit Unified Sensor Library](https://github.com/adafruit/Adafruit_Sensor). I wanted to try to develop my own one-off driver on Raspberry Pi to practice driver development but the Unified Driver still remain the best choice as described [here](https://learn.adafruit.com/using-the-adafruit-unified-sensor-driver/introduction). I took inspiration from TonyDiCola Raspberry Pi drivers (see the Credits section).

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

## Attitude Estimation

The attitude estimation consists in the computation of the Euler angles starting from the reading of the sensors. Specifically the Tait-Bryan angles (sequence x, y', z'') were computed.

## Sensor Fusion Algorithm

These algorithm try to get the most from every sensor used in attitude estimation.

### "Standard"

This is the most naive sensor fusion algorithm implemented. It does not exists in the literature and it does not have a real name. The concept consists in appling a low-pass filter and high-pass filter with the same cut-off frequency F_{c} respectively to the gyro and to the accelerometer and magnetometer. I found it by watching some youtube videos...

### Complementary Filter

The complementary filter is characterized by a parameter $\alpha_{CF}$ (which can be empirically assosicated to a Standard Filter cut-off frequency).

### Corrected Complementary Filter

The estimation of the pose consists in the Euler angles estimation of a rigid body. Euler angles do have discontinuity, hence the complementary filters out the sudden jump producing incorrect pose estimation readings. The complementary filter is disabled when approaching this discontinuity.

### Final Filter

The final filter consisted in the combination of the Corrected Complementary Filter and the Standard filter.

## Credits

The driver I developed took inspiration from the drivers developed by Tony Dicola. I thank him for the work he is doing/has done for the embedded system community.



