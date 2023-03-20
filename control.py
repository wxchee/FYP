
from time import sleep,time
import numpy as np
from math import floor
from musicgen.tools import C_Major


dt = 0
prevTime = time()
i = 0
i_f = 0
dir = 0
dir_predictor = 0

# gyroscope sensitivity +-2000dps = ~ +-34.91radian/s = 0.3491radian/10ms
# 4pi radians = ~720 degrees, fastest the ball can be rotated by a person is about 2 rounds per second

max_radian_per_update = 4 * np.pi

REFRESH_RATE = 0.02 # ~10ms
#


def run(mg, sensor):
    global dt, prevTime, dir, dir_predictor, i, i_f, max_radian_per_second

    while True:
        try:
            # i = math.floor(sensor.yaw / 25.7)
            # i = 7 - (i % 7) if i >= 7 else i
            # mg.set_freq(C_Major[i])

            if sensor.rotStrength > 2:
                mg.set_volume(1)
                dir = get_dir(sensor.rotDir)
                i_f = max(0, min(7, i_f + dir * min(1, sensor.rotStrength / max_radian_per_update)))
                i = floor(i_f)
                mg.set_freq(C_Major[i])
                print('0.4', dir, i_f, sensor.rotStrength, dt)
            elif sensor.rotStrength > 1:
                #  i_f = i
                 mg.set_volume(0.8)
                 print('0.2', dir, i_f, sensor.rotStrength, dt)
            else:
                reset_dir()
                mg.set_volume(0)
                i_f=0


            dt = time() - prevTime
            prevTime = time()
            sleep(REFRESH_RATE)

        except KeyboardInterrupt:
                print("stop music thread.")


def get_dir(curDir):
    global dir_predictor
    LOWER_BOUND = -4
    UPPER_BOUND = 4
    dir_predictor = max(LOWER_BOUND, min(dir_predictor + curDir, UPPER_BOUND))
    
    if dir_predictor < 0:
        return -1
    if dir_predictor > 0:
         return 1
    
    return 0

def reset_dir():
     global dir_predictor
     dir_predictor = 0