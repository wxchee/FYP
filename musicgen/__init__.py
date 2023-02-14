from time import sleep
import math
from pysinewave import SineWave
import vars


class MusicGen:
    def __init__(self):
        self.sinewave = SineWave(pitch=12, pitch_per_second=5)
    
    def run(self):
        self.sinewave.play()
        i=0
        while True:
            # i = (i+1) % 13
            i = math.floor(vars.sensor.yaw / 15) % 13 # range[0, 12]
            if vars.sensor.yaw >=180 and vars.sensor.yaw < 360:
                i = 12 - i

            print('test music thread {} {}'.format(vars.sensor.yaw, i))
            self.sinewave.set_pitch(i)
            sleep(0.1)