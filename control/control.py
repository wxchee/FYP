# control 
# - monitor accelerometer magnitude, if acc magnitude exceed threshold, increment to next mode

from time import sleep,time
import numpy as np
from math import floor, ceil, copysign
import shared
from shared import aMag, mode

# from Music1 import Music1
from Music2 import Music2

# mode 0 dependent
from tools import PATTERN1, NOTES
from shared import goalFreq, goalAmp, rotMag
pi = 0
ni = 0

dt = 0
prevT = 0
curSecond = 0
pi = ni = 0

REFRESH_RATE = 0.02 # ~10ms

def run():
    # sounddevice has issue working with multiprocessing's Process when import onto global level
    # solution: import within function scope 
    # https://blog.csdn.net/NormanBeita/article/details/106499473
    # import sounddevice as sd
    print('start control')
    
    runModes = [Music2()]
    modeCount = 2
    
    if mode.value > 0:
        runModes[mode.value - 1].start()

    while True:
        try:
            print(aMag.value)
            if aMag.value > 2: # trigger mode switching
                if mode.value > 0: # if current mode is not 0
                    runModes[mode.value - 1].stop()
                
                targetMode = (mode.value + 1) % modeCount

                if targetMode > 0: # if new mode is not zero
                    runModes[targetMode - 1].start()
                
                mode.value = targetMode

                print('switch to new mode {}'.format(mode.value))
                sleep(2) # give a buffer for subsequent switch motion, to prevent wrong triggered due to inertia

            if mode.value > 0:
                runModes[mode.value - 1].run()
            else: 
                # mode 0 only custom control
                global dt, prevT, curSecond, pi, ni
                if curSecond >= 1000:
                    curSecond = 0
                    if pi == len(PATTERN1["pattern"]) - 1:
                        ni = (ni + 1) % len(PATTERN1["notes"])

                    pi = (pi + 1) % len(PATTERN1["pattern"])

                    goalFreq.value = NOTES[PATTERN1["notes"][ni] + PATTERN1["pattern"][pi]]


                goalAmp.value = min(1, max(0, (rotMag.value - 0.03)) / 2)

            dt = (time() - prevT) * 1000 * rotMag.value / 0.5
            curSecond += dt
            prevT = time()

        except KeyboardInterrupt:
                print("stop music thread.")
        
        # prevT = time()
        sleep(REFRESH_RATE)
        
