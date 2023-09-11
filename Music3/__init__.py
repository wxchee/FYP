from tools import fs
import numpy as np
import soundfile as sf
from time import time, sleep
from math import floor, ceil

from shared import rotMag, aX, aY, aZ

AUDIO_FILES = [
    'audios/music3/0_africanclave.wav',
    'audios/music3/x1_bongo1.wav',
    'audios/music3/x2_bongo3.wav',
    'audios/music3/y1_cowbell1.wav',
    'audios/music3/y2_cowbell2.wav',
    'audios/music3/z1_cabassa.wav',
    'audios/music3/z2_casternet.wav'
]

# SLOT_SIZE = 5500
SLOT_SIZE = 8000
INTERVAL = 16

SYNC_INTERVAL = 2

PERIOD = SLOT_SIZE * 16

min_sample_chunk = 1000

class Music3:
    def __init__(self):
        import sounddevice as sd
        self.ostream_tick = sd.OutputStream(samplerate=fs,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 0))
        self.ostream_x1 = sd.OutputStream(samplerate=fs,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 1))
        self.ostream_x2 = sd.OutputStream(samplerate=fs,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 2))
        self.ostream_y1 = sd.OutputStream(samplerate=fs,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 3))
        self.ostream_y2 = sd.OutputStream(samplerate=fs,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 4))
        self.ostream_z1 = sd.OutputStream(samplerate=fs,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 5))
        self.ostream_z2 = sd.OutputStream(samplerate=fs,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 6))
        # self.ostream_tick = None
        # self.ostream_x1 = None
        # self.ostream_x2 = None
        # self.ostream_y1 = None
        # self.ostream_y2 = None
        # self.ostream_z1 = None
        # self.ostream_z2 = None

        self.init_t = 0
        self.cur_t = 0
        self.last_sync = 0
        
        self.tracks = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None}
        for i, file in enumerate(AUDIO_FILES):
            wav, sr = sf.read(file)
            print(i, len(wav))
            trimmedWav = wav

            if len(wav) < SLOT_SIZE:
                padOffset = SLOT_SIZE - len(wav)
                trimmedWav = np.pad(wav, (0, padOffset), 'constant')
            else:
                trimmedWav = wav[:SLOT_SIZE]

            self.tracks[i] = {
                "d0": trimmedWav,
                "d": np.tile(trimmedWav, INTERVAL),
                # "d": np.zeros(PERIOD),
                "f": 0
            }

        # self.tracks[0]["d"] = np.tile(self.tracks[0]["d0"], INTERVAL)
        # self.tracks[0]["d"] = np.tile(self.tracks[0]["d0"], INTERVAL)
        # self.tracks[0]["d"] = np.tile(self.tracks[0]["d0"], INTERVAL)
        # self.tracks[0]["d"] = np.tile(self.tracks[0]["d0"], INTERVAL)
        # self.tracks[0]["d"] = np.tile(self.tracks[0]["d0"], INTERVAL)
        # self.tracks[0]["d"] = np.tile(self.tracks[0]["d0"], INTERVAL)


    def _callback(self, outdata, frames, paT, status, i):
        # synchronize all streams
        # use the tick stream as reference
        
        cur_t = paT.currentTime - self.init_t
        
        # if any stream current
        if (cur_t % SYNC_INTERVAL) < self.last_sync: # sync each track every SYNC_INTERVAL seconds
            self.tracks[i]['f'] = floor(cur_t * 44100.0) % PERIOD

        if i == 0:
            self.last_sync = cur_t % SYNC_INTERVAL

        if self.tracks[i]['f'] + frames > PERIOD:
            remain_frames = frames - (PERIOD - self.tracks[i]['f'])
            new_wav = np.concatenate((self.tracks[i]['d'][self.tracks[i]['f']:], self.tracks[i]['d'][:remain_frames]))
            self.tracks[i]['f'] = remain_frames
        else:
            new_wav = self.tracks[i]['d'][self.tracks[i]['f']:self.tracks[i]['f']+frames]
            self.tracks[i]['f'] += frames

        outdata[:, 0] = new_wav


    def start(self):
        self.init_t = time()
        # self.cur_t = 0
        self.last_sync = 0

        for i in range(1, 7):
            self.tracks[i]["d"] = np.zeros(PERIOD)
            self.tracks[i]["f"] = 0

        # self.ostream_tick = sd.OutputStream(samplerate=sr,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 0))
        # self.ostream_x1 = sd.OutputStream(samplerate=sr,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 1))
        # self.ostream_x2 = sd.OutputStream(samplerate=sr,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 2))
        # self.ostream_y1 = sd.OutputStream(samplerate=sr,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 3))
        # self.ostream_y2 = sd.OutputStream(samplerate=sr,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 4))
        # self.ostream_z1 = sd.OutputStream(samplerate=sr,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 5))
        # self.ostream_z2 = sd.OutputStream(samplerate=sr,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 6))
        
        self.ostream_tick.start()
        self.ostream_x1.start()
        self.ostream_x2.start()
        self.ostream_y1.start()
        self.ostream_y2.start()
        self.ostream_z1.start()
        self.ostream_z2.start()

    
    def stop(self):
        self.ostream_tick.stop()
        self.ostream_x1.stop()
        self.ostream_x2.stop()
        self.ostream_y1.stop()
        self.ostream_y2.stop()
        self.ostream_z1.stop()
        self.ostream_z2.stop()

    def run(self):
        # import sounddevice as sd
        # print(rotMag.value, aX.value, aY.value, aZ.value)
        print('x', abs(aX.value), 'y', abs(aY.value), 'z', abs(aZ.value))
        if rotMag.value >= 5:
            cur_f = ((time() - self.init_t) * 44100) % PERIOD
            print('rot at', cur_f)
            
            i = -1
            if abs(aX.value) > 0.75:
                i = 1 if aX.value < 0 else 2
            elif abs(aY.value) > 0.75:
                i = 3 if aY.value < 0 else 4
            elif abs(aZ.value) > 0.75:
                i = 5 if aZ.value < 0 else 6


            if i > 0:
                print('target', i)
                
                # cur_f = ((time() - self.init_t) * 44100) % PERIOD
                target_slot_i = floor(cur_f / SLOT_SIZE)
                start = target_slot_i * SLOT_SIZE
                print(i, 'add at', target_slot_i)
                self.tracks[i]["d"][start:(start + SLOT_SIZE)] = self.tracks[i]["d0"]
                # sd.play(self.tracks[i]["d0"], fs) 
            sleep(1)
