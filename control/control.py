# control 
# - monitor accelerometer magnitude, if acc magnitude exceed threshold, increment to next mode

from time import sleep

from shared import aMag

from Music1 import Music1
from Music2 import Music2
from Music3 import Music3
from Music3Lite import Music3Lite
from MusicTest import MusicTest

from multiprocessing import Process

REFRESH_RATE = 0.02 # ~10ms

def run():
    print('start control')
    
    modeIndex = 0

    runModes = [
        # MusicTest,
        Music3,
        Music3Lite,
        Music1,
        Music2
    ]
    modeCount = len(runModes)


    # initialise the first process
    activeMusic = runModes[modeIndex]()
    activeMusic.start()

    activeP = Process(target=activeMusic.run)
    activeP.start()

    while True:
        try:
            if aMag.value > 2: # trigger mode switching
                print('aMag', aMag.value)
                aMag.value = 0

                activeMusic.stop()
                print('current Music instance stop')

                activeP.terminate() # terminate current Music Process
                print('current run process terminates')
                
                activeP = None
                activeMusic = None  # free memory from current Music instance
                
                print('wait for current active music to release outstream')
                sleep(1) #
                print('done')

                modeIndex = (modeIndex + 1) % modeCount

                activeMusic = runModes[modeIndex]() # initialise new Music instance
                

                activeP = Process(target=activeMusic.run)
                
                print('mode switch to {}'.format(modeIndex))
                sleep(2) # give a buffer for subsequent switch motion, to prevent wrong triggered due to inertia
                
                print('sleep done')
                activeMusic.start()
                print('start instance')
                activeP.start()
                print('start process')

        except KeyboardInterrupt:
                print("stop music thread.")
        
        
        sleep(REFRESH_RATE)
        
