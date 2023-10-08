# control 
# - monitor accelerometer magnitude, if acc magnitude exceed threshold, increment to next mode
from time import sleep
from multiprocessing import Process

from shared import aMag
from PlayMode1 import PlayMode1
from PlayMode2 import PlayMode2
from PlayMode3 import PlayMode3
from PlayMode4 import PlayMode4


def run():
    pmIndex = 0
    playModes = [ PlayMode1, PlayMode2, PlayMode3, PlayMode4 ]
    noOfModes = len(playModes)

    # initialise the first process
    playMode = playModes[pmIndex]()
    playModeProcess = Process(target=playMode.run)
    playMode.start()
    playModeProcess.start()

    while True:
        try:
            if aMag.value > 2: # trigger play mode switching

                # stop the current play mode and terminate its respective process
                playMode.stop()
                playModeProcess.terminate()

                # increment play mode index to the next one
                pmIndex = (pmIndex + 1) % noOfModes

                # instantiate new play mode and its process
                playMode = playModes[pmIndex]()
                playModeProcess = Process(target=playMode.run)
                
                print('mode switch to {}...'.format(pmIndex))
                sleep(1) # give a buffer for subsequent switch motion, to prevent wrong triggered due to inertia
                
                # start running the new play mode process
                playMode.start()
                playModeProcess.start()
                print('play mode ', pmIndex, ' is ready.')

        except KeyboardInterrupt:
                print("stop music thread.")
        
        sleep(0.02)
        
