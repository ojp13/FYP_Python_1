import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("Tkagg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt

import pickle
import threading
import pandas as pd
import numpy as np
import math
import time

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use("ggplot")

f = plt.figure()

#Constants to keep track of settings

#Constants to allow for movement of data in app
gen_Data = False
BT_isRecording = False
accx = []
accy = []
accz = []
angx = []
angy = []
angz = []
timestamp = []

def animate(i):
    
    global accx
    global accy
    global accz
    global angx
    global angy
    global angz
    global timestamp

    #Setting up subplots for plotting bluetooth data
    #Plot for linear accelerations, 9x6 grid, start at top left
    a = plt.subplot2grid((9,6), (0,0), rowspan=3, colspan=6)
    plt.setp(a.get_xticklabels(), visible=False)
    a.set_ylabel("Linear Acc.")
    #Plot for angluar accelerations, start in 4th row, have same x axis as first plot
    a2 = plt.subplot2grid((9,6), (3,0), sharex=a, rowspan=3, colspan=6)
    plt.setp(a2.get_xticklabels(), visible=False)
    a2.set_ylabel("Angular Acc.")
    #Plot for MMG readings
    a3 = plt.subplot2grid((9,6), (6,0), sharex=a, rowspan=3, colspan=6)
    a3.set_ylabel("MMG Signals")
    a3.set_xlabel("Time")

    a.clear()
    a2.clear()
    a3.clear()

    const = 100
    if len(accx) < const:
        a.scatter(timestamp[:], accx[:], label="x component")
        a.scatter(timestamp[:], accy[:], label="y component")
        a.scatter(timestamp[:], accz[:], label="z component")
        a2.scatter(timestamp[:], angx[:], label="x component")
        a2.scatter(timestamp[:], angy[:], label="y component")
        a2.scatter(timestamp[:], angz[:], label="z component")
    else:        
        a.scatter(timestamp[-const:], accx[-const:], label="x component")
        a.scatter(timestamp[-const:], accy[-const:], label="y component")
        a.scatter(timestamp[-const:], accz[-const:], label="z component")
        a2.scatter(timestamp[-const:], angx[-const:], label="x component")
        a2.scatter(timestamp[-const:], angy[-const:], label="y component")
        a2.scatter(timestamp[-const:], angz[-const:], label="z component")
        
                  

def BT_changeRecording():
    global BT_isRecording
    global gen_Data

    if BT_isRecording:
        BT_isRecording = False
        gen_Data = False
    else:
        BT_isRecording = True
        t = threading.Thread(target=read_Data, name="read_Thread")
        t.start()

    print(BT_isRecording)


def read_Data():
    global accx
    global accy
    global accz
    global angx
    global angy
    global angz
    global timestamp
    
    inc = 0
    while BT_isRecording:
        accx.append(math.sin(inc/(2*math.pi)))
        accy.append(math.sin((inc + (10*math.pi/3))/(2*math.pi)))
        accz.append(math.sin((inc + (20*math.pi/3))/(2*math.pi)))
        angx.append(math.sin(inc/(2*math.pi)))
        angy.append(math.sin((inc + (10*math.pi/3))/(2*math.pi)))
        angz.append(math.sin((inc + (20*math.pi/3))/(2*math.pi)))
        timestamp.append(inc)
        time.sleep(0.005)
        inc += 1
        
        
        
        
    
    
        
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
        button_Record = tk.Button(self, text="Generate",
                               command=lambda: BT_changeRecording())
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
ani = animation.FuncAnimation(f, animate, interval=20)
app.mainloop()
