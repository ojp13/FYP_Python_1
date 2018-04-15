import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("Tkagg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import style
from matplotlib import pyplot as plt

classlabel = 1

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

#plt.ion() #"Interactive mode" - Controls if the figure is redrawn every time
f = plt.figure()

a = f.add_subplot(211)
a2 = f.add_subplot(212)

def addtoplot():
    xs = [1,2,3,4,5,6,7,8]
    ys = [1000, 3000, 5000, 7000, 9000, 11000, 13000, 15000]
    y2s = [17000, 19000, 21000, 23000, 25000, 27000, 29000, 31000]

    a.scatter(xs, ys)
    a2.scatter(xs, y2s)
    f.canvas.draw()

def getdata():
    global classlabel

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

    
    classlabel = int(classlabel)
    classlabel += 2
    print(str(classlabel))

def addtwo():
    global classlabel

    classlabel += 2
    print(str(classlabel))

class SeaofBTCapp(tk.Tk): 

    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "ML IMU")
        
        container = tk.Frame(self) 
        container.pack(side="top", fill="both", expand="true")
        container.grid_rowconfigure(0, weight=1) 
        container.grid_columnconfigure(0, weight=1)                          

        self.frames = {}

        for F in (StartPage, Bitfinex_Page):
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
                            command =lambda: controller.show_frame(Bitfinex_Page))
        button1.pack()
        button2 = tk.Button(self, text="Disagree",
                            command =lambda: exit(0))
        button2.pack()

class Bitfinex_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Go to Home",
                            command =lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Plot Data",
                            command =lambda: addtoplot())
        button2.pack()
        button3 = ttk.Button(self, text="Get Data",
                            command =lambda: getdata())
        button3.pack()
        button4 = ttk.Button(self, text="Add Two",
                            command =lambda: addtwo())
        button4.pack()
 
        canvas = FigureCanvasTkAgg(f, self)
        
        toolbar = NavigationToolbar2TkAgg(canvas, self) 
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True) 
        canvas.show()


app = SeaofBTCapp()
app.geometry("1280x720") #Specifying size of application
app.mainloop()
