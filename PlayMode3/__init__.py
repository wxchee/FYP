import numpy as np
from time import sleep
import soundfile as sf

from shared import rotMag, aDir

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

rotMagTh = 5.5

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

        while True:
            if aDir.value > 0 and rotMag.value > rotMagTh:
                print('play ', aDir.value)
                sd.play(self.ds0[aDir.value], SAMPLE_RATE_M3)
                sleep(0.25)
        
            sleep(0.001)
