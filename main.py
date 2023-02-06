import socket
from config import SERVER_ADDR_PORT, BUFFER_SIZE


serverMsg = 'Hello from server'

bytesToSend = str.encode(serverMsg)

UDPServerSocket =  socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.bind(SERVER_ADDR_PORT)

print('UDP Server up and listening')

while(True):
  clientMsg, clientAddr = UDPServerSocket.recvfrom(BUFFER_SIZE)
  x, y, z = clientMsg.decode().split(' ')
  print('Sensor[{}]: {} {} {}'.format(clientAddr, x, y, z))

  UDPServerSocket.sendto(bytesToSend, clientAddr)
  