import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("Tkagg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
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
from scipy.integrate import simps
from scipy.integrate import cumtrapz

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use("ggplot")

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
IMU_Data_Key = ["x acceleration", "y acceleration", "z acceleration", "x gyroscope", "y gyroscope", "z gyroscope"]
movement_features_key = ["x total disp.", "y total disp.", "z total disp.", "x total rot.", "y total rot.", "z total rot.",
                         "class label"]
features_df = pd.DataFrame(columns=movement_features_key)
timestamp = []
movement_rawdata_collected = []
classlabel = 0 #Has to be specified for the popup window functions to work
filename = "" #Has to be spicified for popup window to work
rawdata_index = 0 #Has to be spicified for popup window to work

#Plotting of figures
f = plt.figure()
a = f.add_subplot(211) #2 rows, 1 column, 1st position
a.set_ylim([-36000, 36000])
a.set_ylabel("Linear Acc.")
a.axes.xaxis.set_ticklabels([]) #Hides the x axis tick labels
a2 = f.add_subplot(212) #2 rows, 1 column, 2nd position
a2.set_ylim([-36000, 36000])
a2.set_ylabel("Angular Acc.")
a2.set_xlabel("Time")

#Constants to keep track of settings
feature_normalisation = True

def create_feature_array(movement_rawdata_collected):
    global features_df

    num_samples = len(movement_rawdata_collected)
    x_totaldisp = np.zeros(num_samples)
    y_totaldisp = np.zeros(num_samples)
    z_totaldisp = np.zeros(num_samples)
    x_totalrot = np.zeros(num_samples)
    y_totalrot = np.zeros(num_samples)
    z_totalrot = np.zeros(num_samples)
    classlabels = np.zeros(num_samples, dtype=int)

    for i in range(num_samples):
        x_velocity = cumtrapz(movement_rawdata_collected[i]["x acceleration"][:])
        x_totaldisp[i] = simps(x_velocity)
        y_velocity = cumtrapz(movement_rawdata_collected[i]["y acceleration"][:])
        y_totaldisp[i] = simps(y_velocity)
        z_velocity = cumtrapz(movement_rawdata_collected[i]["z acceleration"][:])
        z_totaldisp[i] = simps(z_velocity)
        
        x_rot_velocity = cumtrapz(movement_rawdata_collected[i]["x gyroscope"][:])
        x_totalrot[i] = simps(x_rot_velocity)
        y_rot_velocity = cumtrapz(movement_rawdata_collected[i]["y gyroscope"][:])
        y_totalrot[i] = simps(y_rot_velocity)
        z_rot_velocity = cumtrapz(movement_rawdata_collected[i]["z gyroscope"][:])
        z_totalrot[i] = simps(z_rot_velocity)

        classlabels[i] = int(movement_rawdata_collected[i]["Class Label"][0])
        
    if feature_normalisation: #If feature normalisation is set to true
        s = sum(x_totaldisp)
        x_totaldisp = [float(i)/s for i in x_totaldisp]
        s = sum(y_totaldisp)
        y_totaldisp = [float(i)/s for i in y_totaldisp]
        s = sum(z_totaldisp)
        z_totaldisp = [float(i)/s for i in z_totaldisp]
        s = sum(x_totalrot)
        x_totalrot= [float(i)/s for i in x_totalrot]
        s = sum(y_totalrot)
        y_totalrot= [float(i)/s for i in y_totalrot]
        s = sum(z_totalrot)
        z_totalrot= [float(i)/s for i in z_totalrot]
  

    features_df["x total disp."] = x_totaldisp
    features_df["y total disp."] = y_totaldisp
    features_df["z total disp."] = z_totaldisp
    features_df["x total rot."] = x_totalrot
    features_df["y total rot."] = y_totalrot
    features_df["z total rot."] = z_totalrot
    features_df["class label"] = classlabels

    print(features_df)

def save_feature_array(features_df):
    global filename

    #Popup window to get the user desired filename for the feature array
    filename_entry = tk.Tk()
    filename_entry.wm_title("Filename?")
    label = ttk.Label(filename_entry, text = "What is the name of the file you would like to save the feature array to?")
    label.pack(side="top", fill="x", pady=10)
    e1 = ttk.Entry(filename_entry) #Entry widget for tkinter, user input
    e1.pack()
    e1.focus_set() #setting the focus

    #Have to make this function in order to get info from the e frame
    def callback_filename():
        global filename

        filename = (e1.get()) #Will get whatever was typed into the popup
        filename_entry.destroy()
        filename_entry.quit()  

    #Add a button to get the entered text into a variable 
    b = ttk.Button(filename_entry, text="Submit", width=10, command=callback_filename)
    b.pack()
    filename_entry.mainloop() #Required to make the popup window appear

    filename = filename + ".pickle"

    pickle_out = open(filename,"wb") #We would like to open a file to save data to
    pickle.dump(features_df, pickle_out) #Saves the list to a pickle file
    pickle_out.close() #Close the file to avoid mistakes

def clear_feature_array():
    global features_df

    features_df.drop(features_df.index, inplace=True)


def display_feature_array(features_df):
    print(features_df)


def load_feature_array():
    global features_df   

    #Popup window to get the user desired filename for the raw data
    filename_entry = tk.Tk()
    filename_entry.wm_title("Filename?")
    label = ttk.Label(filename_entry, text = "What is the name of the file you would like to load your feature array from?\nPlease include pickle suffix")
    label.pack(side="top", fill="x", pady=10)
    
    e1 = ttk.Entry(filename_entry) #Entry widget for tkinter, user input
    e1.pack()
    e1.focus_set() #setting the focus

    #Have to make this function in order to get info from the e frame
    def callback_filename():
        global filename

        filename = (e1.get()) #Will get whatever was typed into the popup
        filename_entry.destroy()
        filename_entry.quit()  

    #Add a button to get the entered text into a variable 
    b = ttk.Button(filename_entry, text="Submit", width=10, command=callback_filename)
    b.pack()
    filename_entry.mainloop() #Required to make the popup window appear

    pickle_in = open(filename,"rb") #We would like to open a file to read data from
    features_df = pickle.load(pickle_in)
    pickle_in.close()
    

def plot_rawdata(movement_rawdata_collected):
    global rawdata_index

    #Popup window to get the index of the data the user wants to plot
    rawdata_index_entry = tk.Tk()
    rawdata_index_entry.wm_title("Data Index")
    label = ttk.Label(rawdata_index_entry, text = "What is the index of the data you would like to plot? (1st, 2nd, 3rd, etc...\nStart Index at 1")
    label.pack(side="top", fill="x", pady=10)
    
    e1 = ttk.Entry(rawdata_index_entry) #Entry widget for tkinter, user input
    e1.pack()
    e1.focus_set() #setting the focus

    #Have to make this function in order to get info from the e frame
    def callback_rawdata_index():
        global rawdata_index

        rawdata_index = (e1.get()) #Will get whatever was typed into the popup
        rawdata_index_entry.destroy()
        rawdata_index_entry.quit()

    #Add a button to get the entered text into a variable 
    b = ttk.Button(rawdata_index_entry, text="Submit", width=10, command=callback_rawdata_index)
    b.pack()
    rawdata_index_entry.mainloop() #Required to make the popup window appear

    rawdata_index = int(rawdata_index) - 1 #The -1 is to turn the user inputted index into a list index (starts at 0)
    data_dict = movement_rawdata_collected[rawdata_index]

    timeaxis = range(len(data_dict["x acceleration"]))

    #Have to clear plots otherwise legends stack on top of each other
    a.clear()
    a2.clear()
    a.axes.xaxis.set_ticklabels([]) #Hides the x axis tick labels
    a.set_ylim([-36000, 36000])
    a2.set_ylim([-36000, 36000])
    
    #Adding data to axes
    a.scatter(timeaxis[:], data_dict["x acceleration"][:], label="x acceleration", s=15, color="red")
    a.scatter(timeaxis[:], data_dict["y acceleration"][:], label="y acceleration", s=15, color="green")
    a.scatter(timeaxis[:], data_dict["z acceleration"][:], label="z acceleration", s=15, color="blue")
    a2.scatter(timeaxis[:], data_dict["x gyroscope"][:], label="x gyroscope", s=15, color="red")
    a2.scatter(timeaxis[:], data_dict["y gyroscope"][:], label="y gyroscope", s=15, color="green")
    a2.scatter(timeaxis[:], data_dict["z gyroscope"][:], label="z gyroscope", s=15, color="blue")   
    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=3, borderaxespad=0)
    a2.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=3, borderaxespad=0)

    #We have to redraw the plot
    f.canvas.draw()

