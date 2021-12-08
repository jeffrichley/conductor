from prisoner_game import *
from utils import *
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# alpha = 0.2
# alpha_decay = 0.999995
# alpha = 1.0
alpha = 0.1
# alpha_decay = 0.999993
# alpha = 0.1
alpha_decay = 0.999995
# alpha_decay = 1
# alpha_decay = (0.001 * alpha)**(1./1000000.)
alpha_start = alpha

# quite it all down
# solvers.options['abstol'] = 1e-4 # Default is 1e-7
# solvers.options['reltol'] = 1e-4 # Default is 1e-6
# solvers.options['feastol'] = 1e-4 # Default is 1e-7
# solvers.options['show_progress'] = False
# solvers.options['glpk'] = {'msg_lev' : 'GLP_MSG_OFF', 'LPX_K_MSGLEV': 0}
# solvers.options['glpk'] = {'LPX_K_MSGLEV': 0}

import time
start_time = time.time()

# p1_q_values = {}
p1_v = {}
# p2_q_values = {}
p2_v = {}

random_start = False
epsilon_chance = 0.1

# for i in [0,1]: # who has the ball
#     for j in range(8): # p1's location
#         for k in range(8): # p2's location
for j in range(9): # p1's location
    for k in range(9): # p2's location
        new_state = (j, k)
        # TODO: need to change these to be 3x3 instead of 5x5
        # p1_q_values[new_state] = [[1, 1, 1],
        #                           [1, 1, 1],
        #                           [1, 1, 1]]
        # p1_q_values[new_state] = np.array([[0., 0., 0.],
        #                                    [0., 0., 0.],
        #                                    [0., 0., 0.]], dtype=np.float64)
        p1_v[new_state] = 1

        # p2_q_values[new_state] = np.array([[0., 0., 0.],
        #                                    [0., 0., 0.],
        #                                    [0., 0., 0.]], dtype=np.float64)
        p2_v[new_state] = 1

p1_q_values = np.zeros((9, 9, 3, 3))
p2_q_values = np.zeros((9, 9, 3, 3))
p1_q_single_values = np.zeros((9, 9, 3))
p2_q_single_values = np.zeros((9, 9, 3))

p1_normal_q_values = np.zeros((9, 9, 3, 3))
p2_normal_q_values = np.zeros((9, 9, 3, 3))

