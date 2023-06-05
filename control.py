
from time import sleep,time
import numpy as np
from math import floor, ceil, copysign
from musicgen.tools import C_Major

note_mat = [
     0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0,
     1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0, 1,
     2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2,
     3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3,
     4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4,
     5, 6, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5,
     6, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6,
     7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7,
     6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7, 6,
     5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7, 6, 5,
     4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4,
     3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3,
     2, 1, 0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2,
     1, 0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1,
     0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0
]
     
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
# only 1 note change request can be made every 100ms
cooldown = 0
ready = True

def run(mg, sensor):
    global dt, prevTime, dir, i, i_f, note_mat
    step = 25.7 # 14 steps
    # step = 23.93 # 15 steps
    while True:
        try:

            z = floor(sensor.yaw / step)
            y = floor(sensor.pitch / step)
            # y = 0
            i = C_Major[note_mat[z * 15 + y]]
            # i = C_Major[]
            print(z, y, i)
            if sensor.rotStrength > 3:
                # z = floor(sensor.yaw / 25.7)
                # z = 7 - (z % 7) if z >= 7 else z
                mg.set_volume(1)
                mg.set_freq(i)
                # mg.set_freq(C_Major[z])
                
            elif sensor.rotStrength > 0.4:
                mg.set_volume(0.8)
                mg.set_freq(i)
            else:
            #      reset_dir()
                mg.set_volume(0)
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