#If the user has loaded some data to plot, but doesn't want to append to it
def clear_rawdata():
    global movement_rawdata_collected

    movement_rawdata_collected = []

#In case the user made a mistake during recording
def clear_last_entry():
    global movement_rawdata_collected

    del movement_rawdata_collected[-1]

def load_rawdata():
    global movement_rawdata_collected   

    #Popup window to get the user desired filename for the raw data
    filename_entry = tk.Tk()
    filename_entry.wm_title("Filename?")
    label = ttk.Label(filename_entry, text = "What is the name of the file you would like to load data from?\nPlease include pickle suffix")
    label.pack(side="top", fill="x", pady=10)
    
    e1 = ttk.Entry(filename_entry) #Entry widget for tkinter, user input
    e1.pack()
    e1.focus_set() #setting the focus

    #Have to make this function in order to get info from the e frame
    def callback_filename():
        global filename

        filename = (e1.get()) #Will get whatever was typed into the popup
        filename_entry.destroy()
        filename_entry.quit()  

    #Add a button to get the entered text into a variable 
    b = ttk.Button(filename_entry, text="Submit", width=10, command=callback_filename)
    b.pack()
    filename_entry.mainloop() #Required to make the popup window appear

    pickle_in = open(filename,"rb") #We would like to open a file to read data from
    movement_rawdata_collected = pickle.load(pickle_in)
    

