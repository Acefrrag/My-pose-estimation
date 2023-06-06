import time
import math
import numpy as np

import ST_L3GD20H
import ST_LSM303DLHC
import calibrate_gyro
import calibrate_acc
import calibrate_magn

delta_time_vect = np.zeros(10000,float)
angle_raw_1 = np.zeros([10000,3],float)
angle_raw_2 = np.zeros([10000,3],float)
angle_f = np.zeros([10000,3],float)
fc = 1
tau = float(1)/(2*3.14*fc)

#Istanzio la classe L3GD20H e inizializzo le variabili del giroscopio(condizio
#ni iiniziali)
L3GD = ST_L3GD20H.L3GD20H()
#gyro_offset = calibrate_gyro.calibrate(L3GD)
gyro_offset = np.array([0,0,0],float)
#Istanzio la classe LSM303DLHC e inizializzo le variabili di accelerometro
#e magnetometro
LSM = ST_LSM303DLHC.LSM303()
#magn_offset = calibrate_magn.calibrate(LSM)
magn_offset = np.array([0,0,0],float)
#acc_offset = calibrate_acc.calibrate(LSM)
acc_offset = np.array([0,0,0],float)

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
#IMPONGO LE CONDIZIONI INIZIALI
(G_raw, B_raw) = LSM.read()
G_x_raw, G_y_raw, G_z_raw = G_raw
B_x_raw, B_y_raw, B_z_raw= B_raw
G_x_lp_raw = G_x_raw
G_y_lp_raw = G_y_raw
G_z_lp_raw = G_z_raw
B_x_lp_raw = B_x_raw
B_y_lp_raw = B_y_raw
B_z_lp_raw = B_z_raw
roll_gyro_prev = 0
pitch_gyro_prev = 0
yaw_gyro_prev = 0
roll_hp = 0
pitch_hp = 0
yaw_hp = 0
omega_x_prev = 0
omega_y_prev = 0
omega_z_prev = 0
start = time.time()
for i in range(10000):
    
    #Leggo i dati dal giroscopio
    omega_raw = L3GD.read()
    
    #Leggo i dati dall accelerometro e dal magnetometro
    (G_raw, B_raw) = LSM.read()
    G_x_raw, G_y_raw, G_z_raw = G_raw
    B_x_raw, B_y_raw, B_z_raw= B_raw

    #Correzione dei valori mediante i valori di offset
    #derivanti dalla calibrazione(Calibrazione del solo giroscopio)
    omega_x = omega_raw[0] - gyro_offset[0]
    omega_y = omega_raw[1] - gyro_offset[1]
    omega_z = omega_raw[2] - gyro_offset[2]

    #Calcolo tempo di campionamento e coefficenti di filtro
    delta_time = time.time() - start
    start = time.time()
    alfa_hp = float(tau)/float((tau + delta_time))
    alfa_lp = float(delta_time)/float((tau+delta_time))

    #Integrazione Numerica
    roll_gyro_curr = roll_gyro_prev + math.radians(omega_x_prev*delta_time)
    pitch_gyro_curr = pitch_gyro_prev + math.radians(omega_y_prev*delta_time)
    yaw_gyro_curr = yaw_gyro_prev + math.radians(omega_z_prev*delta_time)


    #Filtro segnale giroscopio con filtro passa alto
    roll_hp = alfa_hp*roll_hp+alfa_hp*(roll_gyro_curr-roll_gyro_prev)
    pitch_hp = alfa_hp*pitch_hp+alfa_hp*(pitch_gyro_curr-pitch_gyro_prev)
    yaw_hp = alfa_hp*yaw_hp+alfa_hp*(yaw_gyro_curr-yaw_gyro_prev)

    #Filtro Accelerometro e Magnetometro con filtro passa basso
    G_x_lp_raw = alfa_lp*G_x_raw+(1-alfa_lp)*G_x_lp_raw
    G_y_lp_raw = alfa_lp*G_y_raw+(1-alfa_lp)*G_y_lp_raw
    G_z_lp_raw = alfa_lp*G_z_raw+(1-alfa_lp)*G_z_lp_raw
    B_x_lp_raw = alfa_lp*B_x_raw+(1-alfa_lp)*B_x_lp_raw
    B_y_lp_raw = alfa_lp*B_y_raw+(1-alfa_lp)*B_y_lp_raw
    B_z_lp_raw = alfa_lp*B_z_raw+(1-alfa_lp)*B_z_lp_raw

    #Correzioni Dati Magnetometro e Accelerometro(Calibro i rimanenti sensori).
    #La correzione di questi due sensori va fatta qui per la NOTA IMPORTANTE
    #presente nei moduli.(In ogni caso effettuo la correzione anche sui valori
    #non filtrati per il confronto).
    #DATI NON FILTRATI:
    B_x = B_x_raw - magn_offset[0]
    B_y = B_y_raw - magn_offset[1]
    B_z = B_z_raw - magn_offset[2]
    G_x = G_x_raw - acc_offset[0]
    G_y = G_y_raw - acc_offset[1]
    G_z = G_z_raw - acc_offset[2]
    #DATI FILTRATI:
    B_x_lp = B_x_lp_raw - magn_offset[0]
    B_y_lp = B_y_lp_raw - magn_offset[1]
    B_z_lp = B_z_lp_raw - magn_offset[2]
    G_x_lp = G_x_lp_raw - acc_offset[0]
    G_y_lp = G_y_lp_raw - acc_offset[1]
    G_z_lp = G_z_lp_raw - acc_offset[2]

    
    #Computazione angoli
    roll_lp = math.atan2(G_y_lp,G_z_lp)    
    pitch_lp = math.atan((-G_x_lp)/math.sqrt(G_y_lp*G_y_lp + G_z_lp*G_z_lp))
    yaw_lp = math.atan2(B_z_lp*math.sin(roll_lp)-B_y_lp*math.cos(roll_lp),(B_x_lp*math.cos(pitch_lp))+(B_y_lp*math.sin(pitch_lp)*math.sin(roll_lp))+(B_z_lp*math.sin(pitch_lp)*math.cos(roll_lp)))

    #Applico il filtro Standard
    roll_f = roll_hp + roll_lp
    pitch_f = pitch_hp + pitch_lp
    yaw_f = yaw_hp + yaw_lp

    #Computzione Angoli Non Passa Basso filtrati
    roll_acc = math.atan2(G_y,G_z)    
    pitch_acc = math.atan((-G_x)/math.sqrt(G_y*G_y + G_z*G_z))
    yaw_magn = math.atan2(B_z*math.sin(roll_acc)-B_y*math.cos(roll_acc),(B_x*math.cos(pitch_acc))+(B_y*math.sin(pitch_acc)*math.sin(roll_acc))+(B_z*math.sin(pitch_acc)*math.cos(roll_acc)))

    #Aggingo i dati ai segnali che verrano stampati su file
    delta_time_vect[i]=delta_time
    angle_raw_1[i,0] = roll_acc
    angle_raw_1[i,1] = pitch_acc
    angle_raw_1[i,2] = yaw_magn
    angle_raw_2[i,0] = roll_gyro_curr
    angle_raw_2[i,1] = pitch_gyro_curr
    angle_raw_2[i,2] = yaw_gyro_curr
    angle_f[i,0] = roll_f
    angle_f[i,1] = pitch_f
    angle_f[i,2] = yaw_f

    #Agiorno gli angoli
    roll_gyro_prev = roll_gyro_curr
    pitch_gyro_prev = pitch_gyro_curr
    yaw_gyro_prev = yaw_gyro_curr
    omega_x_prev = omega_x
    omega_y_prev = omega_y
    omega_z_prev = omega_z
    

print("Finito. Stampo i dati su file.")
#STAMPO I SEGNALI
#Raw Roll (Accelerometer)
file_path_name = "roll_raw_acc.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw_1[i,0]) + "\n")
data.close()
#Raw Roll (Gyroscope)
file_path_name = "roll_raw_gyro.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw_2[i,0]) + "\n")
data.close()
#Complementary Filtered Roll
file_path_name = "roll_sf.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_f[i,0]) + "\n")
data.close()

#Raw Pitch (Accelerometer)
file_path_name = "pitch_raw_acc.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw_1[i,1]) + "\n")
data.close()
#Raw Pitch (Gyroscope)
file_path_name = "pitch_raw_gyro.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw_2[i,1]) + "\n")
data.close()
#Complementary Filtered Pitch
file_path_name = "pitch_sf.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_f[i,1]) + "\n")
data.close()

#Raw Yaw (Magnetometer)
file_path_name = "yaw_raw_magn.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw_1[i,2]) + "\n")
data.close()
#Raw Yaw (Gyroscope)
file_path_name = "yaw_raw_gyro.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw_2[i,2]) + "\n")
data.close()
#Complementary Filtered Yaw
file_path_name = "yaw_sf.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_f[i,2]) + "\n")
data.close()
