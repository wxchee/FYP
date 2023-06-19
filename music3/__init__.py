import sounddevice as sd
import soundfile as sf
import numpy as np
from musicgen import tools
from shared import goal_amplitude, goal_speed
import sys
import librosa
# from time import time

min_sample_chunk = 3000

class MusicGen:
    def __init__(self):
        self.freq = 0

        self.amplitude = 0
        self.volume_fade_duration = 0.3

        self.speed = 1

        self.f_1 = 0
        self.f_2 = 0
        self.f_3 = 0


        self.wav1, sr1 = sf.read('audios/iso_drum.wav')
        wav2, sr2 = sf.read('audios/iso_piano.wav')
        wav3, sr3 = sf.read('audios/iso_mag_string.wav')

        # print('sr', samplerate, samplerate2, samplerate3)
        print('length', len(self.wav1), len(wav2), len(wav3))
        # 682840 as standard frames length (85355 for drum)
        self.wav2 = np.concatenate((wav2, [wav2[-1]]))
        self.wav3 = wav3[:682840]
        print('new length', len(self.wav1), len(self.wav2), len(self.wav3))
        # data, self.samplerate = librosa.load(wav_file, sr=None, mono=True)
        

        # self.data = librosa.effects.time_stretch(data, rate=1)
        # self.data = data
        goal_amplitude.value = 1

        self.f_global = 0
        self.max_length = max(len(self.wav1), len(self.wav2), len(self.wav3))
        print('maxxxxxxxx', self.max_length)

        self.outstream = sd.OutputStream(samplerate=sr1,channels=2,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 1))
        self.outstream2 = sd.OutputStream(samplerate=sr2,channels=2,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 2))
        self.outstream3 = sd.OutputStream(samplerate=sr3,channels=2,blocksize=min_sample_chunk,callback= lambda *args: self._callback(*args, 3))
        
        self.outstream.start()
        self.outstream2.start()
        self.outstream3.start()
        

    def _callback(self, outdata, frames, time, status, index):
        if (status):
            print('STATUS: ', status, sys.stderr)

        # f_global = int(time.currentTime * 1000) % self.max_length
        f_global = int(time.currentTime * 1000) % len(self.wav1)
        print(index, f_global)
        
        # if index == 1:
        #     if self.f_1 + frames > len(self.wav1):
        #         remain_length1 = frames - (len(self.wav1) - self.f_1)
        #         new_wav = np.concatenate((self.wav1[self.f_1:], self.wav1[:remain_length1]))
        #         self.f_1 = remain_length1
        #     else:
        #         new_wav = self.wav1[self.f_1:self.f_1+frames]
        #         self.f_1 += frames
        # elif index == 2:
        #     if self.f_2 + frames > len(self.wav2):
        #         remain_length2 = frames - (len(self.wav2) - self.f_2)
        #         new_wav = np.concatenate((self.wav2[self.f_2:], self.wav2[:remain_length2]))
        #         self.f_2 = remain_length2
        #     else:
        #         new_wav = self.wav2[self.f_2:self.f_2+frames]
        #         self.f_2 += frames
        # elif index == 3:
        #     if self.f_3 + frames > len(self.wav3):
        #         remain_length3 = frames - (len(self.wav3) - self.f_3)
        #         new_wav = np.concatenate((self.wav3[self.f_3:], self.wav3[:remain_length3]))
        #         self.f_3 = remain_length3
        #     else:
        #         new_wav = self.wav3[self.f_3:self.f_3+frames]
        #         self.f_3 += frames
        if index == 1:
            f_global = int(time.currentTime * 44100) % len(self.wav1)
            if f_global + frames > len(self.wav1):
                remain_length1 = frames - (len(self.wav1) - f_global)
                new_wav = np.concatenate((self.wav1[f_global:], self.wav1[:remain_length1]))
                # self.f_1 = remain_length1
            else:
                new_wav = self.wav1[f_global:f_global+frames]
                # self.f_1 += frames
        elif index == 2:
            f_global = int(time.currentTime * 44100) % len(self.wav2)
            if f_global + frames > len(self.wav2):
                remain_length2 = frames - (len(self.wav2) - f_global)
                new_wav = np.concatenate((self.wav2[f_global:], self.wav2[:remain_length2]))
                # self.f_2 = remain_length2
            else:
                new_wav = self.wav2[f_global:f_global+frames]
                # self.f_2 += frames
        elif index == 3:
            f_global = int(time.currentTime * 44100) % len(self.wav3)
            if f_global + frames > len(self.wav3):
                remain_length3 = frames - (len(self.wav3) - f_global)
                new_wav = np.concatenate((self.wav3[f_global:], self.wav3[:remain_length3]))
                # self.f_3 = remain_length3
            else:
                new_wav = self.wav3[f_global:f_global+frames]
                # self.f_3 += frames
        
        outdata[:] = new_wav




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
    