def save_rawdata(movement_rawdata_collected):
    global filename

    #Popup window to get the user desired filename for the raw data
    filename_entry = tk.Tk()
    filename_entry.wm_title("Filename?")
    label = ttk.Label(filename_entry, text = "What is the name of the file you would like to save data to?")
    label.pack(side="top", fill="x", pady=10)
    e1 = ttk.Entry(filename_entry) #Entry widget for tkinter, user input
    e1.pack()
    e1.focus_set() #setting the focus

    #Have to make this function in order to get info from the e frame
    def callback_filename():
        global filename

        filename = (e1.get()) #Will get whatever was typed into the popup
        filename_entry.destroy()
        filename_entry.quit()  

    #Add a button to get the entered text into a variable 
    b = ttk.Button(filename_entry, text="Submit", width=10, command=callback_filename)
    b.pack()
    filename_entry.mainloop() #Required to make the popup window appear

    filename = filename + ".pickle"

    pickle_out = open(filename,"wb") #We would like to open a file to save data to
    pickle.dump(movement_rawdata_collected, pickle_out) #Saves the list to a pickle file
    pickle_out.close() #Close the file to avoid mistakes  


def bluetooth_Connect(BT_Object, IMU_Address, port):

    try:
        BT_Object.connect((IMU_Address, port))
        popupmsg(str(BT_Object.recv(15)))

    except Exception as e:
        popupmsg("Bluetooth connection failed: " + str(e) + "     \nIf error is 'File descriptor in bad state', reset IMU and App")


def BT_changeRecording(BT_Object, initialise_IMU):
    global BT_isRecording

    if BT_isRecording:
        BT_isRecording = False
    else:
        BT_isRecording = True
        t = threading.Thread(target=read_Bluetooth_Data,
                             args=(BT_Object, initialise_IMU, start_Bytes, packet_length, IMU_Data_Key),
                             name="read_Thread", daemon=True)
        t.start()

    print(BT_isRecording)

        
def read_Bluetooth_Data(BT_Object, initialise_IMU, start_Bytes, packet_length, IMU_Data_Key):
    global timestamp
    global movement_rawdata_collected
    global classlabel
    
    BT_Object.send(initialise_IMU)
    
    packet = np.zeros(packet_length-3, dtype="int")
    IMU_Data = [[],[],[],[],[],[]] #Acc x,y,z Then Gyro x,y,z

    #Incrementer to append to timestamp, which is the x axis for our plots
    inc = 0
    
    while BT_isRecording:

        IMUPacket = BT_Object.recv(3)
        
        if IMUPacket.hex() == start_Bytes:
            # if it is, record the next 38 bytes
            for j in range (0, packet_length-3):
                packet[j] = int(BT_Object.recv(1).hex(),16)
            IMU_Data[0].append(twos_comp(packet[14] | (packet[15] << 8), 16)) #Acc x
            IMU_Data[1].append(twos_comp(packet[16] | (packet[17] << 8), 16)) #Acc y
            IMU_Data[2].append(twos_comp(packet[18] | (packet[19] << 8), 16)) #Acc z
            IMU_Data[3].append(twos_comp(packet[2] | (packet[3] << 8), 16)) #Gyro x
            IMU_Data[4].append(twos_comp(packet[4] | (packet[5] << 8), 16)) #Gyro y
            IMU_Data[5].append(twos_comp(packet[6] | (packet[7] << 8), 16)) #Gyro z

            timestamp.append(inc)
            inc += 1

    movement_rawdata = {}   #Empty dictionary to store raw data in
    i = 0               #Incrementor for for loop

    for K in IMU_Data_Key: #Store raw data in the dictionary
        #Takes the values recorded and stores them as a key-value pair, using the key from
        #IMU_Data_Key
        movement_rawdata[IMU_Data_Key[i]] = IMU_Data[i] 
        i += 1

    #Popup window to get the class label for the movement
    classlabel_entry = tk.Tk()
    classlabel_entry.wm_title("Class Label?")
    label = ttk.Label(classlabel_entry, text = "What is the class label of the movement just completed? (1/2/3/4)")
    label.pack(side="top", fill="x", pady=10)
    e = ttk.Entry(classlabel_entry) #Entry widget for tkinter, user input
    e.pack()
    e.focus_set() #setting the focus

    #Have to make this function in order to get info from the e frame
    def callback():
        global classlabel

        classlabel = (e.get()) #Will get whatever was typed into the popup
        classlabel_entry.destroy()
        classlabel_entry.quit()

    #Add a button to get the entered text into a variable (classlabel)
    b = ttk.Button(classlabel_entry, text="Submit", width=10, command=callback)
    b.pack()
    classlabel_entry.mainloop() #Required to make the popup window appear

    movement_rawdata["Class Label"] = classlabel #Add the class label to the dictionary
    #Appends the data dictionary to a list
    movement_rawdata_collected.append(movement_rawdata)
    #print(movement_rawdata_collected[-1])
    #print(movement_rawdata_collected[-1]["Class Label"])

