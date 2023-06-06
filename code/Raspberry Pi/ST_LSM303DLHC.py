#Questo modulo realiiza l interfaccia con l integrato LSM303DLHC della ST. Esso consiste in un magnetometro ed un accelerometro. Il magnetometro misura il campo magnetico in Gauss, mentre l accelerometro misura le accelerazioni in g(cioe in 9.81m/s^2). I due sensori hanno due indirizzi I2C differenti quindi costituiscono in realta due slave separati.
#IMPORTAZIONE MODULI E PACKAGE
#Imporo il pacchetto smbus per la comunicazione tramite protocollo I2C(Bisogna prima abilitare le rispettive porte all interno della rapberry)
import smbus
#Importo il pacchetto numpy
import numpy as np
#Importo il modulo twos_compl per effettuare il complemento a due
import twos_compl

#VARIABILI ACCELEROMETRO
#NIDIRIZZO I2C SENSORE
#In base a cosa e collegato il pin SDO dell accelerometro, l indirizzo dello stesso varia.
#-LSM303_ADDRESS_ACCEL = 0x19 <----SDO collegato a VIN(nel mio caso)
#-LSM303_ADDRESS_ACCEL = 0x18 <----SDO collegato a GND
#Dato che il modulo dell adafruit utilizzato realizza la connessione all alimentazione del pin in questione l indirizzo sara 6B.
LSM303_ADDRESS_ACCEL = 0x19
#INDIRIZZI REGISTRI CONTROLLO
#Questi indirizzi sono ai registri dell accelerometro mediante i quali avviene, la inizializzazione dello stesso.
LSM303_REGISTER_ACCEL_CTRL_REG1_A = 0x20    
LSM303_REGISTER_ACCEL_CTRL_REG4_A = 0x23
LSM303_REGISTER_ACCEL_OUT_X_L_A   = 0x28
#VARIABILI DI CONTROLLO
#Impostazioni Intervallo
LSM303_ACCGAIN_2g = 0b00000000   # +/- 2g
LSM303_ACCGAIN_4g = 0b00010000   # +/- 4g
LSM303_ACCGAIN_8g = 0b00100000   # +/- 8g
LSM303_ACCGAIN_16g = 0b00110000  # +/- 16g
#Impostazioni ODR(Output Data Rate)
#Il datasheet fornisce anche la BW(larghezza di banda del segnale) associata alle varie ODR, che varia anche essa in funzione della modalita di consumo scelta
LSM303_ACCODR_1HZ = 0b00000000
LSM303_ACCODR_10HZ = 0b00010000
LSM303_ACCODR_25HZ = 0b00110000
LSM303_ACCODR_50HZ = 0b01000000
LSM303_ACCODR_100HZ = 0b01010000
LSM303_ACCODR_200HZ = 0b01100000
LSM303_ACCODR_400HZ = 0b01110000
LSM303_ACCODR_1620HZ = 0b10000000 #Disponibile solo per la modalita low-power mode
LSM303_ACCODR_1344_5376HZ = 0b100010000 #La frequenza varia in base alla modalita di consumo scelta(vedi datasheet)
#VARIABILI MAGNETOMETRO
#INDIRIZZO I2C SENSORE
#In base a cosa e collegato il pin SDO del magnetometro, l indirizzo dello stesso varia.
#-LSM303_ADDRESS_MAG = 0x1e <----SDO collegato a  VIN(nel mio caso)
#-LSM303_ADDRESS_MAG = 0x1d <----SDO collegato a GND
LSM303_ADDRESS_MAG = 0x1e
#INDIRIZZI REGISTRI CONTROLLO
LSM303_REGISTER_MAG_CRA_REG_M     = 0x00
LSM303_REGISTER_MAG_CRB_REG_M     = 0x01
LSM303_REGISTER_MAG_MR_REG_M      = 0x02
LSM303_REGISTER_MAG_OUT_X_H_M     = 0x03
#Impostazioni Intervallo
LSM303_MAGGAIN_1_3 = 0x20 # +/- 1.3gauss
LSM303_MAGGAIN_1_9 = 0x40 # +/- 1.9gauss
LSM303_MAGGAIN_2_5 = 0x60 # +/- 2.5gauss
LSM303_MAGGAIN_4_0 = 0x80 # +/- 4.0gauss
LSM303_MAGGAIN_4_7 = 0xA0 # +/- 4.7gauss
LSM303_MAGGAIN_5_6 = 0xC0 # +/- 5.6gauss
LSM303_MAGGAIN_8_1 = 0xE0 # +/- 8.1gauss
#Impostazioni ODR(Output Data Rate)
LSM303_MAGODR_0_75HZ = 0b00000000
LSM303_MAGODR_1_5HZ = 0b00000100
LSM303_MAGODR_3HZ = 0b00001000
LSM303_MAGODR_7_5HZ = 0b00001100
LSM303_MAGODR_15HZ = 0b00010000
LSM303_MAGODR_30HZ = 0b00010100
LSM303_MAGODR_75HZ = 0b00011000
LSM303_MAGODR_220HZ = 0b00011100
#Nota Lavoro:
#1):
##Ricorda che la frequenza di campionamento effettiva dipende in ultima istanza dalla MCU!!!
#2)
#Mentre il primo registro dei dati campionati dall accelerometro contiene il
#byte meno significativo della coppia di byte relativi alla misuraizone,
#quello del magnetometro quello piu significativo. Quindi l accoppiamento dei
#byte deve avvenire in modo diverso(Per l accelerometro ho una notazione Little
#Endian, per il magnetometro Big Endian).




