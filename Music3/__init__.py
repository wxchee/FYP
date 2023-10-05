import numpy as np
import soundfile as sf
from time import time, sleep
from math import floor

from shared import rotMag, aX, aY, aZ

from Music3.stream import Stream

from multiprocessing import Array, Value


AUDIO_FILES = [
    'audios/music3/0_africanclave.wav',
    'audios/music3/x1_guiro.wav',
    'audios/music3/x2_bongo3.wav',
    'audios/music3/y1_cowbell1.wav',
    'audios/music3/y2_cowbell2.wav',
    'audios/music3/z1_cabassa.wav',
    'audios/music3/z2_casternet.wav'
]


SAMPLE_RATE_M3 = 22050
SLOT_SIZE = 10000
INTERVAL = 8

SYNC_INTERVAL = 2

PERIOD = SLOT_SIZE * INTERVAL

min_sample_chunk = 500

# update 
ds = []
for i in range(len(AUDIO_FILES)):
    ds.append(Array('d', PERIOD))

init_t = Value('d', 0.0)

class Music3:
    def __init__(self):
        # self.init_t = 0
        self.last_sync = 0
        
        self.streams = []

        for i, file in enumerate(AUDIO_FILES):
            wav, sr = sf.read(file)
            trimmedWav = wav

            if len(wav) < SLOT_SIZE:
                padOffset = SLOT_SIZE - len(wav)
                trimmedWav = np.concatenate((wav, np.zeros(padOffset)))
            else:
                trimmedWav = wav[:SLOT_SIZE]
                print(i, 'exceed 8000')

            self.streams.append(Stream(trimmedWav, SLOT_SIZE * INTERVAL))

            if i == 0:
                # customize background stream's track
                ds[0] = np.tile(trimmedWav, INTERVAL)
                lastSlotIndex = int((INTERVAL - 1) / INTERVAL * PERIOD)
                ds[0][:lastSlotIndex] = ds[0][:lastSlotIndex] * 0.5
                ds[0][lastSlotIndex:] = ds[0][lastSlotIndex:] * 0.15
                



    def _callback(self, outdata, frames, paT, status, i):
        # synchronize all streams
        # use the tick stream as reference
        
        cur_t = paT.currentTime - init_t.value

        if not self.streams[i].hadSync:
            self.streams[i].syncFirst(cur_t, SAMPLE_RATE_M3)
            # print('first sync')
        elif (cur_t % SYNC_INTERVAL) < self.last_sync: # sync each track every SYNC_INTERVAL seconds
            self.streams[i].sync(cur_t, SAMPLE_RATE_M3)
            # print(i, 'sync')

        if i == 0:
            self.last_sync = cur_t % SYNC_INTERVAL
        
        outdata[:, 0] = self.streams[i].update_wav(ds[i], frames)


    def update_track(self, oldD, i):
        start_frame = SLOT_SIZE * i
        end_frame = start_frame + SLOT_SIZE
        oldD[start_frame:end_frame] = self.d0
        return oldD

    def start(self):
        import sounddevice as sd
        # self.init_t = time()
        self.last_sync = 0

        # the callback function argument need to be constant, thus unwrap the loop
        self.streams[0].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 0))
        self.streams[1].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 1))
        self.streams[2].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 2))
        self.streams[3].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 3))
        self.streams[4].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 4))
        self.streams[5].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 5))
        self.streams[6].outstream = sd.OutputStream(samplerate=SAMPLE_RATE_M3,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 6))
        
        for i in range(len(self.streams)):
            self.streams[i].outstream.start()
            print(i, 'start')

    
    def stop(self):
        for i in range(len(self.streams)):
            self.streams[i].outstream.close()
            ds[i] = np.zeros(PERIOD)

    def run(self):
        import sounddevice as sd
        init_t.value = time()
        while True:
            # print(aX.value, aY.value, aZ.value)
            i = -1
            if abs(aX.value) > 0.9:
                i = 1 if aX.value < 0 else 2
            elif abs(aY.value) > 0.9:
                i = 3 if aY.value < 0 else 4
            elif abs(aZ.value) > 0.9:
                i = 5 if aZ.value < 0 else 6

            if i > 0 and rotMag.value > 7.5:
                cur_f = ((time() - init_t.value) * SAMPLE_RATE_M3) % PERIOD
                target_slot_i = floor(cur_f / SLOT_SIZE)
                
                # from empire test, delay seems to be 1 slot(s) later consistently
                diff = target_slot_i + 1
                
                if diff < 0:
                    target_slot_i = INTERVAL + diff
                elif diff >= INTERVAL:
                    target_slot_i = diff - INTERVAL
                else:
                    target_slot_i = diff
                
                print(i, 'add at', target_slot_i)

                start_frame = SLOT_SIZE * target_slot_i
                end_frame = start_frame + SLOT_SIZE
                ds[i][start_frame:end_frame] = self.streams[i].d0

                sd.play(self.streams[i].d0, SAMPLE_RATE_M3)
                sleep(1)
            
            # sleep(0.1)
