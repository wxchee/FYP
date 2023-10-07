import socket
import sys
sys.path.append('/home/wxchee/fyp/')

from const import SERVER_ADDR_PORT, BUFFER_SIZE

from sense_hat import SenseHat
sense = SenseHat()
sense.low_light = True
sense.set_imu_config(False, True, True)

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

try:
	while (True):
		gX, gY, gZ = sense.get_gyroscope_raw().values()
		aX, aY, aZ = sense.get_accelerometer_raw().values()

		accMsg = '{:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f}'.format(gX, gY, gZ, aX, aY, aZ)
		UDPClientSocket.sendto(accMsg.encode('UTF-8'), SERVER_ADDR_PORT)
		# print(accMsg)

		recData, revAddr = UDPClientSocket.recvfrom(BUFFER_SIZE)
		print('receive: {}'.format(recData.decode('UTF-8')))
		# sleep(1)
except KeyboardInterrupt:
	print("close sensor client socket.")
	UDPClientSocket.close()
