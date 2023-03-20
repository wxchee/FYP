from sensor import Sensor
import vars
from musicgen import MusicGen
import threading
import control
class MusicalBall:
  def __init__(self):
    vars.sensor = Sensor()
    self.music = MusicGen()

  def start(self):
    print('start musical ball')
    
    thread_sensor = threading.Thread(target=vars.sensor.run)
    thread_music = threading.Thread(target=control.run, args=(self.music, vars.sensor))
    
    thread_sensor.start()
    thread_music.start()

    thread_sensor.join()
    thread_music.join()

if __name__ == '__main__':
  mball = MusicalBall()
  mball.start()