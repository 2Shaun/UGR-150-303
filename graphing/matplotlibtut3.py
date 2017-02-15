import matplotlib.pyplot as plt

population_ages =  [22,55,62,46,2,4,5,120,30,45,84,73,45,34,23,45,22,100,34,5,3,4,52,29,93,73,52,10,13,34,63,100,34,20,1,2,4]

ids = [x for x in range(len(population_ages))]

# bar graphs only really show who's the oldest
# plt.bar(ids, population_ages)

# bin - British version of a box
bins = [0,10,20,30,40,50,60,70,80,90,100,110,120,130]

# histograms show distribution
plt.hist(population_ages, bins, histtype='bar', rwidth=0.8)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()
