# _sensor=None
from multiprocessing import Value

yaw = Value('d', 0)
rotDir = Value('i', 0)
rotMag = Value('d', 0.8)

aMag = Value('d', 0.0)
aX = Value('d', 0.0)
aY = Value('d', 0.0)
aZ = Value('d', 0.0)

# track volumes
volX = Value('d', 0.0)
volY = Value('d', 0.0)
volZ = Value('d', 0.0)


goal_amplitude = Value('d', 0.0)
goal_freq = Value('d', 0.0)

goal_speed = Value('d', 1.0)

def set_volume(v):
    goal_amplitude.value = v

def set_freq(f):
    goal_freq.value = f

def set_speed(s):
    goal_speed.value = min(1.2, max(0.6, s))

def get_vol(index):
    if index == 0:
        return volX.value
    if index == 1:
        return volY.value
    if index == 2:
        return volZ.value

def log():
    while True:
        pass
        # print('yaw', yaw.value)
        # print('rotMag', rotMag.value)
        # print(aX.value, aY.value, aZ.value)
        # print('vx',volX.value, 'vy',volY.value, 'vz',volZ.value)
        # print(yaw.value, rotDir.value, rotMag.value, aMag.value, goal_amplitude.value, goal_freq.value)