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

# main loop for training
while max_change > 0.01:
    print(f'Round {count}')
    count += 1
    for state in all_states:
        for p1_joint_action, p2_joint_action in all_joint_action_pairs:

            if not is_terminal_state(state):
                p1_reward, p2_reward = get_rewards_for_state_joint_action(state, p1_joint_action, p2_joint_action)

                state_prime = game_step(state, p1_joint_action, p2_joint_action)

                # 1. build up the payoff matrix of this state
                p1_payoff = p1_q_values_final[state_prime]
                p2_payoff = p2_q_values_final[state_prime]

                # 2. calculate the maxmax value of the two payoff matrices
                maxmax_value = ((p1_payoff + p2_payoff) / 2).max()

                # 3. calculate the minimax value for each player
                p1_minimax_value = minimax_value((p1_payoff - p2_payoff) / 2)
                p2_minimax_value = minimax_value((p2_payoff.transpose() - p1_payoff.transpose()) / 2)

                # 4. calculate the coco value for each player
                p1_coco_value = maxmax_value + p1_minimax_value
                p2_coco_value = maxmax_value + p2_minimax_value

                discount = 0.99
                p1_q_values_final[state][p1_joint_action][p2_joint_action] = p1_reward + discount * p1_coco_value
                p2_q_values_final[state][p1_joint_action][p2_joint_action] = p2_reward + discount * p2_coco_value

    max_change = max((p1_q_values_final - last_p1_values).max(), (p2_q_values_final - last_p2_values).max())

    last_p1_values = p1_q_values_final.copy()
    last_p2_values = p2_q_values_final.copy()


state = (3, 5)
print('state     actions       resulting state')
print(f'start                   {state}')
while not is_terminal_state(state):
    combined = p1_q_values_final[state] + p2_q_values_final[state]
    p1_action, p2_action = unravel_index(combined.argmax(), combined.shape)
    next_state = game_step(state, p1_action, p2_action)

    print(f'+{state} -> {action_space[p1_action]} {action_space[p2_action]:5} -> {next_state}')
    print(combined)

    state = next_state
