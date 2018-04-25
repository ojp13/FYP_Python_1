import matplotlib.pyplot as plt
from matplotlib.axes import Axes as ax
import numpy as np
from twos_Comp import twos_comp
import socket

IMU_Address = "00:16:A4:13:37:5E"
initialise_IMU = bytes.fromhex('07 4d 34 64 67 0B')
stop_IMU = bytes.fromhex('07 4d 30 64 67 0B')

listen_addr = ("",65000)

port = 1

start_byte1 = 'dd'
start_byte2 = 'aa'
start_byte3 = '55'
start_bytes = start_byte1 + start_byte2 + start_byte3
packet_length = 41      # 41 bytes of data sent each sample
num_samples = 5000

com = 'dev/rfcomm0'   # not sure if this line is important for bt or not

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(listen_addr)
s.listen(15)
