import matplotlib.pyplot as plt
import numpy as np


def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def moving_average(a, n=100) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


data = np.load('burgle_one_player_scores.npy')
roll_mvg_avg = moving_average(data)
roll_std = np.std(rolling_window(data, 100), 1)

# print(data.shape)

plt.plot(data, color='lightblue', label='Game Scores')
plt.plot(roll_mvg_avg, label='Rolling Mean')
plt.plot(roll_mvg_avg + roll_std, color='gainsboro', label='+ sdv')
plt.plot(roll_mvg_avg - roll_std, color='gainsboro', label='- sdv')

plt.axhline(y=91, color='limegreen', linestyle='-', label='Solved')

plt.ylabel('Score')
plt.xlabel('Game Number')
plt.ylim([-250, 140])
plt.xlim([0, 10000])

plt.legend(loc=4)
plt.title('Rolling Mean (100) of Training Scores')

plt.savefig('burgle_one_player_scores.png')

plt.show()


