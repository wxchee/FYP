from const import SERVER_ADDR_PORT, BUFFER_SIZE
import socket

class SensorReceiver:
    def __init__(self):
        self._socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self._socket.bind(SERVER_ADDR_PORT)

    def run(self, set_orientation):
        print("start sensor server")
        while True:
            clientMsg, clientAddr = self._socket.recvfrom(BUFFER_SIZE)
            pitch, roll, yaw = clientMsg.decode().split(' ')
            set_orientation(pitch, roll, yaw)
            # print('{} {} {}'.format(pitch, roll, yaw))
            self._socket.sendto(str.encode('Received.'), clientAddr)