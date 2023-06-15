import sounddevice as sd
import soundfile as sf
import numpy as np
from musicgen import tools
from shared import goal_amplitude
import sys

wav_file = 'audios/mix.wav'
min_sample_chunk = 600 # ~13.6ms worth of frame

class MusicGen:
    def __init__(self):
        self.freq = 0

        self.amplitude = 0
        self.amp_duration = 0.15

        self.f = 0

        self.data, self.samplerate = sf.read(wav_file)
        self.d_length = len(self.data)

        self.outstream = sd.OutputStream(
            samplerate=self.samplerate,
            channels=2,
            blocksize=500,
            callback= lambda *args: self._callback(*args)
        )
        
        self.outstream.start()
        goal_amplitude.value = 1

        
    def _callback(self, outdata, frames, time, status):
        if (status):
            print('STATUS: ', status, sys.stderr)

        if self.f + frames > self.d_length:
            remain_length = frames - (self.d_length - self.f)
            new_wave = np.concatenate((self.data[self.f:], self.data[:remain_length]))
            self.f = remain_length
        else:
            new_wave = self.data[self.f:self.f+frames]
            self.f += frames
        
        # handle amplitude change
        amp_env = np.ones(frames)
        if self.amplitude != goal_amplitude.value:
            amp_env = self.get_amp_env(self.amplitude, frames)
            self.amplitude = amp_env[-1]

        target_amp = amp_env.reshape(-1,1) if self.amplitude != goal_amplitude.value else self.amplitude

        outdata[:] = new_wave * target_amp
        # outdata[:] = new_wave.reshape(-1,1) * target_amp
        


    def get_amp_env(self, start_amp, frames):
        dir = 1 if start_amp < goal_amplitude.value else -1
        end_amp = start_amp + (goal_amplitude.value - start_amp) * frames / (tools.fs * self.amp_duration)

        return np.linspace(start_amp, end_amp, frames)
    

    # def get_cross_fade(self, prev_freq, next_freq):
    #     global min_sample_chunk
    #     cycle = round(min_sample_chunk * 10 * next_freq / tools.fs)
    #     cross_wavelengh = round(tools.fs / next_freq * cycle)

    #     time_array = tools.get_time_array(0, cross_wavelengh)
    #     prev_wave = tools.get_wave_by_freq(prev_freq, 1, time_array)
    #     next_wave = tools.get_wave_by_freq(next_freq, 1, time_array)
    #     cross_env = tools.get_crossfade_filter(cross_wavelengh)

    #     cross_wave = prev_wave * cross_env + next_wave * (1 - cross_env)

    #     return cross_wave, cross_wavelengh
