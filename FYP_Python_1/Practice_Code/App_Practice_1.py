import tkinter as tk
import threading

LARGE_FONT = ("Verdana", 12)

button_flag = True

def change_button_flag():
    global button_flag

    if button_flag:
        button_flag = False
    else:
        button_flag = True
    


class PracticeApp(tk.Tk): 

    def __init__(self, *args, **kwargs): 
        tk.Tk.__init__(self, *args, *kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "ML IMU")
        
        container = tk.Frame(self) 
        container.pack(side="top", fill="both", expand="true")
        container.grid_rowconfigure(0, weight=1) 
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageTwo):
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

        if button_flag == True:
            label = tk.Label(self, text="PageOneTrue", font=LARGE_FONT)
            label.pack(pady=10, padx=10)
        else:
            label = tk.Label(self, text="PageOneFalse", font=LARGE_FONT)
            label.pack(pady=10, padx=10)
        
        button1 = tk.Button(self, text="Agree",
                            command =lambda: change_button_flag())
        button1.pack()
        button2 = tk.Button(self, text="Disagree",
                            command = quit)
        button2.pack()
        button3 = tk.Button(self, text="Agree",
                            command =lambda: controller.show_frame(PageTwo))
        button3.pack()
        button2 = tk.Button(self, text="Disagree",
                            command = lambda: print(button_flag))
        button2.pack()

class PageTwo(tk.Frame): 

    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        label = tk.Label(self, text="PageTwo", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        button1 = tk.Button(self, text="Agree",
                            command =lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = tk.Button(self, text="Disagree",
                            command = quit)
        button2.pack()  

app = PracticeApp()
app.mainloop()
