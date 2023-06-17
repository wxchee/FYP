# _sensor=None
from multiprocessing import Value

yaw = Value('d', 0)
rotDir = Value('i', 0)
rotMag = Value('d', 0.8)

accMag = Value('d', 0.0)

goal_amplitude = Value('d', 0.0)
goal_freq = Value('d', 0.0)

goal_speed = Value('d', 1.0)

def set_volume(v):
    goal_amplitude.value = v

def set_freq(f):
    goal_freq.value = f

def set_speed(s):
    goal_speed.value = min(1.2, max(0.6, s))

def log():
    while True:
        pass
        # print('yaw', yaw.value)
        # print('rotMag', rotMag.value)
        # print(yaw.value, rotDir.value, rotMag.value, accMag.value, goal_amplitude.value, goal_freq.value)