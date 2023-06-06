import time

def calibrate(gyro):
        print("CALIBRAZIONE GIROSCOPIO")
        print("Sto calcolando l offset, attenzione a non muovere il giroscopio")
        offset_x = 0
        offset_y = 0
        offset_z = 0
        for i in range(5000):
                ang = gyro.read()
                offset_x+=ang[0]
                offset_y+=ang[1]
                offset_z+=ang[2]
        offset_x = offset_x/5000
        offset_y = offset_y/5000
        offset_z = offset_z/5000
        print("Calcolo dell offset terminato, passero allo step successivo tra 3 secondi!!")
        time.sleep(3)
        return(offset_x, offset_y, offset_z)
