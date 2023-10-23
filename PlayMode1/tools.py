import numpy as np
from enum import Enum

class STREAM_STATE(Enum):
    IDLE = 0
    CROSSFADE = 1

# NOTES = [261.63 * 2**(i/12) for i in range(13)]
NOTES = np.array([ # 24
    261.63,     # C4     
    277.187,    # C#
    293.67,     # D
    311.132,    # D#
    329.633,    # E
    349.234,    # F
    370.001,    # F#
    392.002,    # G
    415.312,    # G#
    440,        # A
    466.172,    # A#
    493.892,    # B,
    523.25,      # C5
    554.375,    # C5#
    587.339,    # D5
    622.264,    # D5#
    659.266,    # E5
    698.468,    # F5
    740.001,    # F5#
    784.004,    # G5
    830.623,    # G5#
    880.015,    # A5
    932.343,    # A5#
    987.783,    # B5
    1046.52    # C6
])


C_Major = NOTES[[0, 2, 4, 5, 7, 9, 11, 12]]

PATTERN1 = {
    "notes": [12, 7, 9, 4, 5, 0, 5, 7],
    "pattern": [0, 4, 7, 4, 9, 4, 7, 4]
}

fs = 44100

default_duration = 0.5

def get_time_array(start_frame, frames) -> np.array:
    return np.linspace(start_frame/fs, (start_frame + frames)/fs, frames, endpoint=False)

def get_fadeout_env(duration) -> np.array:
    return np.linspace(1, 0, int(duration * fs))

def get_crossfade_filter(frames) -> np.array:
    # fade_frames = int(duration * fs)
    fade_frames = int (0.5 * frames)
    return np.concatenate((
        # np.linspace(0, 1, fade_frames),
        np.ones(frames - fade_frames),
        np.linspace(1, 0, fade_frames)
    )
    )

def get_wave_by_freq(freq=C_Major[0], amp=1, times=0) -> np.array:
    return amp * np.sin(2*np.pi*freq*times)

