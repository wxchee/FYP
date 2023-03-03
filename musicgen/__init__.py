from time import sleep,time
import math
from pysinewave import SineWave
import vars

C_major = [0, 2, 4, 5, 7, 9, 11, 12]

prev_time = 0
dt = 0
isPlaying = 0
yawCountDown = 0

class MusicGen:
    def __init__(self):
        self.sinewave = SineWave(pitch=12, pitch_per_second=12)
        
    def run(self):
        global yawCountDown, isPlaying, dt, prev_time
        self.sinewave.play()
        isPlaying = 1
        i=0
        angle = 0
        try:
            prev_time = time()
            print('test music thread')
            while True:
                dt = time() - prev_time
                print('dt:{} dYaw:{} dYC: {}'.format(dt, vars.sensor.dYaw, yawCountDown))
                prev_time = time()

                if isPlaying == 1:
                    if (yawCountDown <= 0):
                        self.sinewave.stop()
                        isPlaying = 0
                        yawCountDown = 0
                    else:
                        yawCountDown = yawCountDown - dt
                    
                    #-------- C major scale --------#
                    if (vars.sensor.yaw >= 0 and vars.sensor.yaw < 180):
                        i = math.floor(vars.sensor.yaw / 25.7)
                    else:
                        i = 7 - math.floor((vars.sensor.yaw - 180) / 25.7)
                    print('yaw:{} note:{}'.format(vars.sensor.yaw, i))
                    self.sinewave.set_pitch(C_major[i])
                    sleep(0.05)
                else:
                    if (vars.sensor.dYaw > 1):
                        yawCountDown = 5 if vars.sensor.dYaw > 50 else vars.sensor.dYaw
                        self.sinewave.play()
                        isPlaying = 1
                
                
                
                
                # 0-194 [0,12]
                # 195-359 [11-1]
                # i = math.floor(vars.sensor.yaw / 15) % 13 # range[0, 12]
                # if vars.sensor.yaw >= 195 and vars.sensor.yaw < 360:
                #     i = 11 - i

                # print('test music thread {} {}'.format(vars.sensor.yaw, i))
                # self.sinewave.set_pitch(i)

                # i = (i + 1) % 8
                # self.sinewave.set_pitch(C_major[i])


                # #-------- C major scale --------#
                # if (vars.sensor.yaw >= 0 and vars.sensor.yaw < 180):
                #     i = math.floor(vars.sensor.yaw / 25.7)
                # else:
                #     i = 7 - math.floor((vars.sensor.yaw - 180) / 25.7)
                # print('yaw:{} note:{}'.format(vars.sensor.yaw, i))
                # self.sinewave.set_pitch(C_major[i])
                # sleep(0.05)
        except KeyboardInterrupt:
            print("stop music thread.")