from multiprocessing import Value

rotMag = Value('d', 0.0)

aMag = Value('d', 0.0)
aDir = Value('i', -1)
aX = Value('d', 0.0)
aY = Value('d', 0.0)
aZ = Value('d', 0.0)

def log():
    while True:
        pass