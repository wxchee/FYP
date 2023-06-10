
from time import sleep,time
import numpy as np
from math import floor, ceil, copysign
from musicgen import MusicGen
from musicgen.tools import C_Major, NOTES, PATTERN1
from shared import yaw, rotMag, set_volume, set_freq

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
prevT = time()

dir = 0
dir_predictor = 0

# gyroscope sensitivity +-2000dps = ~ +-34.91radian/s = 0.3491radian/10ms
# 4pi radians = ~720 degrees, fastest the ball can be rotated by a person is about 2 rounds per second

# # max_radian_per_update = 4 * np.pi
# max_step_per_rot = 3

# STEP_PER_SEC = 3

REFRESH_RATE = 0.02 # ~10ms
#
# cooldown time before a new note can be request
# only 1 note change request can be made every 100ms
cooldown = 0
ready = True

def run():
    global dt, prevT
    print('start control')
    # global dt, prevTime
    step = 25.7 # 14 steps
    # step = 23.93 # 15 steps
    set_volume(1)
    while True:
        try:
            for note in PATTERN1["notes"]:
                for pattern in PATTERN1["pattern"]:
                    print("note", NOTES[note + pattern])
                    set_freq(NOTES[note + pattern])
                    
                    curSecond = 0
                    while curSecond < 125:
                        dt = (time() - prevT) * 1000 # ms
                        curSecond += dt
                        prevT = time()

            
            # print('rotMag', rotMag.value)
            # if rotMag.value > 3:
            #     mg.set_volume(1)
            #     mg.set_freq(i)
                
            # elif rotMag.value > 0.4:
            #     mg.set_volume(0.8)
            #     mg.set_freq(i)
            # else:
            #     mg.set_volume(0)
        except KeyboardInterrupt:
                print("stop music thread.")
        
        prevT = time()
        sleep(REFRESH_RATE)
        


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