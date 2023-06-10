from sensor import Sensor
from musicgen import MusicGen
from multiprocessing import Process, cpu_count
# import threading
from control import control

class MusicalBall:
  def __init__(self):
    self.sensor = Sensor()
    self.mg = MusicGen()

  def start(self):
    print('start musical ball')
    
    print('cpu count', cpu_count())

    process_sensor = Process(target=self.sensor.run)
    process_control = Process(target=control.run)
    
    process_sensor.start()
    process_control.start()

    try:
      process_sensor.join()
      process_control.join()
    except KeyboardInterrupt:
      process_sensor.terminate()
      process_control.terminate()

if __name__ == '__main__':
  mball = MusicalBall()
  mball.start()