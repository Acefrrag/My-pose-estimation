import time
f_c = 1
tau = float(1)/float(2*3.14*f_c)
#CALIBRATION_TIMEOUT:
#Questo e il massimo intervallo di tempo in secondi che puo intercorrere dall ultimo rilevamento di massimo o minimo del vettore g lungo uno qualsiasi dei 3 assi dell accelerometro.
#I numeri che vengono stampati indicano quando tempo e passato dall ultimo rilevamento di punto di inversione
CALIBRATION_TIMEOUT = 5
def calibrate(LSM):
        print("CALIBRAZIONE ACCELEROMETRO")
        print("Tra tre secondi inizio la calibrazione dell accelerometro.")
        time.sleep(3)
        print("Negl intervallo di tempo in ci raccolgo i dati, attenzione a non muovere BRUSCAMENTE l accelerometro")
        time.sleep(3)
        offset_x = 0
        offset_y = 0
        offset_z = 0
        G_x_min = 10000
        G_x_max = -10000
        G_y_min = 10000
        G_y_max = -10000
        G_z_min = 10000
        G_z_max = -10000
        changed = False
        istantlastchange = time.time()
        delta_time = 0
        print("Posiziona l accelerometro in modo che l asse z sia parallelo concorde al vettore accelerazione di gravita. Premi invio quando sei pronto.")
        a = input()
        #Inizializzo valore filtrato
        (G_raw, B_raw) = LSM.read()
        G_x, G_y, G_z = G_raw
        G_x_lp = G_x
        G_y_lp = G_y
        G_z_lp = G_z
        start_sampling = time.time()
        while (delta_time) <= CALIBRATION_TIMEOUT:
                (G_raw, B_raw) = LSM.read()
                G_x, G_y, G_z = G_raw
                sampling_time = time.time() - start_sampling
                start_sampling = time.time()
                #Calcolo coefficente di filtraggio
                alfa_lp = float(sampling_time)/float((tau+sampling_time))
                #Filtraggio Dati
                G_z_lp = alfa_lp*G_z+(1-alfa_lp)*G_z_lp
                if G_z_lp < G_z_min:
                    changed = True
                    G_z_min = G_z_lp
                if G_z_lp > G_z_max:
                    changed = True
                    G_z_max = G_z_lp
                if changed:
                    istantlastchange = time.time()
                changed = False
                delta_time = time.time() - istantlastchange
                print(delta_time)
        print("Ho raccolto abbastanza dati.")
        print("Posiziona l accelerometro in modo che l asse z sia parallelo discorde al vettore g. Premi invio quando sei pronto.")
        a = input()
        changed = False
        istantlastchange = time.time()
        delta_time = 0
        #Inizializzo valore filtrato
        (G_raw, B_raw) = LSM.read()
        G_x, G_y, G_z = G_raw
        G_x_lp = G_x
        G_y_lp = G_y
        G_z_lp = G_z
        start_sampling = time.time()
        while (delta_time) <= CALIBRATION_TIMEOUT:
                (G_raw, B_raw) = LSM.read()
                G_x, G_y, G_z = G_raw
                sampling_time = time.time() - start_sampling
                start_sampling = time.time()
                #Calcolo coefficente di filtraggio
                alfa_lp = float(sampling_time)/float((tau+sampling_time))
                #Filtraggio Dati
                G_z_lp = alfa_lp*G_z+(1-alfa_lp)*G_z_lp
                if G_z_lp < G_z_min:
                    changed = True
                    G_z_min = G_z_lp
                if G_z_lp > G_z_max:
                    changed = True
                    G_z_max = G_z_lp
                if changed:
                    istantlastchange = time.time()
                changed = False
                delta_time = time.time() - istantlastchange
                print(delta_time)
        print("Ho raccolto abbastanza dati.")
        print("Posiziona l accelerometro in modo che l asse y sia parallelo concorde al vettore g. Premi invio quando sei pronto.")
        a = input()
        changed = False
        istantlastchange = time.time()
        delta_time = 0
        #Inizializzo valore filtrato
        (G_raw, B_raw) = LSM.read()
        G_x, G_y, G_z = G_raw
        G_x_lp = G_x
        G_y_lp = G_y
        G_z_lp = G_z
        start_sampling = time.time()
        while (delta_time) <= CALIBRATION_TIMEOUT:
                (G_raw, B_raw) = LSM.read()
                G_x, G_y, G_z = G_raw
                sampling_time = time.time() - start_sampling
                start_sampling = time.time()
                #Calcolo coefficente di filtraggio
                alfa_lp = float(sampling_time)/float((tau+sampling_time))
                #Filtraggio Dati
                G_y_lp = alfa_lp*G_y+(1-alfa_lp)*G_y_lp
                if G_y_lp < G_y_min:
                    changed = True
                    G_y_min = G_y_lp
                if G_y_lp > G_y_max:
                    changed = True
                    G_y_max = G_y_lp
                if changed:
                    istantlastchange = time.time()
                changed = False
                delta_time = time.time() - istantlastchange
                print(delta_time)
        print("Ho raccolto abbastanza dati.")
        print("Posiziona l accelerometro in modo che l asse y sia parallelo discorde al vettore g. Premi invio quando sei pronto.")
        a = input()
        changed = False
        istantlastchange = time.time()
        delta_time = 0
        #Inizializzo valore filtrato
        (G_raw, B_raw) = LSM.read()
        G_x, G_y, G_z = G_raw
        G_x_lp = G_x
        G_y_lp = G_y
        G_z_lp = G_z
        start_sampling = time.time()
        while (delta_time) <= CALIBRATION_TIMEOUT:
                (G_raw, B_raw) = LSM.read()
                G_x, G_y, G_z = G_raw
                sampling_time = time.time() - start_sampling
                start_sampling = time.time()
                #Calcolo coefficente di filtraggio
                alfa_lp = float(sampling_time)/float((tau+sampling_time))
                #Filtraggio Dati
                G_y_lp = alfa_lp*G_y+(1-alfa_lp)*G_y_lp
                if G_y_lp < G_y_min:
                    changed = True
                    G_y_min = G_y_lp
                if G_y_lp > G_y_max:
                    changed = True
                    G_y_max = G_y_lp
                if changed:
                    istantlastchange = time.time()
                changed = False
                delta_time = time.time() - istantlastchange
                print(delta_time)
        print("Ho raccolto abbastanza dati.")
        print("Posiziona l accelerometro in modo che l asse x sia parallelo concorde al vettore g. Premi invio quando sei pronto.")
        a = input()
        changed = False
        istantlastchange = time.time()
        delta_time = 0
        #Inizializzo valore filtrato
        (G_raw, B_raw) = LSM.read()
        G_x, G_y, G_z = G_raw
        G_x_lp = G_x
        G_y_lp = G_y
        G_z_lp = G_z
        start_sampling = time.time()
        while (delta_time) <= CALIBRATION_TIMEOUT:
                (G_raw, B_raw) = LSM.read()
                G_x, G_y, G_z = G_raw
                sampling_time = time.time() - start_sampling
                start_sampling = time.time()
                #Calcolo coefficente di filtraggio
                alfa_lp = float(sampling_time)/float((tau+sampling_time))
                #Filtraggio Dati
                G_x_lp = alfa_lp*G_x+(1-alfa_lp)*G_x_lp
                if G_x_lp < G_x_min:
                    changed = True
                    G_x_min = G_x_lp
                if G_x_lp > G_x_max:
                    changed = True
                    G_x_max = G_x_lp
                if changed:
                    istantlastchange = time.time()
                changed = False
                delta_time = time.time() - istantlastchange
                print(delta_time)
        print("Ho raccolto abbastanza dati.")
        print("Posiziona l accelerometro in modo che l asse x sia parallelo discorde al vettore g. Premi invio quando sei pronto.")
        a = input()
        changed = False
        istantlastchange = time.time()
        delta_time = 0
        #Inizializzo valore filtrato
        (G_raw, B_raw) = LSM.read()
        G_x, G_y, G_z = G_raw
        G_x_lp = G_x
        G_y_lp = G_y
        G_z_lp = G_z
        start_sampling = time.time()
        while (delta_time) <= CALIBRATION_TIMEOUT:
                (G_raw, B_raw) = LSM.read()
                G_x, G_y, G_z = G_raw
                sampling_time = time.time() - start_sampling
                start_sampling = time.time()
                #Calcolo coefficente di filtraggio
                alfa_lp = float(sampling_time)/float((tau+sampling_time))
                #Filtraggio Dati
                G_x_lp = alfa_lp*G_x+(1-alfa_lp)*G_x_lp
                if G_x_lp < G_x_min:
                    changed = True
                    G_x_min = G_x_lp
                if G_x_lp > G_x_max:
                    changed = True
                    G_x_max = G_x_lp
                if changed:
                    istantlastchange = time.time()
                changed = False
                delta_time = time.time() - istantlastchange
                print(delta_time)
        print("Ho raccolto abbastanza dati.")
        offset_x = (G_x_min + G_x_max)/2
        offset_y = (G_y_min + G_y_max)/2
        offset_z = (G_z_min + G_z_max)/2
        print("Calibrazione terminate, passero allo step successivo tra 3 secondi")
        time.sleep(3)
        return(offset_x, offset_y, offset_z)