class LSM303():
    def __init__(self):
        #INDIRIZZI I2C SENSORI E ISTANZA SMBus
        self._acc_address = LSM303_ADDRESS_ACCEL
        self._mag_address = LSM303_ADDRESS_MAG
        self._LSM303_bus = smbus.SMBus(1)
        #ACCELEROMETRO
        #INTERVALLO
        #Se vuoi cambiare l intervallo di variazione massimo dell accelerazione misurabile, cambia il nome della variabile assegnata all attributo acc_range.      
        # - LSM303_ACCGAIN_2g = +/- 2g
        # - LSM303_ACCGAIN_4g = +/- 4g
        # - LSM303_ACCGAIN_8g = +/- 8g
        # - LSM303_ACCGAIN_16g = +/- 16g
        self._acc_range = LSM303_ACCGAIN_2g
        #SENSIBILITA: Peso in g per unita, g/bit
        if self._acc_range == LSM303_ACCGAIN_2g:
            self._acc_sens = float(1)/1000
        else:
            if self._acc_range == LSM303_ACCGAIN_4g:
                self._acc_sens = float(2)/1000
            else:
                if self._acc_range == LSM303_ACCGAIN_8g:
                    self._acc_sens = float(4)/1000
                else:
                    self._acc_sens = float(12)/1000
        #ODR(Output Data Rate)
        #Se vuoi cambiare la frequenza di campionamento, cambia il nome della variabile assegnata all attributo acc_odr
        #-LSM303_ACCODR_1HZ
        #LSM303_ACCODR_10HZ
        #LSM303_ACCODR_25HZ
        #LSM303_ACCODR_50HZ
        #LSM303_ACCODR_100HZ
        #LSM303_ACCODR_200HZ
        #LSM303_ACCODR_400HZ
        #LSM303_ACCODR_1620HZ
        #LSM303_ACCODR_1344_5376HZ
        self._acc_odr = LSM303_ACCODR_400HZ
        #MODALITA DI RISOLUZIONE
        #Seleziono la modalita di risoluzione:
        #-high-resolution, la misurazione e composta da 12 bit
        #-low-resolution, la misurazione e composta da soli 10 bit, garantisce una maggiore frequenza di camionamento del sensore e minore consumo di corrente
        #-hi-res = True
        #-hi-res = False
        hi_res = True
        self._hi_res = hi_res
        if self._hi_res == True:
            #Abilito la normal mode
            self._power_mode = 0b00000000
            #Abilito la high-resolution mode
            self._res = 0b00001000
        else:
            self._power_mode = 0b00001000
            self._res = 0b00001000
        #IMPOSTAZIONE REGISTRI ACCELEROMETRO
        #Abilito l Accelerometro, seleziono la low o normal power mode, e setto la frequenza di campionamento
        self._LSM303_bus.write_byte_data(self._acc_address,LSM303_REGISTER_ACCEL_CTRL_REG1_A, 0b00000111+self._power_mode+self._acc_odr)
        #Seleziono low o hih resolution
        self._LSM303_bus.write_byte_data(self._acc_address,LSM303_REGISTER_ACCEL_CTRL_REG4_A, self._res+self._acc_range)

        #MAGNETOMETRO
        #INTERVALLO
        #Se vuoi cambiare l intervallo del campo magnetico misurabie cambia la variabile assegnata
        # - LSM303_MAGGAIN_1_3 = +/- 1.3
        # - LSM303_MAGGAIN_1_9 = +/- 1.9
        # - LSM303_MAGGAIN_2_5 = +/- 2.5
        # - LSM303_MAGGAIN_4_0 = +/- 4.0
        # - LSM303_MAGGAIN_4_7 = +/- 4.7
        # - LSM303_MAGGAIN_5_6 = +/- 5.6
        # - LSM303_MAGGAIN_8_1 = +/- 8.1
        self._mag_range = LSM303_MAGGAIN_1_3
        #SENSIBILITA
        if self._mag_range == LSM303_MAGGAIN_1_3:
            self._mag_sens_xy = float(1)/1100
            self._mag_sens_z = float(1)/980
        else:
            if self._mag_range == LSM303_MAGGAIN_1_9:
                self._mag_sens_xy = float(1)/855
                self._mag_sens_z = float(1)/760
            else:
                if self._mag_range == LSM303_MAGGAIN_2_5:
                    self._mag_sens_xy = float(1)/670
                    self._mag_sens_z = float(1)/600
                else:
                    if self._mag_range == LSM303_MAGGAIN_4_0:
                        self._mag_sens_xy = float(1)/450
                        self._mag_sens_z = float(1)/400
                    else:
                        if self._mag_range == LSM303_MAGGAIN_4_7:
                            self._mag_sens_xy = float(1)/400
                            self._mag_sens_z = float(1)/355
                        else:
                            if self._mag_range == LSM303_MAGGAIN_5_6:
                                self._mag_sens_xy = float(1)/330
                                self._mag_sens_z = float(1)/295
                            else:
                                self._mag_sens_xy = float(1)/230
                                self._mag_sens_z = float(1)/205
        #ODR(Output Data Rate)
        #Se vuoi cambiare la frequenza di campionamento, cambia il nome della variabile assegnata all attributo mag_odr
        #LSM303_MAGODR_0_75HZ
        #LSM303_MAGODR_1_5HZ
        #LSM303_MAGODR_3HZ
        #LSM303_MAGODR_7_5HZ
        #LSM303_MAGODR_15HZ
        #LSM303_MAGODR_30HZ
        #LSM303_MAGODR_75HZ
        #LSM303_MAGODR_220HZ
        self._mag_odr = LSM303_MAGODR_220HZ
        #IMPOSTAZIONE REGISTRI
        #Abilitazione Magnetometro 
        self._LSM303_bus.write_byte_data(self._mag_address,LSM303_REGISTER_MAG_MR_REG_M, 0x00)
        #Impostazione Intervallo
        self._LSM303_bus.write_byte_data(self._mag_address,LSM303_REGISTER_MAG_CRB_REG_M, self._mag_range)
        #Impostazione ODR
        self._LSM303_bus.write_byte_data(self._mag_address,LSM303_REGISTER_MAG_CRB_REG_M, self._mag_odr)
    def read(self):
        #Lettura Registri Output Accelerometro
        acc_reading = self._LSM303_bus.read_i2c_block_data(self._acc_address, 0b10000000 + LSM303_REGISTER_ACCEL_OUT_X_L_A, 6)
        #Composizione dei byte tenendo conto che si e in notazione Little Endian
        acc_raw_x = (acc_reading[1] << 8) + acc_reading[0]
        acc_raw_y = (acc_reading[3] << 8) + acc_reading[2]
        acc_raw_z = (acc_reading[5] << 8) + acc_reading[4]
        #Shifto i bit inutlizzati:
        #Il sensore non utilizza in realta tutti e 16 i bit a dispoisizione, ma 12bit oppure 10 secondo i casi. In particolare non utilizza quelli meno significativi.
        #CASO hi_res = True, commentare se si vuole disabilitare l alta risoluzione
        acc_raw_x = acc_raw_x >> 4
        acc_raw_y = acc_raw_y >> 4
        acc_raw_z = acc_raw_z >> 4
        #CASO hi_res = False, commentare se si vuole disabilitare l alta risoluzione
        #acc_raw_x = acc_raw_x >> 6
        #acc_raw_y = acc_raw_y >> 6
        #acc_raw_z = acc_raw_z >> 6
        #Estraggo i numeri interi effettuando il complemento a 2
        acc_raw = np.array((twos_compl.twos_comp(acc_raw_x, 12),twos_compl.twos_comp(acc_raw_y, 12),twos_compl.twos_comp(acc_raw_z, 12)),int)
        #Calcolo il vettore accelerazione in g
        acc = acc_raw*self._acc_sens
        
        #Lettura Registri Output del magnetometro
        mag_reading = self._LSM303_bus.read_i2c_block_data(self._mag_address,0b10000000+LSM303_REGISTER_MAG_OUT_X_H_M, 6)
        #In questo caso abbiamo una notazione Big Endian, quindi la composizione delle coppie di byte avviene in modo diverso
        mag_raw_x = (mag_reading[0] << 8) + mag_reading[1]
        mag_raw_z = (mag_reading[2] << 8) + mag_reading[3]
        mag_raw_y = (mag_reading[4] << 8) + mag_reading[5]
        #Estraggo i numeri interi effettuando il complemento a 2
        mag_raw = np.array((twos_compl.twos_comp(mag_raw_x, 16),twos_compl.twos_comp(mag_raw_y, 16),twos_compl.twos_comp(mag_raw_z, 16)),int)
        #Calcolo il vettore compo magnetico in gauss
        mag = np.array((mag_raw[0]*self._mag_sens_xy,mag_raw[1]*self._mag_sens_xy,mag_raw[2]*self._mag_sens_z),float)
        
        return (acc, mag)
