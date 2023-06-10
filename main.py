from sensor import Sensor
# import shared
from musicgen import MusicGen
from multiprocessing import Process, cpu_count
# import threading
from control import control

class MusicalBall:
  def __init__(self):
    self.sensor = Sensor()

  def start(self):
    print('start musical ball')
    
    print('cpu count', cpu_count())

    process_sensor = Process(target=self.sensor.run)
    process_music = Process(target=control.run)
    process_sensor.start()
    process_music.start()

    try:
      process_sensor.join()
      process_music.join()
    except KeyboardInterrupt:
      process_sensor.terminate()
      process_music.terminate()

if __name__ == '__main__':
  mball = MusicalBall()
  mball.start()