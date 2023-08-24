from musicgen import tools
from musicgen.tools import C_Major, STREAM_STATE

from time import time

import sounddevice as sd
import numpy as np
import sys
# from shared import goal_amplitude, goal_freq
from shared import rotMag

from musicgen.tools.pattern import PATTERN1, NOTES

# approx. stream requested frame size in rpi: 512
# approx. stream requested frame size in laptop: 400
# hence, make every freq wave sample to bigger than 512
min_sample_chunk = 600 # ~13.6ms worth of frame

class Music1:
    def __init__(self):
        self.dt = 0
        self.prevT = 0

        self.freq = 0
        self.wave = tools.get_wave_by_freq(0, 0, np.linspace(0, 1, min_sample_chunk))
        self.wavelength = min_sample_chunk

        self.amplitude = 0
        self.amp_duration = 0.15
        
        self.goal_freq = C_Major[0]
        self.goal_amplitude = 1

        self.cross_wave = None
        self.cross_wavelengh = 0

        self.phase = 0

        self.state = STREAM_STATE.IDLE
        self.next_state = STREAM_STATE.IDLE

        self.outstream = None
        # self.outstream = sd.OutputStream(
        #     samplerate=tools.fs,
        #     channels=1,
        #     blocksize=500,
        #     callback= lambda *args: self._callback(*args)
        # )
        
        # self.outstream.start()
        # goal_freq.value = C_Major[0]
        # goal_amplitude.value = 1

        
    def _callback(self, outdata, frames, time, status):
        if (status):
            print('STATUS: ', status, sys.stderr)

        # print('f', frames)
        # CROSSFADE state
        if self.state == STREAM_STATE.CROSSFADE: 
            if self.phase + frames > self.cross_wavelengh: # reach the end of the wave
                diff = self.phase + frames - self.cross_wavelengh
                goal_wave, goal_wavelength = self.get_goal(self.goal_freq)
                new_wave = np.concatenate((self.cross_wave[self.phase:self.cross_wavelengh], goal_wave[:diff]))
                self.freq, self.wave, self.wavelength = self.goal_freq, goal_wave, goal_wavelength
                self.state = self.next_state = STREAM_STATE.IDLE
                self.phase = diff
            else:
                new_wave = self.cross_wave[self.phase:(self.phase + frames)]
                self.phase += frames
        
        # IDLE state
        else: 
            if self.phase + frames > self.wavelength: # reach the end of the wave
                diff = self.phase + frames - self.wavelength
                if self.goal_freq != self.freq:
                    self.cross_wave, self.cross_wavelengh = self.get_cross_fade(self.freq, self.goal_freq)
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
        if self.amplitude != self.goal_amplitude:
            amp_env = self.get_amp_env(self.amplitude, frames)
            self.amplitude = amp_env[-1]

        target_amp = amp_env.reshape(-1,1) if self.amplitude != self.goal_amplitude else self.amplitude

        outdata[:] = new_wave.reshape(-1,1) * target_amp
        

    def get_goal(self, goal_freq):
        global min_sample_chunk
        cycle = round(min_sample_chunk * goal_freq / tools.fs)
        goal_wavelength = round(tools.fs / goal_freq * cycle)
        new_time_array = tools.get_time_array(0, goal_wavelength)
        goal_wave = tools.get_wave_by_freq(goal_freq, 1, new_time_array)

        return goal_wave, goal_wavelength


    def get_amp_env(self, start_amp, frames):
        dir = 1 if start_amp < self.goal_amplitude else -1
        end_amp = start_amp + (self.goal_amplitude - start_amp) * frames / (tools.fs * self.amp_duration)

        return np.linspace(start_amp, end_amp, frames)
    

    def get_cross_fade(self, prev_freq, next_freq):
        global min_sample_chunk
        cycle = round(min_sample_chunk * 10 * next_freq / tools.fs)
        cross_wavelengh = round(tools.fs / next_freq * cycle)

        time_array = tools.get_time_array(0, cross_wavelengh)
        prev_wave = tools.get_wave_by_freq(prev_freq, 1, time_array)
        next_wave = tools.get_wave_by_freq(next_freq, 1, time_array)
        cross_env = tools.get_crossfade_filter(cross_wavelengh)

        cross_wave = prev_wave * cross_env + next_wave * (1 - cross_env)

        return cross_wave, cross_wavelengh



    def start(self):
        self.dt = 0
        self.prevT = time()
        
        self.outstream = sd.OutputStream(
            samplerate=tools.fs,
            channels=1,
            blocksize=500,
            callback= lambda *args: self._callback(*args)
        )
        
        self.outstream.start()
        self.goal_freq = C_Major[0]
        self.goal_amplitude = 1
    

    def stop(self):
        self.outstream.stop()


    def run(self):
        for note in PATTERN1["notes"]:
            for pattern in PATTERN1["pattern"]:
                self.goal_freq = NOTES[note + pattern]
                # set_freq(NOTES[note + pattern])
                curSecond = 0
                while curSecond < 1000:
                    # this line will affect the dt, when change, dt factor need to be adjust accordingly
                    self.goal_amplitude = min(1, max(0, (rotMag.value - 0.03)) / 2)
                    # set_volume(min(1, max(0, (rotMag.value - 0.03)) / 2)) 
                    self.dt = (time() - self.prevT) * 1000 * rotMag.value / 0.5
                    # dt = (time() - prevT) * 1000 # ms
                    curSecond += self.dt
                    self.prevT = time()