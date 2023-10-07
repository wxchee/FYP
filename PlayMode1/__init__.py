from time import time, sleep
import numpy as np
import sys
from multiprocessing import Value

from shared import rotMag
from PlayMode1.tools import get_wave_by_freq, get_time_array, get_crossfade_filter, C_Major, STREAM_STATE, PATTERN1, NOTES


# shared variable between play mode process and control process
# play mode process - monitoring rotation speed and update goalFreq and goalAmp
# control process - possess outstream threads that read goalFreq and goalAmp
goalFreq = Value('d', C_Major[0])
goalAmp = Value('d', 0.0) 

def resetPlayMode1():
    goalFreq.value = C_Major[0]
    goalAmp.value = 0.0

SAMPLE_RATE_M1 = 44100

# fix the frames request size during outstream's callback
min_sample_chunk = 600 # ~13.6ms worth of frame

class PlayMode1:
    def __init__(self):
        self.dt = 0
        self.prevT = 0

        self.freq = 0
        self.wave = get_wave_by_freq(0, 0, np.linspace(0, 1, min_sample_chunk))
        self.wavelength = min_sample_chunk

        self.amplitude = 0
        self.amp_duration = 0.15

        self.cross_wave = None
        self.cross_wavelengh = 0

        self.phase = 0

        self.state = STREAM_STATE.IDLE
        self.next_state = STREAM_STATE.IDLE

        self.outstream = None
        
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
        cycle = round(min_sample_chunk * goal_freq / SAMPLE_RATE_M1)
        goal_wavelength = round(SAMPLE_RATE_M1 / goal_freq * cycle)
        new_time_array = get_time_array(0, goal_wavelength)
        goal_wave = get_wave_by_freq(goal_freq, 1, new_time_array)

        return goal_wave, goal_wavelength


    def get_amp_env(self, start_amp, frames):
        dir = 1 if start_amp < goalAmp.value else -1
        end_amp = start_amp + (goalAmp.value - start_amp) * frames / (SAMPLE_RATE_M1 * self.amp_duration)

        return np.linspace(start_amp, end_amp, frames)
    

    def get_cross_fade(self, prev_freq, next_freq):
        global min_sample_chunk
        cycle = round(min_sample_chunk * 10 * next_freq / SAMPLE_RATE_M1)
        cross_wavelengh = round(SAMPLE_RATE_M1 / next_freq * cycle)

        time_array = get_time_array(0, cross_wavelengh)
        prev_wave = get_wave_by_freq(prev_freq, 1, time_array)
        next_wave = get_wave_by_freq(next_freq, 1, time_array)
        cross_env = get_crossfade_filter(cross_wavelengh)

        cross_wave = prev_wave * cross_env + next_wave * (1 - cross_env)

        return cross_wave, cross_wavelengh

    def start(self):
        # sounddevice has issue working with multiprocessing's Process when import onto global level
        # solution: import within function scope 
        # https://blog.csdn.net/NormanBeita/article/details/106499473
        import sounddevice as sd
        self.dt = 0
        self.prevT = time()
        
        self.outstream = sd.OutputStream(
            samplerate=SAMPLE_RATE_M1,
            channels=1,
            blocksize=500, # must be smaller than min_sample_chunk
            callback= lambda *args: self._callback(*args)
        )

        self.outstream.start()

    def run(self):
        dt = 0
        prevT = 0
        curSecond = 0
        pi = ni = 0

        while True:
            print('run m1')
            if curSecond >= 1000:
                curSecond = 0
                if pi == len(PATTERN1["pattern"]) - 1:
                    ni = (ni + 1) % len(PATTERN1["notes"])

                pi = (pi + 1) % len(PATTERN1["pattern"])

                goalFreq.value = NOTES[PATTERN1["notes"][ni] + PATTERN1["pattern"][pi]]


            goalAmp.value = min(1, max(0, (rotMag.value - 0.03)) / 2)

            dt = (time() - prevT) * 1000 * rotMag.value / 0.5
            curSecond += dt
            prevT = time()

            sleep(0.1)

    def stop(self):
        self.outstream.close()
        resetPlayMode1()