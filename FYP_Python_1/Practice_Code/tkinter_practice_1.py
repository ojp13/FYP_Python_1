import tkinter as tk

LARGE_FONT = ("Verdana", 12) # Specifying a constant large font

class SeaofBTCapp(tk.Tk): #inheriting for Tk class in tkinter

    def __init__(self, *args, **kwargs): #Initialise method, always runs when creating object
        # *args - arguments, can pass as many arguments as possible
        ## **kwargs - keyword arguments, equivalent to passing dictionaries

        #initialising class we inherited from
        tk.Tk.__init__(self, *args, *kwargs)
        container = tk.Frame(self) # creating a container for the app
        # Frame is the window of the program

        # Packing the screen, doesn't have fine control over where things go
        container.pack(side="top", fill="both", expand="true")

        #simple configuration
        container.grid_rowconfigure(0, weight=1) # 0 is min size, weight is prio
        container.grid_columnconfigure(0, weight=1)

        self.frames = {} # self.frames is an empty dictionary

        frame = StartPage(container, self) # opening window

        # Tkinter will have lots of different frames, but only one frame will be
        # at the front, and that is the frame the user is interacting with atm

        self.frames[StartPage] = frame

        # Grid gives finer control over where things go in the frame
        frame.grid(row=0, column=0, sticky="nsew")
        # sticky specifies alignment + stretch (north, south, east, west)

        # show_frame isn't defined yet
        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont] # cont - container/controller
        frame.tkraise() # run .tkraise method, inherited from tk.Tk

# Example page
class StartPage(tk.Frame): #inheriting from tk.Frame class

    def __init__(self, parent, controller): # Initialising parent class
        tk.Frame.__init__(self, parent) # Parent is the parent class

        # Pass through some tkinter code so we can see the page
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        # label is how we add text to a tkinter window
        # Creating/initialising a label object

        # Actually doing something with the label onject
        label.pack(pady=10, padx=10)

app = SeaofBTCapp() # specific instance of tk class

# mainloop() is tkinter code
app.mainloop()
        
