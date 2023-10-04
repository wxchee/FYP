from multiprocessing import Value
from tools import C_Major

mode = Value("i", 0)

yaw = Value('d', 0)
rotDir = Value('i', 0)
rotMag = Value('d', 0.8)

aMag = Value('d', 0.0)
aX = Value('d', 0.0)
aY = Value('d', 0.0)
aZ = Value('d', 0.0)

# Music1 only shared variables
goalFreq = Value('d', C_Major[0])
goalAmp = Value('d', 0.0) 

def resetMusic1():
    goalFreq.value = C_Major[0]
    goalAmp.value = 0.0

def log():
    while True:
        pass