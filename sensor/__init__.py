import numpy as np
from math import sqrt
from shared import rotMag, aMag, aDir, aX, aY, aZ

class Sensor:
    def __init__(self):
        self._sense = None
        
        self._rotMagList = []
        try:
            from sense_hat import SenseHat
            self._sense = SenseHat()
            self._sense.low_light = True
            self._sense.set_imu_config(False, True, True) # disable magnetometer
        except ModuleNotFoundError:
            print("SenseHat module not found.")

    def run(self):
        if self._sense != None:
            while True:
                gX, gY, gZ = self._sense.get_gyroscope_raw().values()
                self.set_gyro(float(gX),float(gY),float(gZ))
                
                aX, aY, aZ = self._sense.get_accelerometer_raw().values()
                self.set_acc(aX, aY, aZ)

        else:
            print('sensor not available')

    def set_gyro(self, gX, gY, gZ):
        gMags = [abs(gX), abs(gY), abs(gZ)]
        g1, g2, s = sorted(gMags, reverse=True)
        
        rotMagnitude = sqrt(g1 * g1 + g2 * g2)

        self._rotMagList.append(rotMagnitude)

        if len(self._rotMagList) > 4:
            self._rotMagList.pop(0)

        rotMag.value = min(10, sum(self._rotMagList) / len(self._rotMagList))
        
    
    def set_acc(self, x, y, z):
        aMag.value = (x * x + y * y + z * z) ** (1/3)
        
        aX.value = round(x, 1)
        aY.value = round(y, 1)
        aZ.value = round(z, 1)

        i = -1
        if abs(x) > 0.9:
            i = 1 if x < 0 else 2
        elif abs(y) > 0.9:
            i = 3 if y < 0 else 4
        elif abs(z) > 0.9:
            i = 5 if z < 0 else 6
        
        aDir.value = i
    
