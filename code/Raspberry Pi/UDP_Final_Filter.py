#Questo programma confronta gli angoli grezzi con quelli filtrati con l
#ultimo filtro discusso nella tesi.
#Questo consiste nell unione del filtro complementare corretto e del filtro
#standard.
#In questo fitro si applica lo schema a blocchi del filtro standard con l
#unica differenza che le frequenza di taglio dei filtri passa basso e passa alto
#sono diverse e valgono rispettivamente 1Hz e 0.1Hz, e che al termine i segnali
#non sono sommati tra di loro, ma vanno in ingresso al filtro complementare.

import time
import math
import numpy as np
import struct
import socket

import ST_L3GD20H
import ST_LSM303DLHC
import calibrate_gyro
import calibrate_magn
import calibrate_acc

#Inizializzo la socket che rappresenta la comunicazione UDP
my_socket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Instauro la connessione con il server
my_socket.connect(('192.168.1.107', 28000))


delta_time_vect = np.zeros(10000,float)
angle_raw = np.zeros([10000,3],float)
angle_cf = np.zeros([10000,3],float)
a = np.zeros([10000],float)
#Frequenza di taglio filtro standard e filtro passa alto
fc_hp = 0.1
fc_sf = 1
#Costanti di tempo
tau_hp = float(1)/(2*3.14*fc_hp)
tau_sf = float(1)/(2*3.14*fc_sf)
#Abbiamo una frequenza di taglio "complementare" per ogni angolo
#Queste frequenze varieranno nel tempo
fc_x = 1
fc_y = 1
fc_z = 1
#E di conseguenza le costanti di tempo
tau_x = float(1)/(2*3.14*fc_x)
tau_y = float(1)/(2*3.14*fc_y)
tau_z = float(1)/(2*3.14*fc_z)

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
#IMPONGOO LE CONDIZIONI INIZIALI
(G_raw, B_raw) = LSM.read()
G_x_raw, G_y_raw, G_z_raw = G_raw
B_x_raw, B_y_raw, B_z_raw= B_raw
#Calcolo gli angoli di roll, pitch e yaw., preoccupadosi di togliere il solo
#offset. L unica funzione infatti e quella di fungere da condizioni inziali
#per l angolo filtrato finale
B_x = B_x_raw - magn_offset[0]
B_y = B_y_raw - magn_offset[1]
B_z = B_z_raw - magn_offset[2]
G_x = G_x_raw - acc_offset[0]
G_y = G_y_raw - acc_offset[1]
G_z = G_z_raw - acc_offset[2]
roll_acc = math.atan2(G_y,G_z)
pitch_acc = math.atan((-G_x)/math.sqrt(G_y*G_y + G_z*G_z))
yaw_magn = math.atan2(B_z*math.sin(roll_acc)-B_y*math.cos(roll_acc),(B_x*math.cos(pitch_acc))+(B_y*math.sin(pitch_acc)*math.sin(roll_acc))+(B_z*math.sin(pitch_acc)*math.cos(roll_acc)))
roll_cf_prev= roll_acc
pitch_cf_prev = pitch_acc
yaw_cf_prev = yaw_magn
roll_gyro_prev = roll_acc
pitch_gyro_prev = pitch_acc
yaw_gyro_prev = yaw_magn
G_x_lp_raw = G_x_raw
G_y_lp_raw = G_y_raw
G_z_lp_raw = G_z_raw
B_x_lp_raw = B_x_raw
B_y_lp_raw = B_y_raw
B_z_lp_raw = B_z_raw
omega_x_prev = 0
omega_y_prev = 0
omega_z_prev = 0
#Dato che applichiamo il filtro complementare ai sensori filtrati. In questo
#caso filtro passa alto e applicato alle velocita angolari, e non 
omega_x_hp_prev = 0
omega_y_hp_prev = 0
omega_z_hp_prev = 0
roll_hp = 0
pitch_hp = 0
yaw_hp = 0
start = time.time()
try:
    while True:
        #Lettura Dati Giroscopio
        omega_raw = L3GD.read()
        #Lettura dati accelerometro e magnetometro
        (G_raw, B_raw) = LSM.read()
        G_x_raw, G_y_raw, G_z_raw = G_raw
        B_x_raw, B_y_raw, B_z_raw = B_raw
        #Correzione Misurazioni Giroscopio
        omega_x_curr = omega_raw[0] - gyro_offset[0]
        omega_y_curr = omega_raw[1] - gyro_offset[1]
        omega_z_curr = omega_raw[2] - gyro_offset[2]
    
        #Calcolo periodo di campionamento e coefficenti di filtro
        delta_time = time.time() - start
        start = time.time()
        #Coefficenti di filtro standard
        alfa_lp_s = float(delta_time)/float((tau_sf+delta_time))
        alfa_hp_s = float(tau_sf)/float((tau_sf + delta_time))
        #Cpeffcente di filtro passa alto
        alfa_hp = float(tau_hp)/float((tau_hp + delta_time))
        #Coefficenti di filtro complementare
        alfa_cf_roll = tau_x/(tau_x + delta_time)
        alfa_cf_pitch = tau_y/(tau_y + delta_time)
        alfa_cf_yaw = tau_z/(tau_z + delta_time)

        ##BLOCCO FILTRO STANDARD(frequenza di taglio f_s)
    
        #Filtro Accelerometro e Magnetometro con filtro passa basso
        G_x_lp_raw = alfa_lp_s*G_x_raw+(1-alfa_lp_s)*G_x_lp_raw
        G_y_lp_raw = alfa_lp_s*G_y_raw+(1-alfa_lp_s)*G_y_lp_raw
        G_z_lp_raw = alfa_lp_s*G_z_raw+(1-alfa_lp_s)*G_z_lp_raw
        B_x_lp_raw = alfa_lp_s*B_x_raw+(1-alfa_lp_s)*B_x_lp_raw
        B_y_lp_raw = alfa_lp_s*B_y_raw+(1-alfa_lp_s)*B_y_lp_raw
        B_z_lp_raw = alfa_lp_s*B_z_raw+(1-alfa_lp_s)*B_z_lp_raw
    
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

        #Computazione roll, pitch e yaw filtro passa basso
        roll_lp = math.atan2(G_y_lp,G_z_lp)    
        pitch_lp = math.atan((-G_x_lp)/math.sqrt(G_y_lp*G_y_lp + G_z_lp*G_z_lp))
        yaw_lp = math.atan2(B_z_lp*math.sin(roll_lp)-B_y_lp*math.cos(roll_lp),(B_x_lp*math.cos(pitch_lp))+(B_y_lp*math.sin(pitch_lp)*math.sin(roll_lp))+(B_z_lp*math.sin(pitch_lp)*math.cos(roll_lp)))

        #Integrazione Numerica
        roll_gyro_curr = roll_gyro_prev + math.radians(omega_x_curr*delta_time)
        pitch_gyro_curr = pitch_gyro_prev + math.radians(omega_y_curr*delta_time)
        yaw_gyro_curr = yaw_gyro_prev + math.radians(omega_z_curr*delta_time)

        #Filtro angoli giroscopio con filtro passa alto
        roll_hp = alfa_hp_s*roll_hp+alfa_hp_s*(roll_gyro_curr-roll_gyro_prev)
        pitch_hp = alfa_hp_s*pitch_hp+alfa_hp_s*(pitch_gyro_curr-pitch_gyro_prev)
        yaw_hp = alfa_hp_s*yaw_hp+alfa_hp_s*(yaw_gyro_curr-yaw_gyro_prev)

        #Uscita Filtro Standard
        roll_sf = roll_lp +roll_hp
        pitch_sf = pitch_lp + roll_hp
        yaw_sf = yaw_lp + yaw_hp
        

        #BLOCCO FILTRO PASSA ALTO ELOCITA ANGOLARE(frequenza di taglio f_hp)        
        #Filtro segnale giroscopio con filtro passa alto
        omega_x_hp = alfa_hp*omega_x_hp_prev+alfa_hp*(omega_x_curr-omega_x_prev)
        omega_y_hp = alfa_hp*omega_y_hp_prev+alfa_hp*(omega_y_curr-omega_y_prev)
        omega_z_hp = alfa_hp*omega_z_hp_prev+alfa_hp*(omega_z_curr-omega_z_prev)



        ##BLOCCO FINALE FILTRO COMPLEMENTARE(frequenze di taglio fc_x, fc_y, fc_z)
        
        #Filtraggio Roll e Pitch-Filtro Complementare
        roll_cf = alfa_cf_roll*(roll_cf_prev+math.radians(omega_x_hp_prev*delta_time))+(1-alfa_cf_roll)*roll_sf
        pitch_cf = alfa_cf_pitch*(pitch_cf_prev+math.radians(omega_y_hp_prev*delta_time))+(1-alfa_cf_pitch)*pitch_sf

        #Filtraggio Yaw-Filtro Complementare
        yaw_cf = alfa_cf_yaw*(yaw_cf_prev+math.radians(omega_z_hp_prev*delta_time))+(1-alfa_cf_yaw)*yaw_sf
        
        roll_cf_prev = roll_cf
        pitch_cf_prev = pitch_cf
        yaw_cf_prev = yaw_cf
        #Calcolo nuova frequenza di taglio
        fc_x = 0.5*np.power(roll_cf_prev,6)+1
        fc_y = 80*np.power(pitch_cf_prev,4)+1
        fc_z = 0.5*np.power(yaw_cf_prev,6)+1
        tau_x = float(1)/(2*3.14*fc_x)
        tau_y = float(1)/(2*3.14*fc_y)
        tau_z = float(1)/(2*3.14*fc_z)

        #Computazione angolo di roll, pitch e yaw(grezzi)
        roll_acc = math.atan2(G_y,G_z)
        pitch_acc = math.atan((-G_x)/math.sqrt(G_y*G_y + G_z*G_z))
        yaw_magn = math.atan2(B_z*math.sin(roll_acc)-B_y*math.cos(roll_acc),(B_x*math.cos(pitch_acc))+(B_y*math.sin(pitch_acc)*math.sin(roll_acc))+(B_z*math.sin(pitch_acc)*math.cos(roll_acc)))

        
        omega_x_curr = omega_x_prev
        omega_y_curr = omega_y_prev
        omega_z_curr = omega_z_prev
        omega_x_hp = omega_x_hp_prev 
        omega_y_hp = omega_y_hp_prev
        omega_z_hp = omega_z_hp_prev

        #Codifico gli angoli su 32bit
        roll_packed = struct.pack("f",roll_cf)
        pitch_packed = struct.pack("f",pitch_cf)
        yaw_packed = struct.pack("f",yaw_cf)
        #Creo il pacchetto finale
        angles_packed = roll_packed + pitch_packed + yaw_packed
        #Invio il pacchetto al server
        my_socket.send(angles_packed)
except KeyboardInterrupt:
    pass
    
my_socket.close()



    

 

    
    

    
