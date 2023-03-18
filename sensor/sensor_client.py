import socket
import sys
sys.path.append('../')
# from time import sleep
from const import SERVER_ADDR_PORT, BUFFER_SIZE

from sense_hat import SenseHat
sense = SenseHat()

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

try:
	while (True):
		# acc = sense.get_accelerometer_raw()
		orien = sense.get_orientation()
		pitch = round(orien['pitch'])
		roll = round(orien['roll'])
		yaw = round(orien['yaw'])

		accMsg = '{} {} {}'.format(pitch, roll, yaw)
		UDPClientSocket.sendto(accMsg.encode('UTF-8'), SERVER_ADDR_PORT)
		
		recData, revAddr = UDPClientSocket.recvfrom(BUFFER_SIZE)
		print('receive: {}'.format(recData.decode('UTF-8')))
		# sleep(1)
except KeyboardInterrupt:
	print("close sensor client socket.")
	UDPClientSocket.close()
