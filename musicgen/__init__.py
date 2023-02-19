from time import sleep
import math
from pysinewave import SineWave
import vars

C_major = [0, 2, 4, 5, 7, 9, 11, 12]

class MusicGen:
    def __init__(self):
        self.sinewave = SineWave(pitch=12, pitch_per_second=12)
    
    def run(self):
        self.sinewave.play()
        i=0
        angle = 0
        try:
            while True:
                # 0-194 [0,12]
                # 195-359 [11-1]
                # i = math.floor(vars.sensor.yaw / 15) % 13 # range[0, 12]
                # if vars.sensor.yaw >= 195 and vars.sensor.yaw < 360:
                #     i = 11 - i

                # print('test music thread {} {}'.format(vars.sensor.yaw, i))
                # self.sinewave.set_pitch(i)

                # i = (i + 1) % 8
                # self.sinewave.set_pitch(C_major[i])


                #-------- C major scale --------#
                if (vars.sensor.yaw >= 0 and vars.sensor.yaw < 180):
                    i = math.floor(vars.sensor.yaw / 25.7)
                else:
                    i = 7 - math.floor((vars.sensor.yaw - 180) / 25.7)
                print('test music thread {} {}'.format(vars.sensor.yaw, i))
                self.sinewave.set_pitch(C_major[i])
                sleep(0.05)
        except KeyboardInterrupt:
            print("stop music thread.")