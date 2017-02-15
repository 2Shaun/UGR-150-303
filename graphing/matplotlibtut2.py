import matplotlib.pyplot as plt

# easier to create a function which defines the x variables
# rather than hard coding coordinates like this
x = [1,2,3]
y = [5,7,4]

x2 = [1,2,3]
y2 = [10,14,12]

plt.plot(x,y,label='First Line')
plt.plot(x2,y2,label='Second Line')
plt.xlabel('Plot Number')
plt.ylabel('Dependant Variable')

plt.title('Interesting Graph')
plt.legend()
plt.show()
