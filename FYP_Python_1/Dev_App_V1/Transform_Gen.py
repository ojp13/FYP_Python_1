try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
def toggle(t_btn):
    '''
    use
    t_btn.config('text')[-1]
    to get the present state of the toggle button
    '''
    if t_btn.config('text')[-1] == 'True':
        t_btn.config(text='False')
    else:
        t_btn.config(text='True')
        
root = tk.Tk()
t_btn = tk.Button(text="True", width=12, command= lambda: toggle(t_btn))
t_btn.pack(pady=5)

t_btn2 = tk.Button(text="True", width=12, command= lambda: toggle(t_btn2))
t_btn2.pack(pady=5)

print(t_btn.config('text')[-1])

root.mainloop()
