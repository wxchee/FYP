import pyaudio
import numpy as np
from time import time,sleep

# note_freqs = [261.63 * pow(2, i/12) for i in range(12)]
note_freqs = [
    261.63,     # C     
    277.187,    # C#
    293.67,     # D
    311.132,    # D#
    329.633,    # E
    349.234,    # F
    370.001,    # F#
    392.002,    # G
    415.312,    # G#
    440.007,    # A
    466.172,    # A#
    493.892     # B
]

fs=44100
CHANNELS = 2

freq=100
new_freq = 100
phase = 0

p = pyaudio.PyAudio()

TT = time()

def callback(in_data, frame_count, time_info, status):
    global TT, phase, freq, new_freq

    if freq != new_freq:
        phase = 2*np.pi * TT * (freq-new_freq) + phase
        freq = new_freq

    wave = np.sin(phase + + 2 * np.pi * freq * (TT + np.arange(frame_count) / float(fs)))
    data = np.zeros(wave.shape[0] * 2, dtype=np.float32)
    data[0::2] = wave
    data[1::2] = wave
    TT += frame_count / float(fs)

    return (data, pyaudio.paContinue)

stream = p.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=fs,
                output=True,
                stream_callback=callback)

stream.start_stream()

i=0
dir=1

try:
    while True:
        new_freq = note_freqs[i]
        i = (i+1) % len(note_freqs)
        sleep(0.5)
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()