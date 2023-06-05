import math
import numpy as np
from math import copysign, sqrt
class Sensor:
    def __init__(self):
        self._pitch = 0
        self._roll = 0
        self._yaw = 0

        self.rotDir = 0
        self.rotStrength = 0 # magnitude of gyroscope(in radian) combining all three axis

        self.accStrength = 0

        self._sense = None
        try:
            from sense_hat import SenseHat
            self._sense = SenseHat()
            self._sense.low_light = True
            self._sense.set_imu_config(False, True, True)
        except ModuleNotFoundError:
            print("SenseHat module not found, fallback to fetching remote SenseHat data.")

    @property
    def yaw(self):
        return self._yaw
    
    @property 
    def pitch(self):
        return self._pitch
    
    @property 
    def roll(self):
        return self._roll
    
    @property
    def ds(self):
        return self._ds

    def run(self):
            if self._sense != None:
                while True:
                    orien = self._sense.get_orientation()
                    self.set_orientation(
                        round(orien['pitch']),
                        round(orien['roll']),
                        round(orien['yaw']))
                    
                    # self.update_ds()

                    # update gyroscope value changed /second
                    gX, gY, gZ = self._sense.get_gyroscope_raw().values()
                    gMags = [abs(gX), abs(gY), abs(gZ)]
                    g1, g2, s = sorted(gMags, reverse=True)
                    i1 = gMags.index(g1)
                    # i2 = gMags.index(g2)
                    # maxI = np.argmax(gMags)
                    # self.rotDir = np.sign([gX,gY,gZ][maxI])
                    self.rotDir = copysign(1, [gX, gY, gX][i1])
                    self.rotStrength = sqrt(g1 * g1 + g2 * g2)
                    # self.rotStrength = (gX * gX + gY * gY + gZ * gZ) ** (1/3)
                    # print(i1,":",g1,"|", i2, ":",g2, "   ", gX, gY, gZ)
                    # print(self.rotDir, self.rotStrength)
                    # if (self.rotStrength > 2):
                    #     print(i1, self.rotDir, self.rotStrength)
                    #     print('x', gX, 'y', gY, 'z', gZ)

                    # print(self.get_dir_rot(gX, gY, gZ))

                    aX, aY, aZ = self._sense.get_accelerometer_raw().values()
                    self.accStrength = (aX * aX + aY * aY + aZ * aZ) ** (1/3)
                    
                    gds = (abs(gX) + abs(gY) + abs(gX)) / 21 # even out three axis, empirical max gyro change ~7 thus 3*7=21
                    gds = round(min(gds, 1), 3)

            else:
                from sensor.sensor_receiver import SensorReceiver
                sensorReceiver = SensorReceiver()
                sensorReceiver.run(self.set_orientation)


    def get_orientation(self):
        return (self._pitch, self._roll, self._yaw)

    def set_orientation(self, pitch, roll, yaw):
        self._pitch = int(pitch) % 360
        self._roll = int(roll) % 360
        self._yaw = int(yaw) % 360
    
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
    
