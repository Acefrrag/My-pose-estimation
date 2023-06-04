# My pose estimation
This repository contains the code developed as internship work at Polytechnic Marche University during the A.Y. 2017/2018 as partial fulfillment of the requirement for my Bachelor's degree.

## Duties

The pose estimation of the Adafruit 9DOF IMU Breakout Board was performed accomplishing the following tasks:

1. Driver Development
2. Raw data acquisition, data formatting, conversion to SI values
3. Data Calibration and Offset Computation
4. Sensor Fusion and Pose Estimation
5. Pose Representation on remote machine

## Driver

Adafruit provides embedded programmer with a C++ Adafruit Sensor library. I wanted to try to develop my own one-off driver to practice driver development but the Unified library is better to use because the off-the-shelf library allow the embedded developer to switch in between sensor without worrying about data formata, unit of measure etc...

## Hardware

![Internship_BG](https://github.com/Acefrrag/My-pose-estimation/assets/59066474/5091b578-ea42-462f-ad95-1bd6ef2f5839){width="100px"}

<p aligh="center">
<img src=https://github.com/Acefrrag/My-pose-estimation/assets/59066474/5091b578-ea42-462f-ad95-1bd6ef2f5839 width="50%">
</p>

***Adafruit 9 DOF IMU Breakout Board*** embedding:
* L3DG20H
* LSM303DLHC

***Raspeberry Pi 3 Model B***

***Remote Laptop***





