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

from matplotlib import pyplot as plt

pd.options.mode.chained_assignment = None #default = 'warn'; stops an error warning coming up

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use("ggplot")

f = Figure()
a = f.add_subplot(111)

#Constants(variables) for the changeExchange function to work
exchange = "BTC-e"  #Default starting exchange
DatCounter = 9000   #Value at which an update of the ui is forced
programName = "btce"
resampleSize = "15Min" #Default sample size, 15 minute "candlesticks"
DataPace = "1d" #1 Days worth of pricing data
candleWidth = 0.0009 #width of the candle stick on the screen
topIndicator = "none"
bottomIndicator = "none"
middleIndicator = "none"
EMAs = []
SMAs = []


def addMiddleIndicator(what):
    global middleIndicator
    global DatCounter

    if DataPace == "tick":
        popupmsg("Indicators in Tick Data not available.")

    if what != "none":
        if middleIndicator == "none":
            if what == "sma":
                midIQ = tk.Tk                   #midIQ = middle indicator question
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="choose how many periods you want your moving average to be")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicators
                    global DatCounter

                    middleIndicators = []
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    DatCounter=9000
                    print("middle indicator set to", middleIndicators)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)

            if what == "ema":
                midIQ = tk.Tk                   #midIQ = middle indicator question
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="choose how many periods you want your moving average to be")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicators
                    global DatCounter

                    middleIndicators = []
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    DatCounter=9000
                    print("middle indicator set to", middleIndicators)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                
        else:
            if what == "sma":
                midIQ = tk.Tk                   #midIQ = middle indicator question
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="choose how many periods you want your moving average to be")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicators
                    global DatCounter

                    middleIndicators = []
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    DatCounter=9000
                    print("middle indicator set to", middleIndicators)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)

        

def addTopIndicator(what):
    global topIndicator
    global DatCounter

    if DataPace == "tick":
        popupmsg("Indicators in Tick Data not available.")

    elif what == "none":
        topIndicator = what
        DatCounter = 9000

    elif what == "rsi":
        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label = ttk.Label(rsiQ, text = "Choose how many periods you want each RSI calculation to consider.")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ) #Entry widget for tkinter, user input
        e.insert(0,14)
        e.pack()
        e.focus_set() #setting the focus

        def callback():
            global topIndicator
            global DatCounter

            periods = (e.get()) #Will get whatever was typed into e
            group = []
            group.append("rsi")
            group.append(periods)

            topIndicator = group     #rsi,14 now stored as top indicator
            datCounter = 9000
            print("Set top indicator to ", group)
            rsiQ.destroy()

        b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()

    elif what == "macd":
####        global DatCounter

        topIndicator = "macd"
        DatCounter = 9000

def addBottomIndicator(what):
    global bottomIndicator
    global DatCounter

    if DataPace == "tick":
        popupmsg("Indicators in Tick Data not available.")

    elif what == "none":
        bottomIndicator = what
        DatCounter = 9000

    elif what == "rsi":
        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label = ttk.Label(rsiQ, text = "Choose how many periods you want each RSI calculation to consider.")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ) #Entry widget for tkinter, user input
        e.insert(0,14)
        e.pack()
        e.focus_set() #setting the focus

        def callback():
            global bottomIndicator
            global DatCounter

            periods = (e.get()) #Will get whatever was typed into e
            group = []
            group.append("rsi")
            group.append(periods)

            rsiQ = group     #rsi,14 now stored as top indicator
            datCounter = 9000
            print("Set bottom indicator to ", group)
            rsiQ.destroy()

        b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()

    elif what == "macd":
####        global bottomIndicator
##        global DatCounter

        bottomIndicator = "macd"
        DatCounter = 9000


def changeTimeFrame(tf):
    global DataPace
    global DatCounter

    if tf == "7d" and resampleSize == "1Min":
        popupmsg("Too much data chosen, choose a smaller time frame or higher OHLC interval")
    else:
        DataPace = tf
        DatCounter = 9000

def changeSampleSize(size, width): #size of the sample size, width of the candlestick
    global resampleSize
    global DatCounter
    global candleWidth

    if DataPace == "7d" and resampleSize == "1Min":
        popupmsg("Too much data chosen, choose a smaller time frame or higher OHLC interval")

    elif DataPace == "tick":
        popupmsg("You're currently viewing tick data, not OHLC.")

    else:
        resampleSize = size
        DatCounter = 9000
        candlewidth = width
        
#Changes the backend; the source that the program gets the data from
def changeExchange(toWhat, pn):

    #This allows the function to change the value of these variables globally
    global exchange
    global DatCounter
    global programName

    exchange = toWhat
    programName = pn
    DatCounter = 9000
    

