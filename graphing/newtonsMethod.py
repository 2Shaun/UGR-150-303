import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = plt.axes(xlim=(-50,50), ylim=(-2,2))
# y axis
# draws line from (0,-1000) to (0,1000)
plt.plot([0,0],[-1000,1000],lw=1,color='k')
# x axis
# draws line from (-1000,0) to (1000,0)
plt.plot([-1000,1000],[0,0],lw=1,color='k')
line, = ax.plot([], [], '--r')
point, = ax.plot([], [], 'om')

def f(x):
    return np.sin(x)

# linspace
# return array of evenly spaced numbers
# [start,stop],number of samples
x = np.linspace(-100,100,500)
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
    # find value of tan that is close to zero
    # find x value of that point
    # tan seems to be an array of y values
    # fprime*(x-i) = -f(i) 
    tan = f(i)+fprime*(x-i)
    for y in tan:
        if y > -0.01 and y < 0.01:
            xValue = np.interp(y, x, )
    print i
    #tan = fprime*(x-i)
    line.set_data(x, tan)
    point.set_data(i,f(i))
    return line,

def animatePoint(i):
    point.set_data(i,f(i))
    return point,

plt.plot(x,y,'b')
animLine = animation.FuncAnimation(fig, animateLine, init_func=initLine, frames=15, interval=99)
animPoint = animation.FuncAnimation(fig, animatePoint, init_func=initPoint, frames=15, interval=99)
plt.show()

# NEWTON'S METHOD
# find tangent line of arbitrary point on graph (click graph?)
# find x-intercept of tangent line, when tan = 0
# find tangent line of f(x) at where tan = 0 

