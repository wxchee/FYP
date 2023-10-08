import numpy as np
import soundfile as sf
from time import time, sleep
import math
from multiprocessing import Array, Value

from shared import rotMag, aDir
from PlayMode4.stream import Stream
from PlayMode3 import AUDIO_FILES, SLOT_SIZE, SAMPLE_RATE_M3, rotMagTh



INTERVAL = 8
PERIOD = SLOT_SIZE * INTERVAL

SYNC_INTERVAL = 2

min_sample_chunk = 500

# shared variables among processes
ds = []
for i in range(len(AUDIO_FILES)):
    ds.append(Array('d', PERIOD))

init_t = Value('d', 0.0)


class PlayMode4:
    def __init__(self):
        self.last_sync = 0
        
        self.streams = []

        for i, file in enumerate(AUDIO_FILES):
            wav, sr = sf.read(file)
            trimmedWav = wav
            print('load', i, len(wav), sr)
            if len(wav) < SLOT_SIZE:
                padOffset = SLOT_SIZE - len(wav)
                trimmedWav = np.concatenate((wav, np.zeros(padOffset)))
            else:
                trimmedWav = wav[:SLOT_SIZE]
                print(i, 'exceed 8000')

            trimmedWav = np.array(trimmedWav) * 2
            self.streams.append(Stream(trimmedWav, PERIOD))


            if i == 0:
                # customize background stream's track
                ds[0][:] = list(trimmedWav) * INTERVAL
                
                lastSlotIndex = int((INTERVAL - 1) / INTERVAL * PERIOD)
                ds[0][:lastSlotIndex] = np.array(ds[0][:lastSlotIndex]) * 0.15
                ds[0][lastSlotIndex:] = np.array(ds[0][lastSlotIndex:]) * 0.05
                



    def _callback(self, outdata, frames, paT, status, i):
        cur_t = time() - init_t.value

        if not self.streams[i].hadSync:
            self.streams[i].syncFirst(cur_t, SAMPLE_RATE_M3)
        elif (cur_t % SYNC_INTERVAL) < self.last_sync: # sync each track every SYNC_INTERVAL seconds
            self.streams[i].sync(cur_t, SAMPLE_RATE_M3)

        if i == 0:
            self.last_sync = cur_t % SYNC_INTERVAL # use the first stream time as the pivot time to sync timing across all seven streams
        
        outdata[:, 0] = self.streams[i].update_wav(ds[i], frames)


    def update_track(self, oldD, i):
        start_frame = SLOT_SIZE * i
        end_frame = start_frame + SLOT_SIZE
        oldD[start_frame:end_frame] = self.d0
        return oldD

    def start(self):
        import sounddevice as sd
        
        self.last_sync = 0
        
        self.streams[0].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 0))
        self.streams[1].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 1))
        self.streams[2].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 2))
        self.streams[3].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 3))
        self.streams[4].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 4))
        self.streams[5].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 5))
        self.streams[6].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 6))
        
        for i in range(len(self.streams)):
            self.streams[i].outstream.start()

    
    def stop(self):
        for i in range(len(self.streams)):
            self.streams[i].outstream.close()

            ds[i][:] = [0] * PERIOD
        

    def run(self):
        import sounddevice as sd
        init_t.value = time()

        while True:
            if aDir.value > 0 and rotMag.value > rotMagTh:
                cur_f = ((time() - init_t.value) * SAMPLE_RATE_M3) % PERIOD
                target_slot_d = cur_f / SLOT_SIZE
                th = target_slot_d - int(target_slot_d)
                target_slot_i = math.floor(target_slot_d) if th < 0.5 else math.ceil(target_slot_d)
                
                target_slot_i = target_slot_i % INTERVAL
                
                print('percussive ', aDir.value, ', add at', target_slot_i)

                start_frame = SLOT_SIZE * target_slot_i
                end_frame = start_frame + SLOT_SIZE
                ds[aDir.value][start_frame:end_frame] = self.streams[aDir.value].d0

                sd.play(self.streams[aDir.value].d0, SAMPLE_RATE_M3)
                sleep(0.25)
            
            sleep(0.01)
