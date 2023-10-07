import numpy as np
from time import sleep
import soundfile as sf
from Music3 import AUDIO_FILES, SLOT_SIZE, PERIOD, SAMPLE_RATE_M3, rotMagTh

from shared import rotMag, aX, aY, aZ



class Music3Lite:
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

        while True:
            i = -1
            if abs(aX.value) > 0.75:
                i = 1 if aX.value < 0 else 2
            elif abs(aY.value) > 0.75:
                i = 3 if aY.value < 0 else 4
            elif abs(aZ.value) > 0.75:
                i = 5 if aZ.value < 0 else 6

            if i > 0 and rotMag.value > rotMagTh:
                print('play ', i)
                sd.play(self.ds0[i], SAMPLE_RATE_M3)
                sleep(0.5)
        
            sleep(0.001)
