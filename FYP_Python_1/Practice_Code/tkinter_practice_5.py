"""Plotting live data"""

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import urllib
import json

import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None #default = 'warn'; stops an error warning coming up

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(10,6), dpi=100)
a = f.add_subplot(111)

def animate(i):
    dataLink = 'https://api.bitfinex.com/v1/trades/BTCUSD?limit_trades=50'
    #limit is a parameter follows a "?" at the end of the url
    data = urllib.request.urlopen(dataLink)
    data = data.read().decode("utf-8")
    data = json.loads(data)

    data = pd.DataFrame(data) #changes it into a pandas dataset

    #buys is a pandas dataset of data, where the datatype = bit
    buys = data[(data['type']=="buy")]  #all the data of type bid (all the buys)

    #adding a column for the converted timestamp
    buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
    buyDates = (buys["datestamp"]).tolist()
    
    sells = data[(data['type']=="sell")] #same for sells
    sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
    sellDates = (sells["datestamp"]).tolist()
    
    a.clear()
    a.plot_date(buyDates, buys["price"], "#00A3E0", label ="buys")
    a.plot_date(sellDates, sells["price"], "#183A54", label="sells")
    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)
    
    title = "BTC-e BTCUSD Prices\nLast Price: " + str(data["price"][0])
    a.set_title(title)
    
    
 
class SeaofBTCapp(tk.Tk): 

    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, *kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "ML IMU")
        
        container = tk.Frame(self) 
        container.pack(side="top", fill="both", expand="true")
        container.grid_rowconfigure(0, weight=1) 
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, BTCe_Page):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise() 

class StartPage(tk.Frame): 

    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        label = tk.Label(self, text="""ALPHA Bitcoin Trading Application.
Use at your own risk. Thre is no promise
of warranty.""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        button1 = tk.Button(self, text="Agree",
                            command =lambda: controller.show_frame(BTCe_Page))
        button1.pack()
        button2 = tk.Button(self, text="Disagree",
                            command = quit)
        button2.pack()

        
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Go to Home",
                            command =lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Page Two",
                            command =lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = tk.Button(self, text="Graph Page",
                            command =lambda: controller.show_frame(PageThree))
        button3.pack()

class BTCe_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Go to Home",
                            command =lambda: controller.show_frame(StartPage))
        button1.pack()
 
        canvas = FigureCanvasTkAgg(f, self)
        
        toolbar = NavigationToolbar2TkAgg(canvas, self) 
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True) 
        canvas.show()

        

app = SeaofBTCapp()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()





















        
