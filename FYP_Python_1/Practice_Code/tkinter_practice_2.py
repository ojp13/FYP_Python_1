import tkinter as tk

LARGE_FONT = ("Verdana", 12) 

class SeaofBTCapp(tk.Tk): 

    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, *kwargs)
        container = tk.Frame(self) 
        container.pack(side="top", fill="both", expand="true")

        container.grid_rowconfigure(0, weight=1) 
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        #This loop adds the pages to the app, a new page has to be added to the
        #For loop tuple for it to exist
        for F in (StartPage, PageOne, PageTwo):
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
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        #button 1 is the object returned by tk.Button
        # command specifies a function that is executed when you press the button
        # use the lambda construct when the function is passed a parameter
        button1 = tk.Button(self, text="Visit Page 1",
                            command =lambda: controller.show_frame(PageOne))
        button1.pack()
        button2 = tk.Button(self, text="Page Two",
                            command =lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Go to home",
                            command =lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = tk.Button(self, text="Page Two",
                            command =lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Go to Home",
                            command =lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command =lambda: controller.show_frame(PageOne))
        button2.pack()

app = SeaofBTCapp()
app.mainloop()
        
