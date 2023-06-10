from musicgen import tools
from musicgen.tools import C_Major, STREAM_STATE
import sounddevice as sd
import numpy as np
import sys
from shared import goal_amplitude, goal_freq

prev_time = 0
dt = 0
isPlaying = 0
yawCountDown = 0


# approx. stream requested frame size in rpi: 512
# approx. stream requested frame size in laptop: 400
# hence, make every freq wave sample to bigger than 512
sample_chunk = 600 # ~13.6ms worth of frame

class MusicGen:
    def __init__(self):
        self.freq = 0
        self.wave = tools.get_wave_by_freq(0, 0, np.linspace(0, 1, sample_chunk))
        self.wavelength = sample_chunk

        # goal_freq.value = None

        self.amplitude = 0
        # goal_amplitude.value = 0
        self.amp_duration = 0.15
        
        self.cross_wave = None
        self.cross_wavelengh = 0

        self.phase = 0

        self.state = STREAM_STATE.IDLE
        self.next_state = STREAM_STATE.IDLE

        
        self.outstream = sd.OutputStream(
            samplerate=tools.fs,
            channels=1,
            callback= lambda *args: self._callback(*args)
        )

        
        self.outstream.start()
        goal_freq.value = C_Major[0]
        # self.set_freq(C_Major[0])
        # self.set_volume(1)

        
    def _callback(self, outdata, frames, time, status):
        if (status):
            print('STATUS: ', status, sys.stderr)

        # CROSSFADE state
        if self.state == STREAM_STATE.CROSSFADE: 
            if self.phase + frames > self.cross_wavelengh: # reach the end of the wave
                diff = self.phase + frames - self.cross_wavelengh
                goal_wave, goal_wavelength = self.get_goal(goal_freq.value)
                new_wave = np.concatenate((self.cross_wave[self.phase:self.cross_wavelengh], goal_wave[:diff]))
                self.freq, self.wave, self.wavelength = goal_freq.value, goal_wave, goal_wavelength
                self.state = self.next_state  = STREAM_STATE.IDLE
                self.phase = diff
            else:
                new_wave = self.cross_wave[self.phase:(self.phase + frames)]
                self.phase += frames
        
        # IDLE state
        else: 
            if self.phase + frames > self.wavelength: # reach the end of the wave
                diff = self.phase + frames - self.wavelength
                if goal_freq.value != self.freq:
                    self.cross_wave, self.cross_wavelengh = self.get_cross_fade(self.freq, goal_freq.value)
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
        if self.amplitude != goal_amplitude.value:
            amp_env = self.get_amp_env(self.amplitude, frames)
            self.amplitude = amp_env[-1]

        target_amp = amp_env.reshape(-1,1) if self.amplitude != goal_amplitude.value else self.amplitude
        outdata[:] = new_wave.reshape(-1,1) * target_amp

        # print('on callback')

    # def set_freq(self, new_freq):
    #     goal_freq.value = new_freq



    def get_goal(self, goal_freq):
        global sample_chunk
        cycle = round(sample_chunk * goal_freq / tools.fs)
        goal_wavelength = round(tools.fs / goal_freq * cycle)
        new_time_array = tools.get_time_array(0, goal_wavelength)
        goal_wave = tools.get_wave_by_freq(goal_freq, 1, new_time_array)

        return goal_wave, goal_wavelength



    # def set_volume(self, new_amp):
    #     goal_amplitude.value = new_amp


    def get_amp_env(self, start_amp, frames):
        dir = 1 if start_amp < goal_amplitude.value else -1
        end_amp = start_amp + (goal_amplitude.value - start_amp) * frames / (tools.fs * self.amp_duration)

        return np.linspace(start_amp, end_amp, frames)
    

    def get_cross_fade(self, prev_freq, next_freq):
        global sample_chunk
        cycle = round(sample_chunk * 10 * next_freq / tools.fs)
        cross_wavelengh = round(tools.fs / next_freq * cycle)

        time_array = tools.get_time_array(0, cross_wavelengh)
        prev_wave = tools.get_wave_by_freq(prev_freq, 1, time_array)
        next_wave = tools.get_wave_by_freq(next_freq, 1, time_array)
        cross_env = tools.get_crossfade_filter(cross_wavelengh)

        cross_wave = prev_wave * cross_env + next_wave * (1 - cross_env)

        return cross_wave, cross_wavelengh
        