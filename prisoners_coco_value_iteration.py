from utils import *
import numpy as np
from numpy import unravel_index
import itertools

# This is where we will keep our COCO-Q values for learning
p1_q_values_final = np.zeros((9, 9))
p2_q_values_final = np.zeros((9, 9))

last_p1_values = p1_q_values_final.copy()
last_p2_values = p2_q_values_final.copy()

all_states = list(itertools.product([0, 1, 2, 3, 4], [4, 5, 6, 7, 8]))

max_change = 10000
min_change = 10000
count = 0

# main loop for training
while max_change > 0.01:
    count += 1
    for state in all_states:

        # if state[0] == state[1]:
        #     continue

        # 1. build up the payoff matrix of this state
        p1_payoff, p2_payoff = get_payoff_matrices_for_state(state, p1_q_values_final, p2_q_values_final)

        # 2. calculate the maxmax value of the two payoff matrices
        maxmax_value = ((p1_payoff + p2_payoff) / 2).max()

        # 3. calculate the minimax value for each player
        p1_minimax_value = minimax_value((p1_payoff - p2_payoff) / 2)
        # TODO: do we actually need to calculate this?  it may always be the negative of
        #       each other because it is a zero sum game?
        p2_minimax_value = minimax_value((p2_payoff.transpose() - p1_payoff.transpose()) / 2)
        # p2_minimax_value = -1 * p1_minimax_value

        # 4. calculate the coco value for each player
        p1_coco_value = maxmax_value + p1_minimax_value
        p2_coco_value = maxmax_value + p2_minimax_value

        # 5. update the q values for the current state
        discount = 0.99
        p1_q_values_final[state] = p1_coco_value * discount
        p2_q_values_final[state] = p2_coco_value * discount

    print(f'step {count} max change: {max_change}')

    max_change = max((p1_q_values_final - last_p1_values).max(), (p2_q_values_final - last_p2_values).max())
    min_change = min(min_change, max_change)

    last_p1_values = p1_q_values_final.copy()
    last_p2_values = p2_q_values_final.copy()

print(f'Performed {count} value iterations')

# 6. move to a new state
# figure out what each player will do and simulate it
current_state = (3, 5)
print('state     actions       resulting state')
while not is_terminal_state(current_state):
    # this will allow us to take a greedy action that has been previously learned
    # TODO: I don't like how we have to make this every time
    p1_expectations = np.zeros((3, 3))
    p2_expectations = np.zeros((3, 3))

    all_joint_action_pairs = list(itertools.product([0, 1, 2], [0, 1, 2]))

    p1_best_reward = -999999
    p2_best_reward = -999999

    for p1_joint_action, p2_joint_action in all_joint_action_pairs:
        p1_reward, p2_reward = get_rewards_for_state_joint_action(current_state, p1_joint_action, p2_joint_action)

        p1_best_reward = max(p1_reward, p1_best_reward)
        p2_best_reward = max(p2_reward, p2_best_reward)

        state_prime = game_step(current_state, p1_joint_action, p2_joint_action)

        p1_value = p1_reward + p1_q_values_final[state_prime]
        p2_value = p2_reward + p2_q_values_final[state_prime]
        # p1_value = p1_q_values_final[state_prime]
        # p2_value = p2_q_values_final[state_prime]

        # p1_expectations[p1_joint_action][p2_joint_action] = p1_q_values_final[state_prime]
        # p2_expectations[p1_joint_action][p2_joint_action] = p2_q_values_final[state_prime]
        p1_expectations[p1_joint_action][p2_joint_action] = p1_value
        p2_expectations[p1_joint_action][p2_joint_action] = p2_value

    combined_expectations = p1_expectations + p2_expectations

    # print(combined_expectations[(0, 1)] == combined_expectations[(2, 1)])
    # print(combined_expectations[(0, 1)] - combined_expectations[(2, 1)])

    p1_action, p2_action = unravel_index(combined_expectations.argmax(), combined_expectations.shape)
    prev_state = current_state
    current_state = game_step(current_state, p1_action, p2_action)

    print(f'{prev_state} -> {action_space[p1_action]} {action_space[p2_action]:5} -> {current_state}')
    print(f'\tBest individual payouts would be: p1 {p1_best_reward} p2 {p2_best_reward}')
    # print(combined_expectations[p1_action, p2_action])
    # print('p1')
    # print(p1_expectations)
    # print('p2')
    # print(p2_expectations)
    # print(combined_expectations)

    # else:
    #     p1_action = np.random.randint(3)
    #     p2_action = np.random.randint(3)

        # pass

# print(p1_q_values_final)
# print(p2_q_values_final)



