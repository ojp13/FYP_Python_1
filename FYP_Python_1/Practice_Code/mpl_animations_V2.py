import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import threading

style.use("ggplot")

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

plot_data = [[],[]]


def generate_data():
    global plot_data
    for i in range(200000):
        plot_data[0].append(i)
        plot_data[1].append(i**2)
        print(plot_data[0][-1])
        print(plot_data[1][-1])

def animate(i):
    xs = plot_data[0]
    ys = plot_data[1]
    
    ax1.clear()
    ax1.plot(xs, ys)
    
t = threading.Thread(target=generate_data, name="Thread1", daemon=True)
t.start()
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
