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
    print('start control')
    
    modeIndex = 0

    runModes = [
        PlayMode1,
        PlayMode2,
        PlayMode3,
        PlayMode4,
    ]
    modeCount = len(runModes)


    # initialise the first process
    activeMode = runModes[modeIndex]()
    activeMode.start()

    activeModeP = Process(target=activeMode.run)
    activeModeP.start()

    while True:
        try:
            if aMag.value > 2: # trigger mode switching
                aMag.value = 0

                activeMode.stop() # close all outstream associated with this play mode

                activeModeP.terminate() # terminate current Music Process
                # print('current run process terminates')
                
                activeModeP = None
                activeMode = None  # free memory from current Music instance
                
                # print('wait for current active music to release outstream')
                # sleep(1) #
                # print('done')

                modeIndex = (modeIndex + 1) % modeCount

                activeMode = runModes[modeIndex]() # initialise new Music instance
                
                activeModeP = Process(target=activeMode.run)
                
                print('mode switch to {}'.format(modeIndex))
                sleep(1) # give a buffer for subsequent switch motion, to prevent wrong triggered due to inertia
                
                # print('sleep done')
                activeMode.start()
                # print('start instance')
                activeModeP.start()

                print('start play mode ', modeIndex)

        except KeyboardInterrupt:
                print("stop music thread.")
        
        
        sleep(0.02)
        
