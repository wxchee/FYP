import math
import numpy as np
from math import copysign, sqrt
from shared import rotDir, rotMag, aMag, aX, aY, aZ, yaw
from time import time

class Sensor:
    def __init__(self):
        self._sense = None
        self._dt = 0
        self._prevTime = 0
        self._rotMagList = []
        try:
            from sense_hat import SenseHat
            self._sense = SenseHat()
            self._sense.low_light = True
            self._sense.set_imu_config(False, True, True)
        except ModuleNotFoundError:
            print("SenseHat module not found, fallback to fetching remote SenseHat data.")

    def run(self):
        self._prevTime = time()
        if self._sense != None:
            while True:
                gX, gY, gZ = self._sense.get_gyroscope_raw().values()
                self.set_gyro(float(gX),float(gY),float(gZ))

                # orien = self._sense.get_orientation()
                # self.set_orientation(orien['pitch'], orien['roll'], orien['yaw'])
                
                aX, aY, aZ = self._sense.get_accelerometer_raw().values()
                self.set_acc(aX, aY, aZ)
                print('sensor run')

        else:
            from sensor.sensor_receiver import SensorReceiver
            sensorReceiver = SensorReceiver()
            sensorReceiver.run(self.set_gyro, self.set_acc)


    def set_gyro(self, gX, gY, gZ):
        global yaw
        self._dt = time() - self._prevTime

        newZ = yaw.value + (gZ * self._dt) / np.pi * 180
        if (newZ < 0):
            yaw.value = 360 + newZ
        elif newZ > 360:
            yaw.value = newZ - 360
        else:
            yaw.value = newZ
            
        gMags = [abs(gX), abs(gY), abs(gZ)]
        g1, g2, s = sorted(gMags, reverse=True)
        i1 = gMags.index(g1)

        rotDir.value = int(copysign(1, [gX, gY, gX][i1]))
        rotMagnitude = sqrt(g1 * g1 + g2 * g2)

        self._rotMagList.append(rotMagnitude)

        if len(self._rotMagList) > 4:
            self._rotMagList.pop(0)

        rotMag.value = min(5, sum(self._rotMagList) / len(self._rotMagList))
        
        self._prevTime = time()
    
    def set_acc(self, x, y, z):
        aMag.value = (x * x + y * y + z * z) ** (1/3)
        aX.value = round(x, 2)
        aY.value = round(y, 2)
        aZ.value = round(z, 2)

    # def set_orientation(self, p, r, y):
    #     pitch.value = int(p) % 360
    #     roll.value = int(r) % 360
    #     yaw.value = int(y) % 360

        # update gyroscope value changed /second
        # gX, gY, gZ = self._sense.get_gyroscope_raw().values()

        # aX, aY, aZ = self._sense.get_accelerometer_raw().values()
        
    
    def get_dir_rot(self, gX, gY, gZ):
        direction_of_rotation_vector = [gY, -gX, 0]  # Assuming Sense HAT is mounted in landscape orientation

        # Normalize the direction of rotation vector
        magnitude = (direction_of_rotation_vector[0]**2 + direction_of_rotation_vector[1]**2 + direction_of_rotation_vector[2]**2) ** (1/3)
        direction_of_rotation_vector = [direction_of_rotation_vector[0]/magnitude, direction_of_rotation_vector[1]/magnitude, direction_of_rotation_vector[2]/magnitude]

        # Calculate the dot product of the rotation vector and the direction of rotation vector
        dot_product = gX * direction_of_rotation_vector[0] + gY * direction_of_rotation_vector[1] + gZ * direction_of_rotation_vector[2]

        # Calculate the rotation angle around the direction of rotation
        rotation_angle = math.acos(dot_product)

        # Convert the rotation angle from radians to degrees
        return math.degrees(rotation_angle)
    