def popupmsg(msg):
    popup = tk.Tk()

    #This is like a mini-instance of Tkinter
    popup.wm_title("Pop-up Message")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack() #will naturally go underneath the label
    popup.mainloop()
              
class IMU_ML_App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "IMU Movement Classification")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="true")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Main_Page, Display_Data_Page, SetupBluetooth_Page, Collect_Move_Data_Page,
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
        button_LSD = tk.Button(self, text="Display Data",
                               command=lambda: controller.show_frame(Display_Data_Page))
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
        
class Display_Data_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Displaying Data""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button_Home = tk.Button(self, text="Home",
                               command=lambda: controller.show_frame(Main_Page))
        button_Home.pack()
        button_PlotRawData = tk.Button(self, text="Plot Raw Data",
                               command=lambda: plot_rawdata(movement_rawdata_collected))
        button_PlotRawData.pack()

        #Data will be plotted on this page. Creating a canvas to plot to
        canvas = FigureCanvasTkAgg(f, self) #The canvas will be for plotting figure f on this frame
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                               
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
                       
        button_Record = tk.Button(self, text="Record",
                               command=lambda: BT_changeRecording(BT_Object, initialise_IMU))
        button_Record.pack()
        button_Clear_Last_Entry = tk.Button(self, text="Clear Last Entry",
                               command=lambda: clear_last_entry())
        button_Clear_Last_Entry.pack()

class Manage_Stored_Data_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Managing Movement Data""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button_Home = tk.Button(self, text="Home",
                               command=lambda: controller.show_frame(Main_Page))
        button_Home.pack()
        button_Save = tk.Button(self, text="Save Raw Data",
                               command=lambda: save_rawdata(movement_rawdata_collected))
        button_Save.pack()
        button_Load = tk.Button(self, text="Load Raw Data",
                               command=lambda: load_rawdata())
        button_Load.pack()
        button_Clear = tk.Button(self, text="Clear Raw Data",
                               command=lambda: clear_rawdata())
        button_Clear.pack()        
        button_Save_FeatureArray = tk.Button(self, text="Save Feature Array",
                               command=lambda: save_feature_array(features_df))
        button_Save_FeatureArray.pack()
        button_Load_FeatureArray = tk.Button(self, text="Load Feature Array",
                               command=lambda: load_feature_array())
        button_Load_FeatureArray.pack()
        button_Clear_FeatureArray = tk.Button(self, text="Clear Feature Array",
                               command=lambda: clear_feature_array())
        button_Clear_FeatureArray.pack()        
        button_Display_FeatureArray = tk.Button(self, text="Display Feature Array",
                               command=lambda: display_feature_array(features_df))
        button_Display_FeatureArray.pack() 
        

class Train_Classifier_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""Training Classifier""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button_Home = tk.Button(self, text="Home",
                               command=lambda: controller.show_frame(Main_Page))
        button_Home.pack()
        button_FeatureArray = tk.Button(self, text="Create Feature Array",
                               command=lambda: create_feature_array(movement_rawdata_collected))
        button_FeatureArray.pack()

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
app.mainloop()
