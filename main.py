from sensor import Sensor
from multiprocessing import Process, cpu_count
import control
from report_ref import thtest

class MusicalBall:
  def __init__(self):
    self.sensor = Sensor()

  def start(self):
    print('start musical ball')
    
    print('cpu count', cpu_count())

    process_sensor = Process(target=self.sensor.run)
    # process_control = Process(target=control.run)
    process_th = Process(target=thtest.run)

    process_sensor.start()
    # process_control.start()
    process_th.start()

    try:
      process_sensor.join()
      # process_control.join()
      process_th.join()
      
    except KeyboardInterrupt:
      process_sensor.terminate()
      # process_control.terminate()
      process_th.terminate()

if __name__ == '__main__':
  mball = MusicalBall()
  mball.start()