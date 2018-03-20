import bluetooth
import binascii
import numpy as np
import json

IMU_Address = "00:16:A4:13:37:5E"
initialise_IMU = bytes.fromhex('07 4d 34 64 67 0B')
stop_IMU = bytes.fromhex('07 4d 30 64 67 0B')
com = 'dev/rfcomm0'
port = 1

s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((IMU_Address, port))
bytedata=[]

print(s.recv(15))

s.send(initialise_IMU)

for i in range(1000):
    IMUPacket = s.recv(3)
    #bytedata.append(IMUPacket)                  # Raw format
    bytedata.append(IMUPacket.hex())            # Hex format
    #bytedata.append(int(s.recv(1).hex(),16))    # Int format


s.send(stop_IMU)
s.send(stop_IMU)
s.send(stop_IMU)
s.send(stop_IMU)
s.send(stop_IMU)

print(bytedata)

