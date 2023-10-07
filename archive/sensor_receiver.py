from const import SERVER_ADDR_PORT, BUFFER_SIZE
import socket

class SensorReceiver:
    def __init__(self):
        self._socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self._socket.bind(SERVER_ADDR_PORT)

    def run(self, set_gyro, set_acc):
        print("start sensor server")
        try:
            while True:
                clientMsg, clientAddr = self._socket.recvfrom(BUFFER_SIZE)
                # pitch, roll, yaw = clientMsg.decode().split(' ')
                # pitch, roll, yaw, gX, gY, gZ, aX, aY, aZ = clientMsg.decode().split(' ')
                gX, gY, gZ, aX, aY, aZ = clientMsg.decode().split(' ')
                
                # set_orientation(float(pitch), float(roll), float(yaw))
                set_gyro(float(gX), float(gY), float(gZ))
                set_acc(float(aX), float(aY), float(aZ))

                # print('re: {} {} {} {} {} {}'.format(gX, gY, gZ, aX, aY, aZ))
                self._socket.sendto(str.encode('Received.'), clientAddr)
        except KeyboardInterrupt:
            print("close sensor receiver socket.")
            self._socket.close()