import soundfile as sf
import numpy as np
from tools import fs
from shared import aX, aY, aZ, rotMag

import sys
from time import time, sleep
from math import ceil, floor
min_sample_chunk = 1000

AUDIO_FILES = [
    'audios/music2/track_drum.wav',
    'audios/music2/track_piano.wav',
    'audios/music2/track_mag_string.wav'
]

from multiprocessing import Value

vols = [Value('d', 0.0), Value('d', 0.0), Value('d', 0.0)]

SYNC_INTERVAL = 2


FRAME_CAP = 682760

class Music2:
    def __init__(self):
        self.freq = 0

        self.amplitude = 0
        self.volume_fade_duration = 0.3

        self.init_t = 0
        self.last_sync = 0

        self.tracks = {0: None, 1: None, 2: None}

        for i, file in enumerate(AUDIO_FILES):
            wav, sr = sf.read(file)
            self.tracks[i] = { 'd': wav[:FRAME_CAP], 'l': FRAME_CAP if len(wav) > FRAME_CAP else len(wav), 'f': 0, 'amp': 0}
        
        self.outstream = None
        self.outstream2 = None
        self.outstream3 = None
        

    def _callback(self, outdata, frames, paT, status, i):
        if (status):
            print('STATUS: ', status, sys.stderr)
        
        cur_t = paT.currentTime - self.init_t
        
        print('run m2 vols {} {} {}'.format(vols[0].value, vols[1].value, vols[2].value))
        if (cur_t % SYNC_INTERVAL) < self.last_sync: # sync each track every 5 seconds
            self.tracks[i]['f'] = floor(cur_t * 44100.0) % self.tracks[i]['l']
            print(i, 'repos', floor(cur_t * 44100.0) % self.tracks[i]['l'])
        
        if i == 0:
            self.last_sync = cur_t % SYNC_INTERVAL
        
    
        if self.tracks[i]['f'] + frames > self.tracks[i]['l']:
            remain_frames = frames - (self.tracks[i]['l'] - self.tracks[i]['f'])
            new_wav = np.concatenate((self.tracks[i]['d'][self.tracks[i]['f']:], self.tracks[i]['d'][:remain_frames]))
            self.tracks[i]['f'] = remain_frames
        else:
            new_wav = self.tracks[i]['d'][self.tracks[i]['f']:self.tracks[i]['f']+frames]
            self.tracks[i]['f'] += frames

        

        # handle amplitude change
        amp_env = np.ones(frames)
        goal_amp = vols[i].value
        if self.tracks[i]['amp'] != goal_amp:
            if abs(self.tracks[i]['amp'] - goal_amp) < 0.01:
                self.tracks[i]['amp'] = goal_amp
            else:
                amp_env = self.get_amp_env(self.tracks[i]['amp'], frames, goal_amp)
                self.tracks[i]['amp'] = amp_env[-1]


        target_amp = amp_env if self.tracks[i]['amp'] != goal_amp else self.tracks[i]['amp']

        outdata[:,0] = new_wav * target_amp


    def get_amp_env(self, start_amp, frames, goal):
        dir = 1 if start_amp < goal else -1
        diff = goal - start_amp
        
        end_amp = start_amp + diff * min(1, frames / (fs * self.volume_fade_duration))
        
        amp_wave = np.linspace(start_amp, end_amp, frames)
        if dir == 1:
            if (end_amp < goal):
                return amp_wave
        else:
            if (end_amp > goal):
                return amp_wave

        diff_frames = int(abs(diff * fs * self.volume_fade_duration))

        return np.linspace(start_amp, goal, diff_frames)
    

    def start(self):
        import sounddevice as sd
        self.init_t = time()
        self.last_sync = 99

        self.outstream = sd.OutputStream(samplerate=fs,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 0))
        self.outstream2 = sd.OutputStream(samplerate=fs,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 1))
        self.outstream3 = sd.OutputStream(samplerate=fs,channels=1,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 2))

        self.outstream.start()
        self.outstream2.start()
        self.outstream3.start()

    def run(self):
        while True:
            if rotMag.value > 4:
                vols[0].value = vols[1].value = vols[2].value = 1.0
            else:
                vols[0].value = abs(aX.value) if abs(aX.value) > 0.5 else 0.0
                vols[1].value = abs(aY.value) if abs(aY.value) > 0.5 else 0.0
                vols[2].value = abs(aZ.value) if abs(aZ.value) > 0.5 else 0.0
            
            sleep(0.05)
    
    def stop(self):
        self.outstream.close()
        self.outstream2.close()
        self.outstream3.close()