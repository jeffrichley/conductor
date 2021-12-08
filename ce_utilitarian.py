# from game import *
from prisoner_game import *
from utils import *
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from cvxopt.modeling import op
from cvxopt.modeling import variable
from cvxopt.solvers import options

# alpha = 0.2
# alpha_decay = 0.999995
# alpha = 1.0
# alpha_decay = 0.999993
alpha = 0.6
alpha_decay = 0.999995
# alpha_decay = (0.001 * alpha)**(1./1000000.)
alpha_start = alpha

# quite it all down
options['show_progress'] = False
# solvers.options['abstol'] = 1e-4 # Default is 1e-7
# solvers.options['reltol'] = 1e-4 # Default is 1e-6
# solvers.options['feastol'] = 1e-4 # Default is 1e-7
# solvers.options['show_progress'] = False
# solvers.options['glpk'] = {'msg_lev' : 'GLP_MSG_OFF', 'LPX_K_MSGLEV': 0}
# solvers.options['glpk'] = {'LPX_K_MSGLEV': 0}

import time
start_time = time.time()

p1_q_values = {}
p1_v = {}
p2_q_values = {}
p2_v = {}

random_start = False
epsilon_chance = 0.1

for i in [0,1]: # who has the ball
    for j in range(8): # p1's location
        for k in range(8): # p2's location
            new_state = (i, j, k)
            p1_q_values[new_state] = [[1,1,1,1,1],
                                      [1,1,1,1,1],
                                      [1,1,1,1,1],
                                      [1,1,1,1,1],
                                      [1,1,1,1,1]]
            p1_v[new_state] = 1

            p2_q_values[new_state] = [[1,1,1,1,1],
                                      [1,1,1,1,1],
                                      [1,1,1,1,1],
                                      [1,1,1,1,1],
                                      [1,1,1,1,1]]
            p2_v[new_state] = 1

old_value = p1_q_values[start_state][3][4]
last_good_plot_value = 100
game_steps = 0
plot_values = []

current_state = start_state
collect = False

f = open('ce-'+str(alpha_decay) + '-' + str(alpha) + '-' + str(epsilon_chance) + '.csv', "w+")

