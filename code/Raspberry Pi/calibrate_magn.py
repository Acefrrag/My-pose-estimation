import time



f_c = 1
tau = float(1)/float(2*3.14*f_c)
#CALIBRATION_TIMEOUT:
#Questo e il massimo intervallo di tempo in secondi che puo intercorrere dall ultimo rilevamento di massimo o minimo del campo magnetico lungo uno qualsiasi dei 3 assi del magnetometro.
#I numeri che vengono stampati indicano quando tempo e passato dall ultimo rilevamento di punto di inversione.
CALIBRATION_TIMEOUT = 10
def calibrate(LSM):
        print("CALIBRAZIONE MAGNETOMETRO")
        print("Tra tre secondi inizio la calibrazione del magnetometro.")
        time.sleep(3)
        offset_x = 0
        offset_y = 0
        offset_z = 0
        B_x_min = 10000
        B_x_max = -10000
        B_y_min = 10000
        B_y_max = -10000
        B_z_min = 10000
        B_z_max = -10000
        changed = False
        istantlastchange = time.time()
        delta_time = 0
        print("Posiziona il sensore parallelamente alla superficie terrestre. Premi invio quando sei pronto a ruotare il dispositivo attorno all asse z")
        a = input()
        #Inizializzo valore filtrato
        (G_raw, B_raw) = LSM.read()
        B_x, B_y, B_z = B_raw
        B_x_lp = B_x
        B_y_lp = B_y
        B_z_lp = B_z
        start_sampling = time.time()
        while (delta_time) <= CALIBRATION_TIMEOUT:
                (G_raw, B_raw) = LSM.read()
                B_x, B_y, B_z = B_raw
                sampling_time = time.time() - start_sampling
                start_sampling = time.time()
                #Calcolo coefficente di filtraggio
                alfa_lp = float(sampling_time)/float((tau+sampling_time))
                #Filtraggio Dati
                B_x_lp = alfa_lp*B_x+(1-alfa_lp)*B_x_lp
                B_y_lp = alfa_lp*B_y+(1-alfa_lp)*B_y_lp
                B_z_lp = alfa_lp*B_z+(1-alfa_lp)*B_z_lp
                if B_x < B_x_min:
                    changed = True
                    B_x_min = B_x
                if B_x > B_x_max:
                    changed = True
                    B_x_max = B_x                    
                if B_y < B_y_min:
                    changed = True
                    B_y_min = B_y
                if B_y > B_y_max:
                    changed = True
                    B_y_max = B_y
                if changed:
                    istantlastchange = time.time()
                changed = False
                delta_time = time.time() - istantlastchange
                print(delta_time)
        print("Ho raccolto abbastanza dati. Riposiziona il dispositivo come all inizio e premi invio quando sei pronto a ruotare il sensore atttorno all asse x.")
        a = input()
        changed = False
        istantlastchange = time.time()
        delta_time = 0
        #Inizializzo valore filtrato
        (G_raw, B_raw) = LSM.read()
        B_x, B_y, B_z = B_raw
        B_x_lp = B_x
        B_y_lp = B_y
        B_z_lp = B_z
        start_sampling = time.time()
        while (delta_time <= CALIBRATION_TIMEOUT):
                (G_raw, B_raw) = LSM.read()
                B_x, B_y, B_z = B_raw
                sampling_time = time.time() - start_sampling
                start_sampling = time.time()
                #Calcolo coefficente di filtraggio
                alfa_lp = float(sampling_time)/float((tau+sampling_time))
                #Filtraggio Dati
                B_x_lp = alfa_lp*B_x+(1-alfa_lp)*B_x_lp
                B_y_lp = alfa_lp*B_y+(1-alfa_lp)*B_y_lp
                B_z_lp = alfa_lp*B_z+(1-alfa_lp)*B_z_lp
                if B_y < B_y_min:
                    changed = True
                    B_y_min = B_y
                if B_y > B_y_max:
                    changed = True
                    B_y_max = B_y
                if B_z < B_z_min:
                    changed = True
                    B_z_min = B_z
                if B_z > B_z_max:
                    changed = True
                    B_z_max = B_z
                if changed:
                    istantlastchange = time.time()
                changed = False
                delta_time = time.time() - istantlastchange
                print(delta_time)
        print("Ho raccolto abbastanza dati. Riposiziona il dispositivo come all inizio e premi invio quando sei pronto a ruotare il sensore atttorno all asse y.")
        a = input()
        changed = False
        istantlastchange = time.time()
        delta_time = 0
        #Inizializzo valore filtrato
        (G_raw, B_raw) = LSM.read()
        B_x, B_y, B_z = B_raw
        B_x_lp = B_x
        B_y_lp = B_y
        B_z_lp = B_z
        start_sampling = time.time()
        while (delta_time <= CALIBRATION_TIMEOUT):
                (G_raw, B_raw) = LSM.read()
                B_x, B_y, B_z = B_raw
                sampling_time = time.time() - start_sampling
                start_sampling = time.time()
                #Calcolo coefficente di filtraggio
                alfa_lp = float(sampling_time)/float((tau+sampling_time))
                #Filtraggio Dati
                B_x_lp = alfa_lp*B_x+(1-alfa_lp)*B_x_lp
                B_y_lp = alfa_lp*B_y+(1-alfa_lp)*B_y_lp
                B_z_lp = alfa_lp*B_z+(1-alfa_lp)*B_z_lp
                if B_x < B_x_min:
                    changed = True
                    B_x_min = B_x
                if B_x > B_x_max:
                    changed = True
                    B_x_max = B_x
                if B_z < B_z_min:
                    changed = True
                    B_z_min = B_z
                if B_z > B_z_max:
                    changed = True
                    B_z_max = B_z
                if changed:
                    istantlastchange = time.time()
                changed = False
                delta_time = time.time() - istantlastchange
                print(delta_time)
        offset_x = (B_x_min + B_x_max)/2
        offset_y = (B_y_min + B_y_max)/2
        offset_z = (B_z_min + B_z_max)/2
        print("Calibrazione terminate, passero allo step successivo tra 3 secondi")
        time.sleep(3)
        return(offset_x, offset_y, offset_z)
