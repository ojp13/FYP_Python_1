import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("Tkagg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt

import bluetooth
import pickle
import threading
import pandas as pd
import numpy as np
import math
import time
from twos_Comp import twos_comp

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use("ggplot")

f = plt.figure()

#Constants to keep track of settings

#Bluetooth Settings
IMU_Address = "00:16:A4:13:37:5E"
initialise_IMU = bytes.fromhex('07 4d 34 64 67 0B')
stop_IMU = bytes.fromhex('07 4d 30 64 67 0B')
port = 1
start_byte1 = 'dd'
start_byte2 = 'aa'
start_byte3 = '55'
start_Bytes = start_byte1 + start_byte2 + start_byte3
packet_length = 41      # 41 bytes of data sent each sample
com = 'dev/rfcomm0'   # not sure if this line is important for bt or not
BT_Object = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

#Constants to allow for movement of data in app
BT_isRecording = False
IMU_Data = [[],[],[],[],[],[]]
timestamp = []

def animate(i):
    
    global IMU_Data
    global timestamp

    #Setting up subplots for plotting bluetooth data
    #Plot for linear accelerations, 9x6 grid, start at top left
    a = plt.subplot2grid((9,6), (0,0), rowspan=3, colspan=6)
    plt.setp(a.get_xticklabels(), visible=False)
    a.set_ylabel("Linear Acc.")
    a.set_ylim([-32768,32768])
    #Plot for angluar accelerations, start in 4th row, have same x axis as first plot
    a2 = plt.subplot2grid((9,6), (3,0), sharex=a, rowspan=3, colspan=6)
    plt.setp(a2.get_xticklabels(), visible=False)
    a2.set_ylabel("Angular Acc.")
    a2.set_ylim([-32768,32768])
    #Plot for MMG readings
    a3 = plt.subplot2grid((9,6), (6,0), sharex=a, rowspan=3, colspan=6)
    a3.set_ylabel("MMG Signals")
    a3.set_ylim([-32768,32768])
    a3.set_xlabel("Time")

    a.clear()
    a2.clear()
    a3.clear()

    const = 1000
    if len(IMU_Data[0]) < const:
        a.scatter(timestamp[:], IMU_Data[0][:], label="x component", s=10)
        a.scatter(timestamp[:], IMU_Data[1][:], label="y component", s=10)
        a.scatter(timestamp[:], IMU_Data[2][:], label="z component", s=10)
        a2.scatter(timestamp[:], IMU_Data[3][:], label="x component", s=10)
        a2.scatter(timestamp[:], IMU_Data[4][:], label="y component", s=10)
        a2.scatter(timestamp[:], IMU_Data[5][:], label="z component", s=10)
    else:        
        a.scatter(timestamp[-const:], IMU_Data[0][-const:], label="x component", s=10)
        a.scatter(timestamp[-const:], IMU_Data[1][-const:], label="y component", s=10)
        a.scatter(timestamp[-const:], IMU_Data[2][-const:], label="z component", s=10)
        a2.scatter(timestamp[-const:], IMU_Data[3][-const:], label="x component", s=10)
        a2.scatter(timestamp[-const:], IMU_Data[4][-const:], label="y component", s=10)
        a2.scatter(timestamp[-const:], IMU_Data[5][-const:], label="z component", s=10)
        
def bluetooth_Connect(BT_Object, IMU_Address, port):

    try:
        BT_Object.connect((IMU_Address, port))
        print(BT_Object.recv(15))

    except Exception as e:
        print("Bluetooth connection failed: ",e)

#Generates a sin wave to plot        
def practice_changeRecording(BT_Object, initialise_IMU):
    global BT_isRecording

    if BT_isRecording:
        BT_isRecording = False
    else:
        BT_isRecording = True
        t = threading.Thread(target=read_generated_Data, name="read_Thread", daemon=True)
        t.start()

    print(BT_isRecording)

def BT_changeRecording(BT_Object, initialise_IMU):
    global BT_isRecording

    if BT_isRecording:
        BT_isRecording = False
    else:
        BT_isRecording = True
        t = threading.Thread(target=read_Bluetooth_Data,
                             args=(BT_Object, initialise_IMU, start_Bytes, packet_length),
                             name="read_Thread", daemon=True)
        t.start()

    print(BT_isRecording)


def read_generated_Data():
    global IMU_Data
    global timestamp
    
    inc = 0
    while BT_isRecording:
        IMU_Data[0].append(math.sin(inc/(2*math.pi)))
        IMU_Data[1].append(math.sin((inc + (10*math.pi/3))/(2*math.pi)))
        IMU_Data[2].append(math.sin((inc + (20*math.pi/3))/(2*math.pi)))
        IMU_Data[3].append(math.sin(inc/(2*math.pi)))
        IMU_Data[4].append(math.sin((inc + (10*math.pi/3))/(2*math.pi)))
        IMU_Data[5].append(math.sin((inc + (20*math.pi/3))/(2*math.pi)))
        timestamp.append(inc)
        time.sleep(0.005)
        inc += 1
        
def read_Bluetooth_Data(BT_Object, initialise_IMU, start_Bytes, packet_length):
    global IMU_Data
    global timestamp
    
    BT_Object.send(initialise_IMU)
    
    packet = np.zeros(packet_length-3, dtype="int")

    #Incrementer to append to timestamp, which is the x axis for our plots
    inc = 0
    
    while BT_isRecording:

        IMUPacket = BT_Object.recv(3)
        
        if IMUPacket.hex() == start_Bytes:
            # if it is, record the next 38 bytes
            for j in range (0, packet_length-3):
                packet[j] = int(BT_Object.recv(1).hex(),16)
            IMU_Data[0].append(twos_comp(packet[14] | (packet[15] << 8), 16))
            IMU_Data[1].append(twos_comp(packet[16] | (packet[17] << 8), 16))
            IMU_Data[2].append(twos_comp(packet[18] | (packet[19] << 8), 16))
            IMU_Data[3].append(twos_comp(packet[2] | (packet[3] << 8), 16))
            IMU_Data[4].append(twos_comp(packet[4] | (packet[5] << 8), 16))
            IMU_Data[5].append(twos_comp(packet[6] | (packet[7] << 8), 16))

            timestamp.append(inc)
            inc += 1

        time.sleep(0.016)


              
class IMU_ML_App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "IMU Movement Classification")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="true")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Main_Page, Livestream_Data_Page, SetupBluetooth_Page, Collect_Move_Data_Page,
                  Manage_Stored_Data_Page, Train_Classifier_Page, Analyse_Classifier_Page, Play_Page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Main_Page)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Main_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Main Screen""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button_LSD = tk.Button(self, text="Live Stream Data",
                               command=lambda: controller.show_frame(Livestream_Data_Page))
        button_LSD.pack()
        button_BT = tk.Button(self, text="Setup Bluetooth",
                               command=lambda: controller.show_frame(SetupBluetooth_Page))
        button_BT.pack()
        button_CMD = tk.Button(self, text="Collect Movement Data",
                               command=lambda: controller.show_frame(Collect_Move_Data_Page))
        button_CMD.pack()
        button_MSD = tk.Button(self, text="Manage Stored Data",
                               command=lambda: controller.show_frame(Manage_Stored_Data_Page))
        button_MSD.pack()
        button_TCl = tk.Button(self, text="Train Classifier",
                               command=lambda: controller.show_frame(Train_Classifier_Page))
        button_TCl.pack()
        button_TCl = tk.Button(self, text="Analyse Classifier",
                               command=lambda: controller.show_frame(Analyse_Classifier_Page))
        button_TCl.pack()
        button_PP = tk.Button(self, text="PLAY",
                               command=lambda: controller.show_frame(Play_Page))
        button_PP.pack()
        