steps = num_sessions
for t in tqdm(range(steps), mininterval=5):

    # 1. simulate actions a1, ..., an in state s
    # figure out what each player will do and simulate it
    p1_action = np.random.randint(5)
    p2_action = np.random.randint(5)

    # 2. observe rewards R1, ..., Rn and next state s'
    # what is the new state?
    state_prime = game_step(current_state, p1_action, p2_action)
    p1_reward, p2_reward = get_rewards(state_prime)

    # 3. for i = 1 to n
    # 3.(a) Vi(s') = fi(Q1(s'), . . . , Qn(s'))
    # 3.(b) Qi(s,a) = (1 - alpha)Qi(s,a) + alpha[(1-gamma)Ri + gammaVi(s')]

    constraints = list()
    joint_actions = {}

    # declare the variables
    v = variable()
    sum_to_one = 0

    # create a variable for each action pair
    for p1 in range(len(action_space)):
        for p2 in range(len(action_space)):
            action = variable()
            joint_actions[(p1, p2)] = action

            # each action needs to be greater than 0
            constraints.append(action >= 0)

            # all joint actions added together must be 1.0
            sum_to_one += action

    # probabilities all need to add up to 1.0
    # constraints.append(r + p + s == 1)
    constraints.append(sum_to_one == 1.0)




    # for i in range(3):
    #     constrs.append(values[i][0] * r + values[i][1] * p + values[i][2] * s >= v)
    # probabilities * values need to be greater than the value for each row

    # now we need to add all of the constraints for player 1 and the relationships between themselves
    # should be 20 for player 1
    # expectation of first is >= expectation of all the second, third, fourth, fifth.  Do that for all 5
    for i in range(len(action_space)):
        this_one = 0
        # setup the left hand side
        for j in range(len(action_space)):
            this_one += joint_actions[(i, j)] * p1_q_values[state_prime][i][j]

        for k in range(len(action_space)):
            # don't need to compare this_one to itself
            if i != k:
                other = 0
                # setup the right hand side
                for l in range(len(action_space)):
                    other += joint_actions[(i, l)] * p1_q_values[state_prime][k][l]
                constraints.append((this_one >= other))

    # need to do the same thing for player 2, just switch the rows and columns this time
    # should be 20 for player 2
    for i in range(len(action_space)):
        this_one = 0
        # setup the left hand side
        for j in range(len(action_space)):
            this_one += joint_actions[(j, i)] * p2_q_values[state_prime][j][i]

        for k in range(len(action_space)):
            # don't need to compare this_one to itself
            if i != k:
                other = 0
                # setup the right hand side
                for l in range(len(action_space)):
                    other += joint_actions[(l, i)] * p2_q_values[state_prime][l][k]
                constraints.append((this_one >= other))

    # Now that hurt my brain, pretty sure it is good.

    # Now we need to tell it that the summation of each player is our max, that is what we want
    # essentially this is our objective function.  This is different for each of the CE types.
    # This is the utilitarian version.  Maximize the sum of the two players.
    # Make sure to use the expectation.
    sum_total = 0
    for i in range(len(action_space)):
        for j in range(len(action_space)):
            probability = joint_actions[(i, j)]
            sum_total += probability * p1_q_values[state_prime][i][j]
            sum_total += probability * p2_q_values[state_prime][i][j]

    constraints.append(v == sum_total)


    # minimize negative v to get the max value
    lp = op(-v, constraints)
    # lp.solve(solver='glpk')
    lp.solve()

    max_q_value = v.value[0]

    # ok, I think what we need to do here is calculate p1_v and p2_v by using the probabilities that they each would
    # have taken times what they would have gotten for the next states had they taken the actions with calculated probabilities
    p1_value = 0
    p2_value = 0
    for i in range(len(action_space)):
        for j in range(len(action_space)):
            p1_value += joint_actions[(i, j)].value[0] * p1_q_values[state_prime][i][j]
            p2_value += joint_actions[(i, j)].value[0] * p2_q_values[state_prime][i][j]

    p1_v[state_prime] = p1_value
    p2_v[state_prime] = p2_value

    q_s_a_1 = p1_q_values[current_state][p1_action][p2_action]
    q_s_a_2 = p2_q_values[current_state][p1_action][p2_action]

    # update the Q values
    p1_q_values[current_state][p1_action][p2_action] = (1-alpha)*q_s_a_1 + alpha*((1-gamma)*p1_reward + gamma*p1_v[state_prime])
    p2_q_values[current_state][p1_action][p2_action] = (1-alpha)*q_s_a_2 + alpha*((1-gamma)*p2_reward + gamma*p2_v[state_prime])

    # save data for plotting
    new_value = p1_q_values[start_state][3][4]
    tmp = new_value - old_value

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
    old_value = new_value

    game_steps += 1

    if p1_reward != 0:
        # if we are acting via exploration...
        if np.random.rand() <= epsilon_chance:
            current_state = start_state
        else:
            # if we are behaving "rationally"
            current_state = random_state()
        game_steps = 0
    elif game_steps > num_plays:
        # if we are acting via exploration...
        if np.random.rand() <= epsilon_chance:
            current_state = start_state
        else:
            # if we are behaving "rationally"
            current_state = random_state()
        game_steps = 0
    else:
        current_state = state_prime

    # 6. decay alpha according to decay schedule
    alpha = max(0.001, alpha * alpha_decay)

    epsilon = decay_epsilon(t, epsilon)

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

plt.savefig('ce-from-foe-'+str(alpha_decay) + '-' + str(alpha_start) + '-' + str(epsilon_chance) + '.png')

plt.show()
plt.clf()

print(max(plot_values))