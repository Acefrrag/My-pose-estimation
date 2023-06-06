#Questo modulo realizza l interfaccia con il sensore L3G20H della ST Eletronics.
#Il sensore e un giroscopio che restituisce le velocita angolari nella unita di misura gradi/secondo.
#Importazione moduli e pacchetti necessari:
#Imporo il pacchetto smbus per la comunicazione tramite protocollo I2C(Bisogna prima abilitare le rispettive porte all interno della rapberry)
import smbus
#Importo il pacchetto numpy
import numpy as np
#Importo il modulo twos_compl per effettuare il complemento a due
import twos_compl

#VARIABILI SENSORE
#INIDIRIZZO SENSORE GIROSCOPIO
#In base a cosa e collegato il pin SDO del giroscopio, l indirizzo dello stesso varia.
#-L3GD20_address = 0x6B <----SDO collegato all alimentazione(nel mio caso)
#-L3GD20_address = 0x6A <----SDO collegato a massa
#Dato che il modulo dell adafruit utilizzato realizza la connessione all alimentazione del pin in questione l indirizzo sara 6B.
L3GD20H_address = 0x6B
#INDIRIZZI REGISTRI CONTROLLO GIROSCOPIO
#Questi indirizzi sono ai registri del giroscopio mediante i quali avviene, la inizializzazione dello stesso.
L3GD20H_FIFO_CTRL_REG = 0x2e
L3GD20H_CTRL_REG1=0x20
L3GD20H_CTRL_REG2=0x21
L3GD20H_CTRL_REG4=0x23
L3GD20H_CTRL_REG5=0x24
L3GD20H_LOW_ODR=0x39
#VARIABILI DI CONTROLLO GIROSCOPIO
#Queste variabili contengono la sequenze di bit da scrivere negli appositi registri del giroscpio per attivare le varie funzionalita
#AMPIEZZA INTERVALLO VELOCITA ANGOLARI
L3GD20H_range_245dps =0b00000000 #  +/-245dps
L3GD20H_range_500dps =0b00010000 #  +/-500dps
L3GD20H_range_2000dps =0b00100000 # +/- 2000dps
#FREQUENZA DI CAMPIONAMENTO
#Per l impostazione della frequenza bisogna agire su due differenti registri, il LOW_ODR REGISTER e il CTRL1 REGISTER. Si lasciano a 0 i bit relativi a BW.
#Se si abilita il low_speed_bit all interno LOW_ODR:
L3GD20H_LOW_ODR_E = 0b00000001 #<-- Low speed bit abilitato
L3GD20H_12_5Hz = 0b00000000
L3GD20H_25Hz = 0b01000000
L3GD20H_50Hz = 0b10000000
#Se il low_speed_bit e disabilitato:
L3GD20H_LOW_ODR_D = 0b00000000 #<-- Low speed bit disabilitato
L3GD20H_100Hz = 0b00000000
L3GD20H_200Hz = 0b01000000
L3GD20H_400Hz = 0b10000000
L3GD20H_800Hz = 0b11000000
#FREQUENZA DI CUT-OFF(FILTRO PASSA ALTO)
#L effettiva frequenza di taglio dipende dalla frequenza di campionamento settata(vedere datasheet per maggiori dettagli). In ogni caso, il numero ordinario associato alle varie variabili indica l entita del filtraggio.
L3GD20H_10 = 0b00000000 #ALTO IMPATTO
L3GD20H_9 = 0b00000001
L3GD20H_8 = 0b00000010
L3GD20H_7 = 0b00000011
L3GD20H_6 = 0b00000100 #MEDIO ALTO IMPATTO
L3GD20H_5 = 0b00000101 #MEDIO BASSO IMPATTO
L3GD20H_4 = 0b00000110
L3GD20H_3 = 0b00000111
L3GD20H_2 = 0b00001000
L3GD20H_1 = 0b00001001 #BASSO IMPATTO
#REGISTRI DI OUTPUT
#Per velocizzare i tempi di acquisizione si leggono in blocco i dati campionati a partire dal registro con questo indirizzo.
L3GD20H_OUT_X_L=0x28

#DEFINIZIONE CLASSE
#Ho definito una classe che rappresenta il sensore.
#METODI:
#-COSTRUTTORE
#-READ, restituisce una terna di valori interi che rappresentano
#ATTRIBUTI:
#gyr_bus,       contiene una istanza della classe SMBus dal package smbus importato precedentemente;
#address,       contiene l indirizzo del sensore;
#range,         contiene la sequenza di bit da scrivere per impostare un certo intervallo di variazione delle velocita angolari;
#sens,          varia in base al range scelto, e il peso in gradi/sec. di ogni singolo bit.
#fS,            contiene la frequenza di campionamento;
#low_odr        contiene la sequenza per abilitare o meno la low speed output data rate
#cutoff,        contiene la sequenza di bit da scrivere per avere una determinata frequenza di cut-off(filtro passa alto);


