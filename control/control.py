# control 
# - monitor accelerometer magnitude, if acc magnitude exceed threshold, increment to next mode

from time import sleep,time
import numpy as np
from math import floor, ceil, copysign
import shared
from shared import aMag, mode

from Music1 import Music1
from Music2 import Music2
from Music3 import Music3

from multiprocessing import Process

# mode 0 dependent
from shared import rotMag

REFRESH_RATE = 0.02 # ~10ms

activeMusic = None
activeP = None


def run():
    print('start control')
    
    runModes = [
        Music3,
        Music1,
        Music2
    ]
    modeCount = len(runModes)

    # initialise the first process
    activeMusic = runModes[mode.value]()
    activeMusic.start()

    activeP = Process(target=activeMusic.run)
    activeP.start()

    while True:
        try:
            if aMag.value > 2: # trigger mode switching
                print('aMag', aMag.value)
                activeP.terminate() # terminate current Music Process
                print('current run process terminates')
                activeMusic.stop()
                print('current Music instance stop')
                
                activeP = None
                activeMusic = None  # free memory from current Music instance
                
                print('wait for current active music to release outstream')
                sleep(1) #
                print('done')

                mode.value = (mode.value + 1) % modeCount

                activeMusic = runModes[mode.value]() # initialise new Music instance
                

                activeP = Process(target=activeMusic.run)
                
                print('mode switch to {}'.format(mode.value))
                sleep(2) # give a buffer for subsequent switch motion, to prevent wrong triggered due to inertia
                
                print('sleep done')
                activeMusic.start()
                print('start instance')
                activeP.start()
                print('start process')

        except KeyboardInterrupt:
                print("stop music thread.")
        
        # prevT = time()
        sleep(REFRESH_RATE)
        
