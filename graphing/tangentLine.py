import numpy as np
from matplotlib import pyplot as plt

fig = plt.figure()
ax = plt.axes(xlim=(-50,50), ylim=(-500,500))
line, = ax.plot([], [], '--r')
point, = ax.plot([], [], 'om')

def f(x):
    return np.power(2, x)

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

# arbirtrarily close to 0
h = 0.1
# i = iterator
# [f(i+h) - f(i)]/
# h
a = 2
fprime = (f(a+h)-f(a))/h
tan = f(a)+fprime*(x-a)
inverse = ((x-f(a))*h)/(f(a+h)-f(a)) + a
root = ((0-f(a))*h)/(f(a+h)-f(a)) + a
line.set_data(x, tan)
point.set_data(a,f(a))

plt.plot(x,y,'b')
plt.show()