class Livestream_Data_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Live Streaming Data""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button_Home = tk.Button(self, text="Home",
                               command=lambda: controller.show_frame(Main_Page))
        button_Home.pack()        
        button_Generate = tk.Button(self, text="Generate",
                               command=lambda: practice_changeRecording(BT_Object, initialise_IMU))
        button_Generate.pack()               
        button_Record = tk.Button(self, text="Record",
                               command=lambda: BT_changeRecording(BT_Object, initialise_IMU))
        button_Record.pack()

        #Canvas on the frame to put the figure into
        canvas = FigureCanvasTkAgg(f, self) #Not sure why it needs self
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas.draw()
                               
class SetupBluetooth_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Setting up Bluetooth""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button_Home = tk.Button(self, text="Home",
                               command=lambda: controller.show_frame(Main_Page))
        button_Home.pack()
        button_BTCon = tk.Button(self, text="Connect To Bluetooth",
                               command=lambda: bluetooth_Connect(BT_Object, IMU_Address, port))
        button_BTCon.pack()

class Collect_Move_Data_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Collecting Movement Data""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button_Home = tk.Button(self, text="Home",
                               command=lambda: controller.show_frame(Main_Page))
        button_Home.pack()

class Manage_Stored_Data_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Managing Movement Data""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button_Home = tk.Button(self, text="Home",
                               command=lambda: controller.show_frame(Main_Page))
        button_Home.pack()

class Train_Classifier_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Training Classifier""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button_Home = tk.Button(self, text="Home",
                               command=lambda: controller.show_frame(Main_Page))
        button_Home.pack()

class Analyse_Classifier_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Analysing Classifier""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button_Home = tk.Button(self, text="Home",
                               command=lambda: controller.show_frame(Main_Page))
        button_Home.pack()

class Play_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Playing""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button_Home = tk.Button(self, text="Home",
                               command=lambda: controller.show_frame(Main_Page))
        button_Home.pack()
        
app = IMU_ML_App()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=200)
app.mainloop()
