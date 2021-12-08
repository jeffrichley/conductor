# from game import *
from prisoner_game import *
from utils import *
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import itertools
from itertools import permutations

from cvxopt.modeling import op
from cvxopt.modeling import variable
from cvxopt.solvers import options

alpha = 1.0
alpha_decay = 0.999995
alpha_start = alpha

# quite it all down
options['show_progress'] = False

import time
start_time = time.time()

random_start = False
epsilon_chance = 0.1


p1_q_values = np.zeros((9, 9, 3, 3))
p2_q_values = np.zeros((9, 9, 3, 3))
p1_q_single_values = np.zeros((9, 9, 3))
p2_q_single_values = np.zeros((9, 9, 3))


old_value = p1_q_values[start_state][1][0]
last_good_plot_value = 100
game_steps = 0
plot_values = []

current_state = start_state
collect = False

f = open('ce-'+str(alpha_decay) + '-' + str(alpha) + '-' + str(epsilon_chance) + '.csv', "w+")

last_p1_values = p1_q_values.copy()
last_p2_values = p2_q_values.copy()

steps = num_sessions
for t in tqdm(range(1), mininterval=5):

    if is_terminal_state(current_state):
        complete = True
        # p1_reward, p2_reward = get_rewards(current_state)
        # p1_q_values[current_state][2][2] += alpha * (p1_reward - p1_q_values[current_state][2][2])
        # p2_q_values[current_state][2][2] += alpha * (p2_reward - p2_q_values[current_state][2][2])
        # p1_q_single_values[current_state[0]][current_state[1]][2] += alpha * (p1_reward - p1_q_values[current_state][2][2])
        # p2_q_single_values[current_state[0]][current_state[1]][2] += alpha * (p2_reward - p2_q_values[current_state][2][2])
    else:
        complete = False

    new_p1_q_single_values = p1_q_single_values.copy()
    new_p2_q_single_values = p2_q_single_values.copy()

    for p1_position in range(1, 4):
        for p2_position in range(5, 8):

            for p1_action in range(len(action_space)):
                for p2_action in range(len(action_space)):
                    if p1_position == 3 and p2_position == 5 and p1_action == 0 and p2_action == 1:
                        state_prime = game_step(current_state, p1_action, p2_action)
                        # p1_reward, p2_reward = get_rewards(state_prime)

                        new_p1_q_single_values[p1_position][p2_position][p1_action] += 0.5 * 100 + 0.5 * 100
                        new_p2_q_single_values[p1_position][p2_position][p1_action] += 0.5 * 100 + 0.5 * 100

                    else:
                        state_prime = game_step(current_state, p1_action, p2_action)
                        p1_reward, p2_reward = get_rewards(state_prime)

                        new_p1_q_single_values[p1_position][p2_position][p1_action] += p1_reward + gamma * p1_q_single_values[state_prime].max()
                        new_p2_q_single_values[p1_position][p2_position][p1_action] += p2_reward + gamma * p2_q_single_values[state_prime].max()

    p1_q_single_values = new_p1_q_single_values
    p2_q_single_values = new_p2_q_single_values


    diff = ((np.abs(p1_q_values) - np.abs(last_p1_values))).sum()

    last_p1_values = p1_q_values.copy()
    last_p2_values = p2_q_values.copy()

    # if t % 1000 == 0 and abs(diff) > 0.0:
    #     print(diff)


    # save data for plotting
    # new_value = p1_q_values[start_state][1][0]
    # tmp = new_value - old_value
    tmp = diff
    if abs(tmp) > 0.0:
        f.write(str(t) + ',' + str(abs(tmp)) + '\n')
        f.flush()

    if tmp == 0 and len(plot_values) > 0:
        tmp = plot_values[-1]
    plot_value = abs(tmp)
    plot_values.append(plot_value)
    # if t % 100 == 0:
    #     length = (time.time() - start_time)
        # print(t, plot_value, alpha, length, epsilon_chance, alpha_start)
    # old_value = new_value

    game_steps += 1

    # if p1_reward != 0 or p2_reward != 0:
    if complete:
        complete = False
        # if we are acting via exploration...
        if np.random.rand() <= epsilon_chance:
            current_state = random_state()
        else:
            # if we are behaving "rationally"
            current_state = start_state
        game_steps = 0
    elif game_steps > num_plays:
        # if we are acting via exploration...
        if np.random.rand() <= epsilon_chance:
            current_state = random_state()
        else:
            # if we are behaving "rationally"
            current_state = start_state
        game_steps = 0
    else:
        current_state = state_prime

    # 6. decay alpha according to decay schedule
    # alpha = max(0.001, alpha * alpha_decay)

    # epsilon = decay_epsilon(t, epsilon)

f.close()

print('generating plot')

plt.rcParams['agg.path.chunksize'] = 1000

x = range(len(plot_values))
y = plot_values
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y, c='b', label='y1', linewidth=0.75)
# ax.set_ylim([0.0, 0.5])
ax.set_xlim([0.0, steps])
ax.xaxis.set_major_locator(plt.MaxNLocator(10))
ax.ticklabel_format(style='sci', axis='x', scilimits=(5, 5), useMathText=True)

plt.title('Correlated-Q')
plt.ylabel('Q-value Difference')
plt.xlabel('Simulation Iteration')

plt.savefig('ce-from-foe-' + str(alpha_start) + '-' + str(gamma) + '.png')

# plt.show()
# plt.clf()

# print(max(plot_values))

for i in range(3, -1, -1):
    # print(p1_q_values[start_state])
    # print(p2_q_values[start_state])
    print((i, 5))
    print(p1_q_values[(i, 5)])
    print(p2_q_values[(i, 5)])
    print(p1_q_values[(i, 5)] + p2_q_values[(i, 5)])
    print(p1_q_single_values[i][5])
    print(p2_q_single_values[i][5])

    print(get_coco_value(p1_q_values[(i, 5)], p2_q_values[(i, 5)]))

    print('------------------------')

