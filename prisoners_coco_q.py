from prisoner_game import *
from utils import *
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

alpha = 0.1
alpha_start = alpha

random_start = False
epsilon_chance = 0.1

# This is where we will keep our COCO-Q values for learning
p1_q_values = np.zeros((9, 9, 3, 3))
p2_q_values = np.zeros((9, 9, 3, 3))

# This is where we will keep our Q-learning values for comparison with COCO-Q
p1_normal_q_values = np.zeros((9, 9, 3, 3))
p2_normal_q_values = np.zeros((9, 9, 3, 3))

game_steps = 0

current_state = start_state
collect = False

last_p1_values = p1_q_values.copy()
last_p2_values = p2_q_values.copy()

steps = num_sessions

# main loop for training
for t in tqdm(range(steps), mininterval=5):

    if is_terminal_state(current_state):
        complete = True
    else:
        complete = False

        # 1. simulate actions a1, ..., an in state s
        # figure out what each player will do and simulate it
        if np.random.rand() <= epsilon_chance:
            # this will allow us to take a greedy action that has been previously learned
            # p1_current = p1_q_values[current_state]
            # p2_current = p2_q_values[current_state]
            # added = p1_current + p2_current
            # p1_action_sim, p2_action_sim = np.unravel_index(added.argmax(), added.shape)

            p1_action_sim = np.random.randint(3)
            p2_action_sim = np.random.randint(3)
        else:
            p1_action_sim = np.random.randint(3)
            p2_action_sim = np.random.randint(3)

        # 2. observe rewards R1, ..., Rn and next state s'
        # what is the new state?
        state_prime = game_step(current_state, p1_action_sim, p2_action_sim)
        p1_reward, p2_reward = get_rewards(state_prime)

        # gathering information for the Q update
        q_s_a_1 = p1_q_values[current_state][p1_action_sim][p2_action_sim]
        q_s_a_2 = p2_q_values[current_state][p1_action_sim][p2_action_sim]

        p1_prime = p1_q_values[state_prime]
        p2_prime = p2_q_values[state_prime]

        p1_coco_value = get_coco_value(p1_prime, p2_prime)
        p2_coco_value = get_coco_value(p2_prime, p1_prime)

        # cost of each step is -1 except stick
        # if p1_action_sim != 2:
        #     p1_reward -= 1
        #
        # if p2_action_sim != 2:
        #     p2_reward -= 1

        # for now we will have all moves get a reward of -1
        p1_reward -= 1
        p2_reward -= 1

        # update the COCO-Q values
        p1_q_values[current_state][p1_action_sim][p2_action_sim] = q_s_a_1 + alpha * (p1_reward + gamma * p1_coco_value - q_s_a_1)
        p2_q_values[current_state][p1_action_sim][p2_action_sim] = q_s_a_2 + alpha * (p2_reward + gamma * p2_coco_value - q_s_a_2)

        # update the normal Q-learning values
        # TODO: is this correct?  Do we just get a max or do we need probabilities for play?
        p1_normal_qsa = p1_normal_q_values[current_state][p1_action_sim][p2_action_sim]
        p1_next_max = p1_normal_q_values[state_prime].max()
        p1_normal_q_values[current_state][p1_action_sim][p2_action_sim] = p1_normal_qsa + alpha * (p1_reward + gamma * p1_next_max - p1_normal_qsa)

        p2_normal_qsa = p2_normal_q_values[current_state][p1_action_sim][p2_action_sim]
        p2_next_max = p2_normal_q_values[state_prime].max()
        p2_normal_q_values[current_state][p1_action_sim][p2_action_sim] = p2_normal_qsa + alpha * (p2_reward + gamma * p2_next_max - p2_normal_qsa)

    diff = ((np.abs(p1_q_values) - np.abs(last_p1_values))).sum()

    last_p1_values = p1_q_values.copy()
    last_p2_values = p2_q_values.copy()

    # tmp = diff
    # if abs(tmp) > 0.0:
    #     f.write(str(t) + ',' + str(abs(tmp)) + '\n')
    #     f.flush()

    game_steps += 1

    # if we have finished that round, reset and start over again
    if complete:
        complete = False
        # if we are acting via exploration...
        if np.random.rand() <= epsilon_chance:
            current_state = random_state()
        else:
            # if we are behaving "rationally"
            current_state = start_state
        game_steps = 0
    else:
        current_state = state_prime

    # 6. decay alpha and epsilon according to decay schedule
    # alpha = max(0.001, alpha * alpha_decay)
    # epsilon = decay_epsilon(t, epsilon)

# save the learned policies for analysis
np.save('p1_policy', p1_q_values, allow_pickle=True)
np.save('p2_policy', p2_q_values, allow_pickle=True)
np.save('p1_normal_policy', p1_normal_q_values, allow_pickle=True)
np.save('p2_normal_policy', p2_normal_q_values, allow_pickle=True)

for i in range(3, -1, -1):
    print((i, 5))
    print(p1_q_values[(i, 5)])
    print(p2_q_values[(i, 5)])
    print(p1_q_values[(i, 5)] + p2_q_values[(i, 5)])
    print(get_coco_value(p1_q_values[(i, 5)], p2_q_values[(i, 5)]))
    print('------------------------')

