import numpy as np
from math import floor

class Stream:
    def __init__(self, i, d0, period):
        self.i = i
        self.f = 0
        self.d0 = d0
        self.period = period
        self.outstream = None
        self.hadSync = False


    def syncFirst(self, t, sr):
        self.sync(t, sr)
        self.hadSync = True


    def sync(self, t, sr):
        self.f = floor(t * sr) % self.period


    def update_wav(self, dRef, frames):
        if self.f + frames > self.period:
            remain_frames = frames - (self.period - self.f)
            new_wav = np.concatenate((dRef[self.f:], dRef[:remain_frames]))
            self.f = remain_frames
        else:
            new_wav = dRef[self.f:self.f + frames]
            self.f += frames

        return new_wav
