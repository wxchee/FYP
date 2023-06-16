import sounddevice as sd
import soundfile as sf
import numpy as np
from musicgen import tools
from shared import goal_amplitude, goal_speed
import sys
import librosa
wav_file = 'audios/mix.wav'

min_sample_chunk = 3000

class MusicGen:
    def __init__(self):
        self.freq = 0

        self.amplitude = 0
        self.volume_fade_duration = 0.3

        self.speed = 1

        self.f = 0

        self.data, self.samplerate = sf.read(wav_file)
        self.data_ref = self.data[::self.speed]
        self.d_length = len(self.data_ref)

        self.outstream = sd.OutputStream(
            samplerate=self.samplerate,
            channels=2,
            blocksize=min_sample_chunk,
            callback= lambda *args: self._callback(*args)
        )
        
        self.outstream.start()
        goal_amplitude.value = 1

        
    def _callback(self, outdata, frames, time, status):
        if (status):
            print('STATUS: ', status, sys.stderr)
        print(self.f, self.amplitude)
        prev_f = self.f
        
        if self.speed != goal_speed.value:
            anchor_f = self.f * self.speed
            self.data_ref = np.concatenate((self.data[anchor_f:], self.data[:anchor_f]))
            self.data_ref = self.data_ref[::goal_speed.value]
            self.speed = goal_speed.value
            self.d_length = len(self.data_ref)
            self.f = 0

        if self.f + frames > self.d_length:
            remain_length = frames - (self.d_length - self.f)
            new_wave = np.concatenate((self.data_ref[self.f:], self.data_ref[:remain_length]))
            self.f = remain_length
        else:
            new_wave = self.data_ref[self.f:self.f+frames]
            self.f += frames
        
        # handle amplitude change
        amp_env = np.ones(frames)
        if self.amplitude != goal_amplitude.value:
            amp_env = self.get_amp_env(self.amplitude, frames)
            self.amplitude = round(amp_env[-1], 3)

        if goal_amplitude.value == 0 and round(self.amplitude,2) <= 0.01:
            self.amplitude = 0
            self.f = prev_f
        elif goal_amplitude.value == 1 and round(self.amplitude, 2) >= 0.99:
            self.amplitude = 1

        target_amp = amp_env.reshape(-1,1) if self.amplitude != goal_amplitude.value else self.amplitude

        outdata[:] = new_wave * target_amp
        # outdata[:] = new_wave.reshape(-1,1) * target_amp
        


    def get_amp_env(self, start_amp, frames):
        dir = 1 if start_amp < goal_amplitude.value else -1
        diff = goal_amplitude.value - start_amp
        
        end_amp = start_amp + diff * min(1, frames / (tools.fs * self.volume_fade_duration))
        
        amp_wave = np.linspace(start_amp, end_amp, frames)
        if dir == 1:
            if (end_amp < goal_amplitude.value):
                return amp_wave
        else:
            if (end_amp > goal_amplitude.value):
                return amp_wave

        diff_frames = int(abs(diff * tools.fs * self.volume_fade_duration))

        return np.linspace(start_amp, goal_amplitude.value, diff_frames)
    