def popupmsg(msg):
    popup = tk.Tk()

    #This is like a mini-instance of Tkinter
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack() #will naturally go underneath the label
    popup.mainloop()
    

def animate(i):
    dataLink = 'https://api.bitfinex.com/v1/trades/BTCUSD?limit_trades=2000'
    data = urllib.request.urlopen(dataLink)
    data = data.read().decode("utf-8")
    data = json.loads(data)

    data = pd.DataFrame(data) 

    buys = data[(data['type']=="buy")]

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
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "ML IMU")
        
        container = tk.Frame(self) 
        container.pack(side="top", fill="both", expand="true")
        container.grid_rowconfigure(0, weight=1) 
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container) #Creating a menu, putting it in the container
        filemenu = tk.Menu(menubar, tearoff=0) #Creating a filemenu
        filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported just yet!"))
        #adding a command to the filemenu pupupmsg is a user defined function
        filemenu.add_separator() # adds a separating bar to the menu
        filemenu.add_command(label="Exit", command = quit)
        menubar.add_cascade(label="File", menu=filemenu)

        exchangeChoice = tk.Menu(menubar, tearoff=1)
        exchangeChoice.add_command(label="BTC-e",
                                   command=lambda: changeExchange("BTC-e","btce"))
        exchangeChoice.add_command(label="Bitfinex",
                                   command=lambda: changeExchange("Bitfinex","bitfinex"))
        exchangeChoice.add_command(label="Bitstamp",
                                   command=lambda: changeExchange("Bitstamp","bitstamp"))
        exchangeChoice.add_command(label="Huobi",
                                   command=lambda: changeExchange("Huobi","huobi"))
        menubar.add_cascade(label="Exchange", menu=exchangeChoice)

        dataTF = tk.Menu(menubar, tearoff=1) #Timeframe for data
        dataTF.add_command(label="Tick",
                           command=lambda: changeTimeFrame("tick"))
        dataTF.add_command(label="1 Day",
                           command=lambda: changeTimeFrame("1d"))
        dataTF.add_command(label="3 Day",
                           command=lambda: changeTimeFrame("3d"))
        dataTF.add_command(label="1 Week",
                           command=lambda: changeTimeFrame("7d"))
        menubar.add_cascade(label="Data Time Frame", menu = dataTF)

        OHLCI = tk.Menu(menubar, tearoff=1)
        OHLCI.add_command(label="Tick",
                           command=lambda: changeTimeFrame("tick"))
        OHLCI.add_command(label="1 minute",
                           command=lambda: changeSampleSize("1Min", 0.0005))
        OHLCI.add_command(label="5 minute",
                           command=lambda: changeSampleSize("5Min", 0.003))
        OHLCI.add_command(label="15 minute",
                           command=lambda: changeSampleSize("15Min", 0.008))
        OHLCI.add_command(label="30 minute",
                           command=lambda: changeSampleSize("30Min", 0.016))
        OHLCI.add_command(label="1 Hour",
                           command=lambda: changeSampleSize("1H", 0.032))
        OHLCI.add_command(label="3 Hour",
                           command=lambda: changeSampleSize("3H", 0.096))
        menubar.add_cascade(label="OHLC Interval", menu=OHLCI)

        #Adding indicators to the graph
        topIndi = tk.Menu(menubar, tearoff=1)
        topIndi.add_command(label="None",
                            command=lambda: addTopIndicator("none"))
        topIndi.add_command(label="RSI",
                            command=lambda: addTopIndicator("rsi"))     #rsi = relative strength index
        topIndi.add_command(label="MACD",
                            command=lambda: addTopIndicator("macd"))
        menubar.add_cascade(label="Top Indicator", menu=topIndi)


        mainI = tk.Menu(menubar, tearoff=1)
        mainI.add_command(label="None",
                            command=lambda: addMiddleIndicator("none"))
        mainI.add_command(label="SMA",
                            command=lambda: addMiddleIndicator("rsi"))  #sma = simple moving average
        mainI.add_command(label="EMA",
                            command=lambda: addMiddleIndicator("macd")) #ema = exponential moving average
        menubar.add_cascade(label="Main/Middle Indicator", menu=mainI)
        

        bottomI = tk.Menu(menubar, tearoff=1)
        bottomI.add_command(label="None",
                            command=lambda: addBottomIndicator("none"))
        bottomI.add_command(label="RSI",
                            command=lambda: addBottomIndicator("rsi"))
        bottomI.add_command(label="MACD",
                            command=lambda: addBottomIndicator("macd"))
        menubar.add_cascade(label="Bottom Indicator", menu=bottomI)
        

        

        
        
        tk.Tk.config(self, menu=menubar) #Adds the menubar

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
app.geometry("1280x720") #Specifying size of application
ani = animation.FuncAnimation(f, animate, interval=3000)
app.mainloop()





















        
