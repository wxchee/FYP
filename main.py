from sensor import Sensor
from multiprocessing import Process, cpu_count
from control import control
# from shared import log

class MusicalBall:
  def __init__(self):
    self.sensor = Sensor()

  def start(self):
    print('start musical ball')
    
    print('cpu count', cpu_count())

    process_sensor = Process(target=self.sensor.run)
    process_control = Process(target=control.run)

    # process_log = Process(target=log)

    process_sensor.start()
    process_control.start()

    # process_log.start()

    try:
      process_sensor.join()
      process_control.join()

      # process_log.join()
    except KeyboardInterrupt:
      process_sensor.terminate()
      process_control.terminate()

      # process_log.terminate()

if __name__ == '__main__':
  mball = MusicalBall()
  mball.start()