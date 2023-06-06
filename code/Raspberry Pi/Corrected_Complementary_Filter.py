import time
import math
import numpy as np

import ST_L3GD20H
import ST_LSM303DLHC
import calibrate_gyro
import calibrate_magn
import calibrate_acc


delta_time_vect = np.zeros(10000,float)
angle_raw = np.zeros([10000,3],float)
angle_cf = np.zeros([10000,3],float)
a = np.zeros([10000],float)
#Ho una frequenza di taglio per ogni angolo. Queste saranno variabili nel tempo
fc_x = 1
fc_y = 1
fc_z = 1
tau_x = float(1)/(2*3.14*fc_x)
tau_y = float(1)/(2*3.14*fc_y)
tau_z = float(1)/(2*3.14*fc_z)


#Istanzio la classe L3GD20H e inizializzo le variabili del giroscopio(condizio
#ni iiniziali)
L3GD = ST_L3GD20H.L3GD20H()
gyro_offset = calibrate_gyro.calibrate(L3GD)
#gyro_offset = np.array([0,0,0],float)
#Istanzio la classe LSM303DLHC e inizializzo le variabili di accelerometro
#e magnetometro
LSM = ST_LSM303DLHC.LSM303()
magn_offset = calibrate_magn.calibrate(LSM)
#magn_offset = np.array([0,0,0],float)
acc_offset = calibrate_acc.calibrate(LSM)
#acc_offset = np.array([0,0,0],float)

#STAMPO GLI OFFSET:
print("STAMPO GLI OFFSET.")
time.sleep(1)
print("OFFSET ACCELEROMETRO:")
print("OFFSET: " + str(acc_offset) + " g")
print("OFFSET MAGNETOMETRO:")
print("OFFSET: " + str(magn_offset) + " gauss")
print("OFFSET GIROSCOPIO")
print("OFFSET: " + str(gyro_offset) + " deg/s")
time.sleep(0.5)
print("Inizio a raccogliere dati tra 1 secondo")
time.sleep(1)
#IMPONGOO LE CONDIZIONI INIZIALI
omega_x_prev = 0
omega_y_prev = 0
omega_z_prev = 0
roll_cf = 0
pitch_cf = 0
yaw_cf = 0
roll_cf_prev= 0
pitch_cf_prev = 0
yaw_cf_prev = 0
start = time.time()
for i in range(10000):
    #Lettura Dati Giroscopio
    omega_raw = L3GD.read()
    #Lettura dati accelerometro e magnetometro
    (G_raw, B_raw) = LSM.read()
    G_x_raw, G_y_raw, G_z_raw = G_raw
    B_x_raw, B_y_raw, B_z_raw = B_raw
    #Correzione Misurazioni
    G_x = G_x_raw - acc_offset[0]
    G_y = G_y_raw - acc_offset[1]
    G_z = G_z_raw - acc_offset[2]
    B_x = B_x_raw - magn_offset[0]
    B_y = B_y_raw - magn_offset[1]
    B_z = B_z_raw - magn_offset[2]
    omega_x = omega_raw[0] - gyro_offset[0]
    omega_y = omega_raw[1] - gyro_offset[1]
    omega_z = omega_raw[2] - gyro_offset[2]
    #Computazione angolo di roll e di pitch
    roll_acc = math.atan2(G_y,G_z)
    pitch_acc = math.atan((-G_x)/math.sqrt(G_y*G_y + G_z*G_z))

    #Calcolo periodo di campionamento e coefficente di filtro
    delta_time = time.time() - start
    start = time.time()
    alfa_cf_roll = tau_x/(tau_x + delta_time)
    alfa_cf_pitch = tau_y/(tau_y + delta_time)
    alfa_cf_yaw = tau_z/(tau_z + delta_time)

    #Filtraggio Roll e Pitch-Filtro Complementare
    roll_cf = alfa_cf_roll*(roll_cf_prev+math.radians(omega_x_prev*delta_time))+(1-alfa_cf_roll)*roll_acc
    pitch_cf = alfa_cf_pitch*(pitch_cf_prev+math.radians(omega_y_prev*delta_time))+(1-alfa_cf_pitch)*pitch_acc

    #Computazione angolo di yaw
    yaw_magn = math.atan2(B_z*math.sin(roll_cf)-B_y*math.cos(roll_cf),(B_x*math.cos(pitch_cf))+(B_y*math.sin(pitch_cf)*math.sin(roll_cf))+(B_z*math.sin(pitch_cf)*math.cos(roll_cf)))    

    #Filtraggio Yaw-Filtro Complementare
    yaw_cf = alfa_cf_yaw*(yaw_cf_prev+math.radians(omega_z_prev*delta_time))+(1-alfa_cf_yaw)*yaw_magn

    delta_time_vect[i]=delta_time
    angle_raw[i,0] = roll_acc
    angle_raw[i,1] = pitch_acc
    angle_raw[i,2] = yaw_magn
    angle_cf[i,0] = roll_cf
    angle_cf[i,1] = pitch_cf
    angle_cf[i,2] = yaw_cf
    roll_cf_prev = roll_cf
    pitch_cf_prev = pitch_cf
    yaw_cf_prev = yaw_cf
    #Calcolo nuova frequenza di taglio
    ####PARTE AGGIUNTA
    fc_x = 0.5*np.power(roll_cf_prev,6)+1
    fc_y = 0.5*np.power(pitch_cf_prev,6)+1
    fc_z = 0.5*np.power(yaw_cf_prev,6)+1
    tau_x = float(1)/(2*3.14*fc_x)
    tau_y = float(1)/(2*3.14*fc_y)
    tau_z = float(1)/(2*3.14*fc_z)
    ####
    #A CONTROLLARE
    omega_x_prev = omega_x
    omega_y_prev = omega_y
    omega_z_prev = omega_z

#STAMPO I SEGNALI SU FILE
#Raw Roll (Accelerometer)
file_path_name = "roll_raw.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw[i,0]) + "\n")
data.close()
#Complementary Filtered Roll
file_path_name = "roll_cf.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_cf[i,0]) + "\n")
data.close()

#Raw Pitch (Accelerometer)
file_path_name = "pitch_raw.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw[i,1]) + "\n")
data.close()
#Complementary Filtered Pitch
file_path_name = "pitch_cf.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_cf[i,1]) + "\n")
data.close()

#Raw Yaw (Magnetometer)
file_path_name = "yaw_raw.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw[i,2]) + "\n")
data.close()
#Complementary Filtered Yaw
file_path_name = "yaw_cf.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_cf[i,2]) + "\n")
data.close()



    

 

    
    

    
