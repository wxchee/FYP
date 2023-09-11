from multiprocessing import Value

yaw = Value('d', 0)
rotDir = Value('i', 0)
rotMag = Value('d', 0.8)

aMag = Value('d', 0.0)
aX = Value('d', 0.0)
aY = Value('d', 0.0)
aZ = Value('d', 0.0)

def log():
    while True:
        pass