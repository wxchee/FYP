from sensor import Sensor
import vars
from musicgen import MusicGen
import threading

class MusicalBall:
  def __init__(self):
    vars.sensor = Sensor()
    self.music = MusicGen()

  def start(self):
    print('start musical ball')
    
    thread_sensor = threading.Thread(target=vars.sensor.run)
    thread_music = threading.Thread(target=self.music.run)

    thread_sensor.start()
    thread_music.start()

    thread_sensor.join()
    thread_music.join()


if __name__ == '__main__':
  mball = MusicalBall()
  mball.start()