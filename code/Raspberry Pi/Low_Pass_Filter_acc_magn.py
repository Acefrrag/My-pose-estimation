import ST_LSM303DLHC
import calibrate_acc
import calibrate_magn
import time
import math
import numpy as np


angle_raw = np.zeros([100000,3],float)  #Anche se e una matrice utilizzero solo le prima due colonne. La prima per il roll, la seconda per il pitch.
angle_lp = np.zeros([100000,3],float)   #Anche se e una matrice utilizzero solo le prima due colonne. La prima per il roll, la seconda per il pitch.
acc_raw = np.zeros([100000,3],float)
acc_lp = np.zeros([100000,3],float)
f_c = 1
tau = float(1)/float(2*3.14*f_c)

LSM = ST_LSM303DLHC.LSM303()
 
acc_offset = calibrate_acc.calibrate(LSM)
#acc_offset = np.array([0,0,0],float)
print("OFFSET: " + str(acc_offset) + " g")
#magn_offset = calibrate_magn.calibrate(LSM)
magn_offset = np.array([0,0,0],float)
print("OFFSET: " + str(magn_offset) + " gauss")
time.sleep(1)
#Inizializzo valore filtrato
(acc,magn) = LSM.read()
G_x_raw, G_y_raw, G_z_raw = acc
B_x_raw, B_y_raw, B_z_raw = magn
G_x_lp_raw = G_x_raw
G_y_lp_raw = G_y_raw
G_z_lp_raw = G_z_raw
B_x_lp_raw = B_x_raw
B_y_lp_raw = B_y_raw
B_z_lp_raw = B_z_raw
start_sampling = time.time()
for i in range(10000):
    #DATI GREZZI
    (acc,magn) = LSM.read()
    G_x_raw, G_y_raw, G_z_raw = acc
    B_x_raw, B_y_raw, B_z_raw = magn
    sampling_time = time.time() - start_sampling
    start_sampling = time.time()
    #Calcolo coefficente di filtraggio
    alfa_lp = float(sampling_time)/float((tau+sampling_time))
    #DATI FILTRATI
    G_x_lp_raw = alfa_lp*G_x_raw+(1-alfa_lp)*G_x_lp_raw
    G_y_lp_raw = alfa_lp*G_y_raw+(1-alfa_lp)*G_y_lp_raw
    G_z_lp_raw = alfa_lp*G_z_raw+(1-alfa_lp)*G_z_lp_raw
    B_x_lp_raw = alfa_lp*B_x_raw+(1-alfa_lp)*B_x_lp_raw
    B_y_lp_raw = alfa_lp*B_y_raw+(1-alfa_lp)*B_y_lp_raw
    B_z_lp_raw = alfa_lp*B_z_raw+(1-alfa_lp)*B_z_lp_raw
    #DATI CALIBRATI(SIA GREZZI CHE FILTRATI)
    G_x = G_x_raw - acc_offset[0]
    G_y = G_y_raw - acc_offset[1]
    G_z = G_z_raw - acc_offset[2]
    G_x_lp = G_x_lp_raw - acc_offset[0]
    G_y_lp = G_y_lp_raw - acc_offset[1]
    G_z_lp = G_z_lp_raw - acc_offset[2]
    B_x = B_x_raw - magn_offset[0]
    B_y = B_y_raw - magn_offset[1]
    B_z = B_z_raw - magn_offset[2]
    B_x_lp = B_x_lp_raw - magn_offset[0]
    B_y_lp = B_y_lp_raw - magn_offset[1]
    B_z_lp = B_z_lp_raw - magn_offset[2]
    #Calcolo angolo dalle accelerazioni e campi magentici non filtrati
    roll_acc = math.atan2(G_y,G_z)
    pitch_acc = math.atan((-G_x)/math.sqrt(G_y*G_y + G_z*G_z))
    yaw_magn = math.atan2(B_z*math.sin(roll_acc)-B_y*math.cos(roll_acc),(B_x*math.cos(pitch_acc))+(B_y*math.sin(pitch_acc)*math.sin(roll_acc))+(B_z*math.sin(pitch_acc)*math.cos(roll_acc)))
    #Calcolo angolo dalle accelerazioni e campi magentici filtrati
    roll_lp = math.atan2(G_y_lp,G_z_lp)
    pitch_lp = math.atan((-G_x_lp)/math.sqrt(G_y_lp*G_y_lp + G_z_lp*G_z_lp))
    yaw_lp = math.atan2(B_z_lp*math.sin(roll_lp)-B_y_lp*math.cos(roll_lp),(B_x_lp*math.cos(pitch_lp))+(B_y_lp*math.sin(pitch_lp)*math.sin(roll_lp))+(B_z_lp*math.sin(pitch_lp)*math.cos(roll_lp)))
    #Aggiungo i dati ai segnali
    angle_raw[i,0] = roll_acc
    angle_lp[i,0] = roll_lp
    angle_raw[i,1] = pitch_acc
    angle_lp[i,1] = pitch_lp
    angle_raw[i,2] = yaw_magn
    angle_lp[i,2] = yaw_lp
    acc_raw[i,0] = G_x
    acc_lp[i,0] = G_x_lp
print("Finish")

#STAMPO SEGNALI SU FILE
#Raw Theta
file_path_name = "acc_raw.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(acc_raw[i,0]) + "\n")
data.close()
#Low Passed Theta
file_path_name = "acc_low_pass.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(acc_lp[i,0]) + "\n")
data.close()
#Raw Roll
file_path_name = "acc_roll_raw.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw[i,0]) + "\n")
data.close()
#Low Passed Roll
file_path_name = "acc_roll_low_pass.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_lp[i,0]) + "\n")
data.close()
#Raw Pitch
file_path_name = "acc_pitch_raw.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw[i,1]) + "\n")
data.close()
#Low Passed Pitch
file_path_name = "acc_pitch_low_pass.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_lp[i,1]) + "\n")
data.close()
#Raw Yaw
file_path_name = "magn_yaw_raw.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_raw[i,2]) + "\n")
data.close()
#Low Passed Yaw
file_path_name = "magn_yaw_low_pass.txt"
data = open(file_path_name,"w")
for i in range(10000):
	data.write(str(angle_lp[i,2]) + "\n")
data.close()
    
    
    

    

    
