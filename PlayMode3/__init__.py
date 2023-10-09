import numpy as np
from time import sleep
import soundfile as sf

from shared import getRotMag, aDir

AUDIO_FILES = [
    'audios/music3_acoustic/0_africanclave.wav',
    'audios/music3_acoustic/1_clap.wav',
    'audios/music3_acoustic/2_hat.wav',
    'audios/music3_acoustic/3_tom.wav',
    'audios/music3_acoustic/4_kick.wav',
    'audios/music3_acoustic/5_snare.wav',
    'audios/music3_acoustic/6_block.wav',
]

SAMPLE_RATE_M3 = 44100
SLOT_SIZE = 10000

rotMagTh = 8

class PlayMode3:
    def __init__(self):
        self.ds0 = []

        for i,file in enumerate(AUDIO_FILES):
            wav, sr = sf.read(file)
            trimmedWav = wav

            if len(wav) < SLOT_SIZE:
                padOffset = SLOT_SIZE - len(wav)
                trimmedWav = np.concatenate((wav, np.zeros(padOffset)))
            else:
                trimmedWav = wav[:SLOT_SIZE]
                print(i, 'exceed 8000')
            
            self.ds0.append(trimmedWav)

    def start(self):
        pass
    
    def stop(self):
        pass

    def run(self):
        import sounddevice as sd
        curDir = -1
        while True:
            if curDir != aDir.value:
                if aDir.value < 0:
                    print('\nnot align with any axis.\n')
                else:
                    print('\nnow align with ', aDir.value, '\n')
                curDir = aDir.value
            
            if getRotMag() > rotMagTh:
                print('play ', aDir.value)
                sd.play(self.ds0[aDir.value], SAMPLE_RATE_M3)
                sleep(0.25)
        
            sleep(0.001)
