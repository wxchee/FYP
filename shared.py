from multiprocessing import Value

aMag = Value('d', 0.0)
aDir = Value('i', -1)
aX = Value('d', 0.0)
aY = Value('d', 0.0)
aZ = Value('d', 0.0)

rotMag = Value('d', 0.0)
rX = Value('d', 0.0)
rY = Value('d', 0.0)
rZ = Value('d', 0.0)

def getRotMag(self):
    if (aDir.value == 1 or aDir.value == 2):
        return abs(rX.value)
    elif (aDir.value == 3 or aDir.value == 4):
        return abs(rY.value)
    elif (aDir.value == 5 or aDir.value == 6):
        return abs(rZ.value)
    
    return -1



