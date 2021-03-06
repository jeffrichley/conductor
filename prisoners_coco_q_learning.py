import random

from utils import *
import numpy as np
from numpy import unravel_index
import itertools

# This is where we will keep our COCO-Q values for learning
p1_q_values_final = np.zeros((9, 9, 3, 3))
p2_q_values_final = np.zeros((9, 9, 3, 3))

last_p1_values = p1_q_values_final.copy()
last_p2_values = p2_q_values_final.copy()

all_states = list(itertools.product([0, 1, 2, 3, 4], [4, 5, 6, 7, 8]))
all_joint_action_pairs = list(itertools.product([0, 1, 2], [0, 1, 2]))

max_change = 10000
min_change = 10000
count = 0
changes = np.zeros(1000)

current_state = (3, 5)
previous_state = current_state

# main loop for training
while count < num_sessions:
    count += 1

    # if we are above the random threshold, take the highest reward action
    if random.random() >= epsilon:
        combined = p1_q_values_final[current_state] + p2_q_values_final[current_state]
        p1_action, p2_action = unravel_index(combined.argmax(), combined.shape)
    else:
        p1_action = np.random.randint(num_actions)
        p2_action = np.random.randint(num_actions)

    # if we finished the game last time, lets go to a random place to start
    if is_terminal_state(current_state):
        # current_state = random_state()
        current_state = (3, 5)
    else:

        if current_state == (1, 7):
            p1_action = 1
            p2_action = 0

        # what kind of rewards to we get for the state and joint action?
        p1_reward, p2_reward = get_rewards_for_state_joint_action(current_state, p1_action, p2_action)

        # take the actions
        state_prime = game_step(current_state, p1_action, p2_action)

        # 1. build up the payoff matrix of this state
        p1_payoff = p1_q_values_final[state_prime]
        p2_payoff = p2_q_values_final[state_prime]

        # 2. calculate the maxmax value of the two payoff matrices
        maxmax_value = ((p1_payoff + p2_payoff) / 2).max()

        # 3. calculate the minimax value for each player
        p1_minimax_value = minimax_value((p1_payoff - p2_payoff) / 2)
        # p2_minimax_value = minimax_value((p2_payoff.transpose() - p1_payoff.transpose()) / 2)
        p2_minimax_value = -p1_minimax_value

        # 4. calculate the coco value for each player
        p1_coco_value = maxmax_value + p1_minimax_value
        p2_coco_value = maxmax_value + p2_minimax_value

        # gather up the values for the update
        p1_q_s_a = p1_q_values_final[current_state][p1_action][p2_action]
        p2_q_s_a = p2_q_values_final[current_state][p1_action][p2_action]

        # perform the Q-Learning update
        p1_q_values_final[current_state][p1_action][p2_action] = p1_q_s_a + alpha * (p1_reward + gamma * p1_coco_value - p1_q_s_a)
        p2_q_values_final[current_state][p1_action][p2_action] = p2_q_s_a + alpha * (p2_reward + gamma * p2_coco_value - p2_q_s_a)

        # just some bookkeeping for logging
        max_change = max((p1_q_values_final - last_p1_values).max(), (p2_q_values_final - last_p2_values).max())
        changes[:-1] = changes[1:];
        changes[-1] = max_change

        last_p1_values = p1_q_values_final.copy()
        last_p2_values = p2_q_values_final.copy()

        # epsilon = decay_epsilon(count, 0.99)
        epsilon = max(0.05, epsilon * epsilon_decay)
        alpha = max(0.001, alpha * alpha_decay)

        previous_state = current_state
        current_state = state_prime

    if count % 1000 == 0 and count != 0:
        print(f'Round {count} {epsilon} {alpha} {np.mean(changes)} {max_change}')

state = (3, 5)
print('state     actions       resulting state')
print(f'start                   {state}')
while not is_terminal_state(state):

    combined = p1_q_values_final[state] + p2_q_values_final[state]
    p1_action, p2_action = unravel_index(combined.argmax(), combined.shape)
    next_state = game_step(state, p1_action, p2_action)

    print(f'\t{state} -> {action_space[p1_action]} {action_space[p2_action]:5} -> {next_state}')

    state = next_state


np.save('p1_policy', p1_q_values_final, allow_pickle=True)
np.save('p2_policy', p2_q_values_final, allow_pickle=True)
