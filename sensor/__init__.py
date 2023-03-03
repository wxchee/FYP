class Sensor:
    def __init__(self):
        self._pitch = 0
        self._roll = 0
        self._yaw = 0
        self._prevYaw = 0
        self._dYaw = 0
        self._sense = None
        try:
            from sense_hat import SenseHat
            self._sense = SenseHat()
        except ModuleNotFoundError:
            print("SenseHat module not found, fallback to fetching remote SenseHat data.")

    @property
    def yaw(self):
        return self._yaw
    
    @property
    def dYaw(self):
        return self._dYaw

    def run(self):
            if self._sense != None:
                while True:
                    orien = self._sense.get_orientation()
                    self.set_orientation(
                        round(orien['pitch']),
                        round(orien['roll']),
                        round(orien['yaw']))
            else:
                from sensor.sensor_receiver import SensorReceiver
                sensorReceiver = SensorReceiver()
                sensorReceiver.run(self.set_orientation)


    def get_orientation(self):
        return (self._pitch, self._roll, self._yaw)

    def set_orientation(self, pitch, roll, yaw):
        self._pitch = int(pitch)
        self._roll = int(roll)
        self._yaw = int(yaw)
        
        self._dYaw = abs(self._prevYaw - self._yaw)
        self._prevYaw = self._yaw

    
