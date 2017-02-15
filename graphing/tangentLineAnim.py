import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = plt.axes(xlim=(-50,50), ylim=(-500,500))
plt.plot([0,0],[-1000,1000],lw=1,color='k')
plt.plot([-1000,1000],[0,0],lw=1,color='k')
line, = ax.plot([], [], '--r')
point, = ax.plot([], [], 'om')
e = 2.71828182846

def f(x):
    return 200*np.sin(x)

# linspace
# return array of evenly spaced numbers
# [start,stop],number of samples
x = np.linspace(-100,25,500)
y = f(x)

def initLine():
    line.set_data([], [])
    return line,

def initPoint():
    point.set_data([], [])
    return point,

def animateLine(i):
    # arbirtrarily close to 0
    h = 0.1
    # i = iterator
    # [f(i+h) - f(i)]/
    # h
    fprime = (f(i+h)-f(i))/h
    tan = f(i)+fprime*(x-i)
    root = ((0-f(i))*h)/(f(i+h)-f(i)) + i
    line.set_data(x, tan)
    point.set_data(root,f(root))
    return line,

def animatePoint(i):
    point.set_data(root,f(i))
    return point,

plt.plot(x,y,'b')
animLine = animation.FuncAnimation(fig, animateLine, init_func=initLine, frames=15, interval=1000)
#animPoint = animation.FuncAnimation(fig, animatePoint, init_func=initPoint, frames=15, interval=100)
plt.show()
