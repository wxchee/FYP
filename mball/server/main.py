import socket
from os import path

localIP = ''
ROOT_DIR = path.dirname(__file__)
with open(path.join(ROOT_DIR, './../IP_client.txt')) as f:
  localIP = f.readline()

# localIP = '192.168.68.119'
localPort = 4010
bufferSize = 1024

serverMsg = 'Hello from server'

bytesToSend = str.encode(serverMsg)

UDPServerSocket =  socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.bind((localIP, localPort))

print('UDP Server up and listening')

while(True):
  clientMsg, clientAddr = UDPServerSocket.recvfrom(bufferSize)

  print('Msg from client[{}]: {}'.format(clientAddr, clientMsg.decode()))

  UDPServerSocket.sendto(bytesToSend, clientAddr)
  