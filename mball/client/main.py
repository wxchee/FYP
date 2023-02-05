import socket
from time import sleep
from os import path
# from get_ip import get_ip

ROOT_DIR = path.dirname(__file__)

localIP = ''
RPI_IP = ''
with open(path.join(ROOT_DIR, '..', 'IP_host.txt')) as f:
  localIP = f.readline().strip('\n')
with open(path.join(ROOT_DIR, '..', 'IP_client.txt')) as f:
	RPI_IP = f.readline().strip('\n')
# print('test: {}'.format(get_ip()))

# localIP = get_ip()
print(localIP)
print(RPI_IP)

hostAddrPort = (RPI_IP, 4010)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

byteSize = 1024

dummyMsg = '{}-{}-{}'.format(20,1,2)

while (True):
	data = dummyMsg.encode('UTF-8')
	UDPClientSocket.sendto(data, hostAddrPort)
	
	recData, revAddr = UDPClientSocket.recvfrom(byteSize)
	recMsg = recData.decode('UTF-8')
	print('receive: {}'.format(recMsg))
	sleep(1)