class L3GD20H():
        #COSTRUTTORE DELLA CLASSE __init__
        #La classe possiede i seguenti attributi:
        def __init__(self):
                
                self._address = L3GD20H_address
                #Nel mio caso ho abilitato la porta 1 della porta IC della raspberry
                self._gyr_bus = smbus.SMBus(1)
                #Se vuoi cambiare l intervallo di conversione cambia il nome della variabile assegnata all attributo range:
                #L3GD20_range_245dps ---> +/-245dps
                #L3GD20_range_500dps ---> +/-500dps
                #L3GD20_range_2000dps ---> +/-2000dps
                self._range = L3GD20H_range_2000dps
                if self._range == L3GD20H_range_245dps:
                        self._sens = 0.00875
                else:
                        if self._range == L3GD20H_range_500dps:
                                self._sens = 0.0175
                        else:
                                self._sens = 0.07
                #Se vuoi cambiare la frequenza di campionamento, devi cambiare sia la variabile assegnata a fs che a low_odr. Tieni conto associazioni fatte a inizio codice. SE hai dubbi, consulta il datasheet.
                #Possibili valori di low_odr:
                #L3GD20H_LOW_ODR_E
                #L3GD20H_LOW_ODR_D
                #Possibili valori di fs:
                #L3GD20H_12_5Hz
                #L3GD20H_25Hz
                #L3GD20H_50Hz
                #L3GD20H_100Hz
                #L3GD20H_200Hz
                #L3GD20H_400Hz
                #L3GD20H_800Hz
                self._low_odr = L3GD20H_LOW_ODR_D
                self._fs = L3GD20H_400Hz
                #discorso come ai precedenti
                #-L3GD20H_10
                #-L3GD20H_9
                #-L3GD20H_8
                #-L3GD20H_7
                #-L3GD20H_6
                #-L3GD20H_5
                #-L3GD20H_4
                #-L3GD20H_3
                #-L3GD20H_2
                #-L3GD20H_1
                self._cutoff = L3GD20H_10
                #SETTAGGIO REGISTRI
                #Impostazione Intervallo
                self._gyr_bus.write_byte_data(self._address,L3GD20H_CTRL_REG4, 0b00000000 + self._range)
                #Abilitazione FIFO Area
                self._gyr_bus.write_byte_data(self._address,L3GD20H_CTRL_REG5,0b01000000)
                #Abilitazione assi Giroscopio, assi e settaggio frequenza di
                #campionamento e di cut-off
                self._gyr_bus.write_byte_data(self._address,L3GD20H_LOW_ODR,  self._low_odr)
                self._gyr_bus.write_byte_data(self._address,L3GD20H_CTRL_REG1, self._fs + 0b00001111)
                self._gyr_bus.write_byte_data(self._address,L3GD20H_CTRL_REG2, self._cutoff)
                #Impostazione Modalita di Acquisizione
                self._gyr_bus.write_byte_data(self._address,L3GD20H_FIFO_CTRL_REG,0b00010000)             


        #METODO read
        #Il metodo read restiusice le velocita angolari di rotazione attorno
        #ai tre assi solidali al giroscopio.
        def read(self):
                #Leggo la sequenza di 6 byte dai 6 registri del giroscopio
                ang_vel_reading = self._gyr_bus.read_i2c_block_data(self._address,L3GD20H_OUT_X_L+10000000, 6)
                #Compongo coppie di byte tenendo conto che sono in notazione Little Endian
                ang_vel_raw_x = (ang_vel_reading[1] << 8) + ang_vel_reading[0]
                ang_vel_raw_y = (ang_vel_reading[3] << 8) + ang_vel_reading[2]
                ang_vel_raw_z = (ang_vel_reading[5] << 8) + ang_vel_reading[4]
                #Estraggo il numero intero effettuando il complemento a 2
                ang_vel_raw = np.array((twos_compl.twos_comp(ang_vel_raw_x,16), twos_compl.twos_comp(ang_vel_raw_y,16),twos_compl.twos_comp(ang_vel_raw_z,16)),float)
                #Calcolo il valore misurato in gradi/secondo
                ang_vel = ang_vel_raw*self._sens
                return(ang_vel)



                

