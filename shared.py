# _sensor=None
from multiprocessing import Value

yaw = Value('d', 0)
rotDir = Value('i', 0)
rotMag = Value('d', 0.0)

accMag = Value('d', 0.0)

goal_amplitude = Value('d', 0.0)
goal_freq = Value('d', 0.0)

def set_volume(v):
    goal_amplitude.value = v

def set_freq(f):
    goal_freq.value = f