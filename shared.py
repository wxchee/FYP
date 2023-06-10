# _sensor=None
from multiprocessing import Value

yaw = Value('d', 0)
rotDir = Value('i', 0)
rotMag = Value('d', 0.0)

accMag = Value('d', 0.0)