#TODO: temporarily hacking the final end goals
# for i in range(9):
#     p1_q_values[0][i] = 100
# for i in range(9):
#     p2_q_values[i][8] = 100
# p1_q_single_values[0] = 100
# p2_q_single_values[8] = 100

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
for t in tqdm(range(steps), mininterval=5):

    if is_terminal_state(current_state):
        complete = True
        # p1_reward, p2_reward = get_rewards(current_state)
        # p1_q_values[current_state][2][2] += alpha * (p1_reward - p1_q_values[current_state][2][2])
        # p2_q_values[current_state][2][2] += alpha * (p2_reward - p2_q_values[current_state][2][2])
        # p1_q_single_values[current_state[0]][current_state[1]][2] += alpha * (p1_reward - p1_q_values[current_state][2][2])
        # p2_q_single_values[current_state[0]][current_state[1]][2] += alpha * (p2_reward - p2_q_values[current_state][2][2])
    else:
        complete = False

        # 1. simulate actions a1, ..., an in state s
        # figure out what each player will do and simulate it
        if np.random.rand() <= epsilon_chance:
            # p1_current = p1_q_values[current_state]
            # p2_current = p2_q_values[current_state]
            # added = p1_current + p2_current
            # p1_action_sim, p2_action_sim = np.unravel_index(added.argmax(), added.shape)
            p1_action_sim = np.random.randint(3)
            p2_action_sim = np.random.randint(3)
        else:
            p1_action_sim = np.random.randint(3)
            p2_action_sim = np.random.randint(3)

        # p1_action_sim = 0
        # p2_action_sim = 1


        # 2. observe rewards R1, ..., Rn and next state s'
        # what is the new state?
        state_prime = game_step(current_state, p1_action_sim, p2_action_sim)
        p1_reward, p2_reward = get_rewards(state_prime)

        # if current_state == start_state and p1_action_sim == 0 and p2_action_sim == 1:
        #     print(p1_reward, p2_reward)


        q_s_a_1 = p1_q_values[current_state][p1_action_sim][p2_action_sim]
        q_s_a_2 = p2_q_values[current_state][p1_action_sim][p2_action_sim]



        p1_prime = p1_q_values[state_prime]
        p2_prime = p2_q_values[state_prime]
        # plus = p1_prime + p2_prime


        # p1_action_coco, p2_action_coco = np.unravel_index(plus.argmax(), plus.shape)

        p1_coco_value = get_coco_value(p1_prime, p2_prime)
        p2_coco_value = get_coco_value(p2_prime, p1_prime)

        # coco_value = get_coco_value(p1_prime, p2_prime)
        # p1_side_payment = coco_value - p1_prime[p1_action_coco][p2_action_coco]
        # p2_side_payment = -p1_side_payment

        # p1_side_payment = get_coco_value(p1_prime, p2_prime)
        # p2_side_payment = get_coco_value(p2_prime, p1_prime)

        # cost of each step is -1 except stick
        if p1_action_sim != 2 or True:
            p1_reward -= 1

        if p2_action_sim != 2 or True:
            p2_reward -= 1

        # state_prime = game_step(current_state, p1_action_coco, p2_action_coco)
        # p1_reward, p2_reward = get_rewards(state_prime)

        # side_payment_p1 = coco_value - p1[p1_action_coco][p2_action_coco]

        # p1_coco_reward = p1[p1_action_coco][p2_action_coco] + side_payment_p1
        # p2_coco_reward = p2[p1_action_coco][p2_action_coco] - side_payment_p1

        # p1_coco_value = get_coco_value(p1, p2)
        # p2_coco_value = get_coco_value(p2, p1)

        # p2_coco_reward = p2[p2_action_coco][p2_action_coco]
        # p2_coco_value = -p1_coco_value



        # q_s_a_1 = p1_q_values[current_state][p1_action_coco][p2_action_coco]
        # q_s_a_2 = p2_q_values[current_state][p1_action_coco][p2_action_coco]

        # update the Q values

        p1_q_values[current_state][p1_action_sim][p2_action_sim] = q_s_a_1 + alpha * (p1_reward + gamma * p1_coco_value - q_s_a_1)
        p2_q_values[current_state][p1_action_sim][p2_action_sim] = q_s_a_2 + alpha * (p2_reward + gamma * p2_coco_value - q_s_a_2)

        p1_normal_qsa = p1_normal_q_values[current_state][p1_action_sim][p2_action_sim]
        p1_next_max = p1_normal_q_values[state_prime].max()
        p1_normal_q_values[current_state][p1_action_sim][p2_action_sim] = p1_normal_qsa + alpha * (p1_reward + gamma * p1_next_max - p1_normal_qsa)

        p2_normal_qsa = p2_normal_q_values[current_state][p1_action_sim][p2_action_sim]
        p2_next_max = p2_normal_q_values[state_prime].max()
        p2_normal_q_values[current_state][p1_action_sim][p2_action_sim] = p2_normal_qsa + alpha * (p2_reward + gamma * p2_next_max - p2_normal_qsa)


        # p1_q_values[current_state][p1_action_sim][p2_action_sim] = q_s_a_1 + alpha * (p1_reward + gamma * p1_side_payment - q_s_a_1)
        # p2_q_values[current_state][p1_action_sim][p2_action_sim] = q_s_a_2 + alpha * (p2_reward + gamma * p2_side_payment - q_s_a_2)
        # p1_q_single_values[current_state[0]][current_state[1]][p1_action_sim] = q_s_a_1 + alpha * (p1_reward + gamma * p1_side_payment - q_s_a_1)
        # p2_q_single_values[current_state[0]][current_state[1]][p2_action_sim] = q_s_a_2 + alpha * (p2_reward + gamma * p2_side_payment - q_s_a_2)

        # p1_q_values[current_state][p1_action_sim][p2_action_sim] = q_s_a_1 + alpha * (p1_reward + gamma * p1_coco_value - q_s_a_1)
        # p2_q_values[current_state][p1_action_sim][p2_action_sim] = q_s_a_2 + alpha * (p2_reward + gamma * p2_coco_value - q_s_a_2)
        # p1_q_single_values[current_state[0]][current_state[1]][p1_action_sim] = q_s_a_1 + alpha * (p1_reward + gamma * p1_coco_value - q_s_a_1)
        # p2_q_single_values[current_state[0]][current_state[1]][p2_action_sim] = q_s_a_2 + alpha * (p2_reward + gamma * p2_coco_value - q_s_a_2)


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
ax.set_ylim([0.0, 0.5])
ax.set_xlim([0.0, steps])
ax.xaxis.set_major_locator(plt.MaxNLocator(10))
ax.ticklabel_format(style='sci', axis='x', scilimits=(5, 5), useMathText=True)

plt.title('Correlated-Q')
plt.ylabel('Q-value Difference')
plt.xlabel('Simulation Iteration')

plt.savefig('coco-q-' + str(alpha_start) + '-' + str(gamma) + '.png')

# plt.show()
# plt.clf()

# print(max(plot_values))

np.save('p1_policy', p1_q_values, allow_pickle=True)
np.save('p2_policy', p2_q_values, allow_pickle=True)
np.save('p1_normal_policy', p1_normal_q_values, allow_pickle=True)
np.save('p2_normal_policy', p2_normal_q_values, allow_pickle=True)

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

