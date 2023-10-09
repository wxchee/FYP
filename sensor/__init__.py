import numpy as np
from math import sqrt
from shared import rotMag3D, rX, rY, rZ, aMag, aDir, aX, aY, aZ

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
                # update rotation data
                rXRaw, rYRaw, rZRaw = self._sense.get_gyroscope_raw().values()
                rX.value = round(rXRaw, 3)
                rY.value = round(rYRaw, 3)
                rZ.value = round(rZRaw, 3)

                newRotMag = sqrt(rXRaw*rXRaw + rYRaw*rYRaw + rZRaw*rZRaw) ** (1/3)
                self._rotMagList.append(newRotMag)

                if len(self._rotMagList) > 4:
                    self._rotMagList.pop(0)

                rotMag3D.value = min(10, sum(self._rotMagList) / len(self._rotMagList))
                

                # update acceleration data
                aXRaw, aYRaw, aZRaw = self._sense.get_accelerometer_raw().values()
                aMag.value = (aXRaw*aXRaw + aYRaw*aYRaw + aZRaw*aZRaw) ** (1/3)
                aX.value = round(aXRaw, 1)
                aY.value = round(aYRaw, 1)
                aZ.value = round(aZRaw, 1)

                i = -1
                if abs(aXRaw) > 0.9:
                    i = 1 if aXRaw < 0 else 2
                elif abs(aYRaw) > 0.9:
                    i = 3 if aYRaw < 0 else 4
                elif abs(aZRaw) > 0.9:
                    i = 5 if aZRaw < 0 else 6
                
                aDir.value = i

        else:
            print('sensor not available')
    
