import numpy as np
import matplotlib.pyplot as plt

from prisoner_game import *


steps = num_sessions

plot_values = np.genfromtxt('ce-0.999995-0.6-0.1.csv', delimiter=',')
x = plot_values[:,0]
y = plot_values[:,1]
print(x)

print(plot_values)

plt.rcParams['agg.path.chunksize'] = 1000

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y, c='b', label='y1', linewidth=0.75)
ax.set_ylim([0.0, 0.5])
ax.set_xlim([0.0, steps])
ax.xaxis.set_major_locator(plt.MaxNLocator(10))
ax.ticklabel_format(style='sci', axis='x', scilimits=(5, 5), useMathText=True)


plt.title('Correlated-Q')
plt.ylabel('Q-value Difference')
plt.xlabel('Simulation Iteration')

plt.show()
