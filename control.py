
from time import sleep,time
import numpy as np
from math import floor, ceil, copysign
from musicgen.tools import C_Major


dt = 0
prevTime = time()
i = 0
i_f = 0

dir = 0
dir_predictor = 0

# gyroscope sensitivity +-2000dps = ~ +-34.91radian/s = 0.3491radian/10ms
# 4pi radians = ~720 degrees, fastest the ball can be rotated by a person is about 2 rounds per second

# max_radian_per_update = 4 * np.pi
max_step_per_rot = 3

STEP_PER_SEC = 3

REFRESH_RATE = 0.02 # ~10ms
#
# cooldown time before a new note can be request
# only 1 note changed request can be made every 100ms
cooldown = 0
ready = True

def run(mg, sensor):
    global dt, prevTime, dir, i, i_f

    while True:
        try:
            if sensor.rotStrength > 3:
            #     dir = get_dir(sensor.rotDir)
            #     i_f = max(0, min(7, i_f + dir * dt * 6))
            #     i = ceil(i_f) if int(i_f) - i_f > 0.5 else floor(i_f)
            #     # print(dir, i, i_f)
            #     mg.set_freq(C_Major[i])
                i = floor(sensor.yaw / 25.7)
                i = 7 - (i % 7) if i >= 7 else i
                mg.set_volume(1)
                mg.set_freq(C_Major[i])
                sensor.set_pixels(i)
            elif sensor.rotStrength > 0.4:
                mg.set_volume(0.8)
                i = floor(sensor.yaw / 25.7)
                i = 7 - (i % 7) if i >= 7 else i
                mg.set_freq(C_Major[i])
            else:
            #      reset_dir()
                mg.set_volume(0)
                 
            # mg.set_freq(C_Major[floor(i)])
                 
            # dt = time() - prevTime
            # prevTime = time()
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