import numpy as np
from math import sqrt
from shared import rotMag, rX, rY, rZ, aMag, aDir, aX, aY, aZ

class Sensor:
    def __init__(self):
        self._sense = None
        self._rotMagPool = []
        
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
                self._rotMagPool.append(newRotMag)

                if len(self._rotMagPool) > 4:
                    self._rotMagPool.pop(0)

                rotMag.value = min(10, sum(self._rotMagPool) / len(self._rotMagPool))
                

                # update acceleration data
                aXRaw, aYRaw, aZRaw = self._sense.get_accelerometer_raw().values()
                aMag.value = (aXRaw*aXRaw + aYRaw*aYRaw + aZRaw*aZRaw) ** (1/3)
                aX.value = round(aXRaw, 1)
                aY.value = round(aYRaw, 1)
                aZ.value = round(aZRaw, 1)

                i = -1
                maxAxis = [abs(aXRaw), abs(aYRaw), abs(aZRaw)]
                g1, g2, s = sorted(maxAxis, reverse=True)
                maxI = maxAxis.index(g1)

                if g1 > 0.85:
                    if maxI == 0:
                        i = 1 if aXRaw < 0 else 2
                    elif maxI == 1:
                        i = 3 if aYRaw < 0 else 4
                    elif maxI == 2:
                        i = 5 if aZRaw < 0 else 6
                
                aDir.value = i

        else:
            print('sensor not available')
    
