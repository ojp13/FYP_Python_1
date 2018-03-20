import bluetooth
import matplotlib.pyplot as plt
import numpy as np
from twos_Comp import twos_comp

IMU_Address = "00:16:A4:13:37:5E"
initialise_IMU = bytes.fromhex('07 4d 34 64 67 0B')
stop_IMU = bytes.fromhex('07 4d 30 64 67 0B')

port = 1

start_byte1 = 'dd'
start_byte2 = 'aa'
start_byte3 = '55'
start_bytes = start_byte1 + start_byte2 + start_byte3
packet_length = 41      # 41 bytes of data sent each sample
num_samples = 5000

com = 'dev/rfcomm0'   # not sure if this line is important for bt or not
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((IMU_Address, port))

byte_data_whole = np.zeros([num_samples, packet_length-3], dtype = int)
xgyro = []
ygyro = []
zgyro = []
lastbyte = []

print(s.recv(15))

s.send(initialise_IMU)

k = 0
while k < num_samples:
    IMUPacket = s.recv(3)
    # print(IMUPacket.hex())
    # checking if the packet is the 3 start bytes
    if IMUPacket.hex() == start_bytes:
        # if it is, record the next 38 bytes
        for j in range (0, packet_length-3):
            byte_data_whole[k,j] = int(s.recv(1).hex(),16)
        xgyro.append(twos_comp(byte_data_whole[k,2] | (byte_data_whole[k,3] << 8), 16))
        ygyro.append(twos_comp(byte_data_whole[k,4] | (byte_data_whole[k,5] << 8), 16))
        zgyro.append(twos_comp(byte_data_whole[k,6] | (byte_data_whole[k,7] << 8), 16))
        lastbyte.append(byte_data_whole[k,37])
        # k iterates every time we gather a sample
        k += 1

#print(lastbyte)

plt.scatter(range(len(xgyro)), xgyro, s = 1)
plt.scatter(range(len(ygyro)), ygyro, s = 1)
plt.scatter(range(len(zgyro)), zgyro, s = 1)
plt.show()

