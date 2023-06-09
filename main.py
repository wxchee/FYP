from sensor import Sensor
import vars
from musicgen import MusicGen
from multiprocessing import Process, cpu_count
# import threading
import control

class MusicalBall:
  def __init__(self):
    vars.sensor = Sensor()
    # self.music = MusicGen()

  def start(self):
    print('start musical ball')
    
    # thread_sensor = threading.Thread(target=vars.sensor.run)
    # thread_music = threading.Thread(target=control.run, args=(self.music, vars.sensor))
    # thread_sensor.start()
    # thread_music.start()

    # thread_sensor.join()
    # thread_music.join()
    print('cpu count', cpu_count())

    process_sensor = Process(target=vars.sensor.run)
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