
# from math import sqrt
import numpy as np

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
                    # orien = self._sense.get_orientation()
                    # self.set_orientation(
                    #     round(orien['pitch']),
                    #     round(orien['roll']),
                    #     round(orien['yaw']))
                    
                    # self.update_ds()

                    # update gyroscope value changed /second
                    gX, gY, gZ = self._sense.get_gyroscope_raw().values()
                    maxI = np.argmax([abs(gX), abs(gY), abs(gZ)])
                    self.rotDir = np.sign([gX,gY,gZ][maxI])
                    self.rotStrength = (gX * gX + gY * gY + gZ * gZ) ** (1/3)


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
    
    
