# control 
# - monitor accelerometer magnitude, if acc magnitude exceed threshold, increment to next mode
from time import sleep
from multiprocessing import Process
import soundfile as sf

from shared import aMag
from PlayMode1 import PlayMode1
from PlayMode2 import PlayMode2
from PlayMode3 import PlayMode3
from PlayMode4 import PlayMode4

PLAYMODE_AUDIOS = [
    'audios/voices/pm1.wav',
    'audios/voices/pm2.wav',
    'audios/voices/pm3.wav',
    'audios/voices/pm4.wav',
    'audios/voices/sm.wav'
]

pmWav = []
for i, file in enumerate(PLAYMODE_AUDIOS):
    wav, sr = sf.read(file)
    # print(len(wav), sr)
    pmWav.append((wav, sr))

def run():
    import sounddevice as sd
    pmIndex = 0
    playModes = [ PlayMode1, PlayMode2, PlayMode3, PlayMode4 ]
    noOfModes = len(playModes)

    # initialise the first process
    playMode = playModes[pmIndex]()
    playModeProcess = Process(target=playMode.run)
    playMode.start()
    playModeProcess.start()

    # play "Play mode 1" voice 
    wav, sr = pmWav[pmIndex]
    sd.play(wav, sr, blocking=True)
    sleep(1)

    while True:
        try:
            if aMag.value > 2: # trigger play mode switching
                
                # stop the current play mode and terminate its respective process
                playMode.stop()
                playModeProcess.terminate()

                # play switch mode voice
                smWav, smSR = pmWav[4]
                sd.play(smWav, smSR, blocking=True)

                # increment play mode index to the next one
                pmIndex = (pmIndex + 1) % noOfModes

                # instantiate new play mode and its process
                playMode = playModes[pmIndex]()
                playModeProcess = Process(target=playMode.run)
                
                print('mode switch to {}...'.format(pmIndex+1))
                sleep(1)
                
                # start running the new play mode process
                playMode.start()
                playModeProcess.start()
                
                # play the next mode indicator voice
                wav, sr = pmWav[pmIndex]
                sd.play(wav, sr, blocking=True)
                
                print('play mode ', (pmIndex+1), ' is ready.')

        except KeyboardInterrupt:
                print("stop music thread.")
        
        sleep(0.02)
        
