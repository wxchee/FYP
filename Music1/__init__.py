from tools import get_wave_by_freq, get_time_array, get_crossfade_filter, fs
from tools import C_Major, STREAM_STATE
# , PATTERN1, NOTES

from time import time, sleep

import numpy as np
import sys
from shared import rotMag, mode, goalFreq, goalAmp



# approx. stream requested frame size in rpi: 512
# approx. stream requested frame size in laptop: 400
# hence, make every freq wave sample to bigger than 512
min_sample_chunk = 600 # ~13.6ms worth of frame

class Music1:
    def __init__(self):
        self.dt = 0
        self.prevT = 0

        self.freq = 0
        self.wave = get_wave_by_freq(0, 0, np.linspace(0, 1, min_sample_chunk))
        self.wavelength = min_sample_chunk

        self.amplitude = 0
        self.amp_duration = 0.15
        
        # goalFreq.value = C_Major[0]
        # goalAmp.value = 1

        self.cross_wave = None
        self.cross_wavelengh = 0

        self.phase = 0

        self.state = STREAM_STATE.IDLE
        self.next_state = STREAM_STATE.IDLE

        self.outstream = None

        self.init() # only call this if Music1 is instantiated via Process in main.py

        
    def _callback(self, outdata, frames, time, status):
        if (status):
            print('STATUS: ', status, sys.stderr)

        # print('f', frames)
        # CROSSFADE state
        if self.state == STREAM_STATE.CROSSFADE: 
            if self.phase + frames > self.cross_wavelengh: # reach the end of the wave
                diff = self.phase + frames - self.cross_wavelengh
                goal_wave, goal_wavelength = self.get_goal(goalFreq.value)
                new_wave = np.concatenate((self.cross_wave[self.phase:self.cross_wavelengh], goal_wave[:diff]))
                self.freq, self.wave, self.wavelength = goalFreq.value, goal_wave, goal_wavelength
                self.state = self.next_state = STREAM_STATE.IDLE
                self.phase = diff
            else:
                new_wave = self.cross_wave[self.phase:(self.phase + frames)]
                self.phase += frames
        
        # IDLE state
        else: 
            if self.phase + frames > self.wavelength: # reach the end of the wave
                diff = self.phase + frames - self.wavelength
                if goalFreq.value != self.freq:
                    self.cross_wave, self.cross_wavelengh = self.get_cross_fade(self.freq, goalFreq.value)
                    new_wave = np.concatenate((self.wave[self.phase:self.wavelength], self.cross_wave[:diff]))
                    self.state = STREAM_STATE.CROSSFADE
                else:
                    new_wave = np.concatenate((self.wave[self.phase:self.wavelength], self.wave[:diff]))

                self.phase = diff
            else:
                new_wave = self.wave[self.phase:(self.phase + frames)]
                self.phase += frames

        # handle amplitude change
        amp_env = np.ones(frames)
        if self.amplitude != goalAmp.value:
            amp_env = self.get_amp_env(self.amplitude, frames)
            self.amplitude = amp_env[-1]

        target_amp = amp_env.reshape(-1,1) if self.amplitude != goalAmp.value else self.amplitude

        outdata[:] = new_wave.reshape(-1,1) * target_amp
        

    def get_goal(self, goal_freq):
        global min_sample_chunk
        cycle = round(min_sample_chunk * goal_freq / fs)
        goal_wavelength = round(fs / goal_freq * cycle)
        new_time_array = get_time_array(0, goal_wavelength)
        goal_wave = get_wave_by_freq(goal_freq, 1, new_time_array)

        return goal_wave, goal_wavelength


    def get_amp_env(self, start_amp, frames):
        dir = 1 if start_amp < goalAmp.value else -1
        end_amp = start_amp + (goalAmp.value - start_amp) * frames / (fs * self.amp_duration)

        return np.linspace(start_amp, end_amp, frames)
    

    def get_cross_fade(self, prev_freq, next_freq):
        global min_sample_chunk
        cycle = round(min_sample_chunk * 10 * next_freq / fs)
        cross_wavelengh = round(fs / next_freq * cycle)

        time_array = get_time_array(0, cross_wavelengh)
        prev_wave = get_wave_by_freq(prev_freq, 1, time_array)
        next_wave = get_wave_by_freq(next_freq, 1, time_array)
        cross_env = get_crossfade_filter(cross_wavelengh)

        cross_wave = prev_wave * cross_env + next_wave * (1 - cross_env)

        return cross_wave, cross_wavelengh

    def init(self):
        import sounddevice as sd
        self.dt = 0
        self.prevT = time()
        
        self.outstream = sd.OutputStream(
            samplerate=fs,
            channels=1,
            blocksize=500, # must be smaller than min_sample_chunk
            callback= lambda *args: self._callback(*args)
        )

    def run(self):
        while True:
            if mode.value == 0:
                if not self.outstream.active:
                    self.outstream.start()
            else:
                if self.outstream.active:
                    self.outstream.stop()
                sleep(0.2)