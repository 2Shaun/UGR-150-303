"""
 simple example of an animated plot
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

x = np.arange(1, 6, 1)

line, = ax.plot(x, 1/x)

def animate(i):
    line.set_ydata(1/i)  # update the data
    return line,
        
        
#Init only required for blitting to give a clean slate.
def init():
    line.set_ydata(np.ma.array(x, mask=True))
    return line,
                
ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init,interval=25, blit=True)
plt.show()
