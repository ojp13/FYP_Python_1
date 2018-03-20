import time
import numpy as np
import serial
import io
import bluetooth
import socket
import sys
    
ADDR_R_43 = "00:00:39:85:16:03" #right 43
ADDR_L_43 = "00:00:39:DA:C6:AD" #left 43


class Insole(object):
    
    
    def __init__(self, side = 'right', size = 43, **kwargs):
        if size == 43:
            self.data_size = 70
            if side == 'right':
                self.com = '/dev/rfcomm1' #'right'
                self.addr = ADDR_R_43
            else: 
                self.com = '/dev/rfcomm0' #left
                self.addr = ADDR_L_43
        elif size == 40:
            self.data_size = 68
            if side == 'right':
                self.addr = ADDR_R_40
            else: 
                self.addr = ADDR_L_40
        self.size = size
        self.data_offset = np.zeros((self.data_size))
        self.data = self.data_offset
    
    def connect_bt(self):
        port = 5       
        self.sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.sock.connect((self.addr, port))    
    
    def start_data_bt(self):
        self.sock.send("start_sending")
        
    def stop_data_bt(self):
        self.sock.send("stop_sending")
      
      def read_data_bt(self):
        try:
            data = []
            nb_bytes = 0
            while True:               
                    datum = self.sock.recv(1, socket.MSG_PEEK)
                    if len(datum)>0:
                        datum = self.sock.recv(1).encode("hex")
                  
                    else:
                        continue
                    data = np.hstack([data, datum])
                    nb_bytes = nb_bytes +1
                    if datum == '00' and nb_bytes == (self.data_size +5):
                        data = np.array([int(x) for x in bytearray.fromhex(data[4:75])])
                        data[data<0]=0
                        data[data>224]=0
                        return data
                    elif datum == '00' and nb_bytes > (self.data_size +5):
                        data = []
                        nb_bytes = 0
                          
        except....
               
