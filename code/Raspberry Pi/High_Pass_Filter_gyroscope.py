import time
import math
import numpy as np

import ST_L3GD20H
import calibrate_gyro



angle_raw = np.zeros([100000,3],float)
angle_hp = np.zeros([100000,3],float)
f_c = 0.1
tau = float(1)/float(2*3.14*f_c)


L3GD = ST_L3GD20H.L3GD20H()
offset_gyro = calibrate_gyro.calibrate(L3GD)
print("OFFSET: " + str(offset_gyro) + " deg/s")
#Impongo le condizioni inziali
roll_gyro_previous = 0
pitch_gyro_previous = 0
yaw_gyro_previous = 0
roll_hp_previous = 0
pitch_hp_previous = 0
yaw_hp_previous = 0
print("Inizio a raccogliere i dati")
start = time.time()
for i in range(20000):
    #Reading Gyroscope Data
    omega = L3GD.read()
    #Correzione
    omega_x = omega[0] - offset_gyro[0]
    omega_y = omega[1] - offset_gyro[1]
    omega_z = omega[2] - offset_gyro[2]
    #Calcolo coefficente di filtraggio
    time_el = time.time() - start
    start = time.time()
    alpha_hp = float(tau)/float(tau+time_el)
    #Integrazione Numerica
    delta_roll_gyro = math.radians(omega_x*time_el)
    delta_pitch_gyro = math.radians(omega_y*time_el)
    delta_yaw_gyro = math.radians(omega_z*time_el)
    roll_gyro = roll_gyro_previous + delta_roll_gyro
    pitch_gyro = pitch_gyro_previous + delta_pitch_gyro
    yaw_gyro = yaw_gyro_previous + delta_yaw_gyro
    #Fitraggio
    roll_hp = alpha_hp*roll_hp_previous + alpha_hp*(roll_gyro - roll_gyro_previous)
    pitch_hp = alpha_hp*pitch_hp_previous + alpha_hp*(pitch_gyro - pitch_gyro_previous)
    yaw_hp = alpha_hp*yaw_hp_previous + alpha_hp*(yaw_gyro - yaw_gyro_previous)
    #Aggiorno i valori
    roll_gyro_previous = roll_gyro
    pitch_gyro_previous = pitch_gyro
    yaw_gyro_previous = yaw_gyro
    roll_hp_previous = roll_hp
    pitch_hp_previous = pitch_hp
    yaw_hp_previous = yaw_hp
    angle_raw[i,0] = roll_gyro
    angle_raw[i,1] = pitch_gyro
    angle_raw[i,2] = yaw_gyro
    angle_hp[i,0] = roll_hp
    angle_hp[i,1] = pitch_hp
    angle_hp[i,2] = yaw_hp

    
print("Finito Stampo i dati su file.")
#STAMPO SU FILE I DUE SEGNALI
#Raw Roll
file_path_name = "gyro_roll_raw.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw[i,0]) + "\n")
data.close()
#High Passed Roll
file_path_name = "gyro_roll_high_pass.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_hp[i,0]) + "\n")
data.close()
#Raw Pitch
file_path_name = "gyro_pitch_raw.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw[i,1]) + "\n")
data.close()
#High Passed Pitch
file_path_name = "gyro_pitch_high_pass.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_hp[i,1]) + "\n")
data.close()
#Raw Yaw
file_path_name = "gyro_yaw_raw.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw[i,2]) + "\n")
data.close()
#High Passed Yaw
file_path_name = "gyro_yaw_high_pass.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_hp[i,2]) + "\n")
data.close()
    
    
    
