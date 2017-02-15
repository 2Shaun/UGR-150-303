import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# figure window
fig = plt.figure()
ax = plt.axes(xlim=(0, 0), ylim=(0,0))
line, = ax.plot([], [], lw=2)
#single axis
x = np.linspace(0,2,10)
#empty line object

def init():
    line.set_data([], [])
    return line,

def animate(i):
    y = i*x
    ax = plt.axes(xlim=(0, i), ylim=(0,y))
    line, = ax.plot([], [], lw=2)
    line.set_data(x, y)
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init,
        frames=100, interval=20, blit=True)

plt.show()
