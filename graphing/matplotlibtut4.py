import matplotlib.pyplot as plt

x = [1,2,3,4,5,6,7,8]
y = [5,2,3,4,5,6,7,4]

#scatter plots show a correlation/distribution/relationship two-variables (x,y)
plt.scatter(x,y, label='scat', color='k', marker='^', s=100)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()
