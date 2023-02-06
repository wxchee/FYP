import socket
import sys
sys.path.append('../')
# from time import sleep
from config import SERVER_ADDR_PORT, BUFFER_SIZE

from sense_hat import SenseHat
sense = SenseHat()

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while (True):
	acc = sense.get_accelerometer_raw()
	x = round(acc['x'], 4)
	y = round(acc['y'], 4)
	z = round(acc['z'], 4)
	accMsg = '{} {} {}'.format(x, y, z)
	data = accMsg.encode('UTF-8')
	UDPClientSocket.sendto(data, SERVER_ADDR_PORT)
	
	recData, revAddr = UDPClientSocket.recvfrom(BUFFER_SIZE)
	recMsg = recData.decode('UTF-8')
	print('receive: {}'.format(recMsg))
	# sleep(1)
