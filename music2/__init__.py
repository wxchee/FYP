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
        self.anchor_f = 0

        # self.data, self.samplerate = sf.read(wav_file)
        data, self.samplerate = librosa.load(wav_file, sr=None, mono=True)
        

        # self.data = librosa.effects.time_stretch(data, rate=1)
        self.data = data

        self.data_refs = {}
        for rate in np.arange(0.6, 1.3, 0.1):
            self.data_refs[round(rate,1)] = librosa.effects.time_stretch(data, rate=round(rate,1))
            print(round(rate, 1), self.data_refs[round(rate,1)])
            
        self.data_ref = self.data
        self.init_length = len(self.data)

        self.outstream = sd.OutputStream(
            samplerate=self.samplerate,
            channels=1,
            blocksize=min_sample_chunk,
            callback= lambda *args: self._callback(*args)
        )
        
        self.outstream.start()
        goal_amplitude.value = 1

        
    def _callback(self, outdata, frames, time, status):
        if (status):
            print('STATUS: ', status, sys.stderr)
            
        prev_f = self.f
        
        # frames_s = frames
        # int(frames * goal_speed.value)
        
        if (self.speed != goal_speed.value):
            # self.anchor_f = int(self.f )
            data_new_start = np.concatenate((self.data[self.anchor_f:], self.data[:self.anchor_f]))
            # self.data_ref = librosa.effects.time_stretch(data_new_start, rate=goal_speed.value)
            self.data_ref = self.data_refs[goal_speed.value]
            self.f = int(self.f / goal_speed.value)
            # self.f = 0
            
            self.speed = goal_speed.value

        # if goal_speed.value != 1:
        if self.f + frames > len(self.data_ref):
            remain_length = frames - (len(self.data_ref) - self.f)
            new_wave = np.concatenate((self.data_ref[self.f:], self.data_ref[:remain_length]))
            self.f = remain_length
        else:
            new_wave = self.data_ref[self.f:self.f+frames]
            self.f += frames
        # print(len(new_wave), frames, goal_speed.value)

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

        # outdata[:] = new_wave * target_amp
        outdata[:] = new_wave.reshape(-1,1) * target_amp
        
        # print(self.f, self.amplitude)


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
    
