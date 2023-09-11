# control 
# - monitor accelerometer magnitude, if acc magnitude exceed threshold, increment to next mode

from time import sleep,time
import numpy as np
from math import floor, ceil, copysign
import shared
from shared import aMag

from Music1 import Music1
from Music2 import Music2

REFRESH_RATE = 0.02 # ~10ms

def run():
    import sounddevice as sd
    print('start control')
    
    mode = 0
    runModes = [Music1(), Music2()]
    
    runModes[mode].start(sd)

    while True:
        try:
            # print(aMag.value)
            if aMag.value > 10:
                runModes[mode].stop()
                mode = (mode + 1) % 2
                runModes[mode].start(sd)
                print('switch to new mode {}'.format(mode))

            runModes[mode].run(sd)

            # # dynamic melody mode
            # for note in PATTERN1["notes"]:
            #     for pattern in PATTERN1["pattern"]:
            #         set_freq(NOTES[note + pattern])
            #         curSecond = 0
            #         while curSecond < 1000:
            #             # this line will affect the dt, when change, dt factor need to be adjust accordingly
            #             set_volume(min(1, max(0, (rotMag.value - 0.03)) / 2)) 
            #             dt = (time() - prevT) * 1000 * rotMag.value / 0.5
            #             # dt = (time() - prevT) * 1000 # ms
            #             curSecond += dt
            #             prevT = time()



            # # load wav file test
            # if rotMag.value > 4:
            #     volX.value = volY.value = volZ.value = 1.0
            # else:
            #     volX.value = abs(aX.value) if abs(aX.value) > 0.5 else 0.0
            #     volY.value = abs(aY.value) if abs(aY.value) > 0.5 else 0.0
            #     volZ.value = abs(aZ.value) if abs(aZ.value) > 0.5 else 0.0

        except KeyboardInterrupt:
                print("stop music thread.")
        
        # prevT = time()
        sleep(REFRESH_RATE)
        
