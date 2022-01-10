from prisoner_game import *
from utils import *
import numpy as np
from numpy import unravel_index
import matplotlib.pyplot as plt
from tqdm import tqdm
import itertools


alpha = 0.1
alpha_start = alpha

random_start = False
epsilon_chance = 0.1

# This is where we will keep our COCO-Q values for learning
p1_q_values = np.zeros((9, 9))
p2_q_values = np.zeros((9, 9))

game_steps = 0

current_state = start_state
collect = False

last_p1_values = p1_q_values.copy()
last_p2_values = p2_q_values.copy()

steps = num_sessions

# current_state = (2, 5)

# main loop for training
for t in tqdm(range(steps), mininterval=5):

    if is_terminal_state(current_state):
        complete = True
    else:
        complete = False

        # 1. build up the payoff matrix of this state
        p1_payoff, p2_payoff = get_payoff_matrices_for_state(current_state, p1_q_values, p2_q_values)

        # 2. calculate the maxmax value of the two payoff matrices
        maxmax_value = ((p1_payoff + p2_payoff) / 2).max()

        # 3. calculate the minimax value for each player
        p1_minimax_value = minimax_value((p1_payoff - p2_payoff) / 2)
        # TODO: do we actually need to calculate this?  it may always be the negative of
        #       each other because it is a zero sum game?
        p2_minimax_value = minimax_value((p2_payoff.transpose() - p1_payoff.transpose()) / 2)

        # 4. calculate the coco value for each player
        p1_coco_value = maxmax_value + p1_minimax_value
        p2_coco_value = maxmax_value + p2_minimax_value

        # 5. update the q values for the current state
        p1_q_values[current_state] = p1_coco_value
        p2_q_values[current_state] = p2_coco_value

        # 6. move to a new state
        # figure out what each player will do and simulate it
        if np.random.rand() >= epsilon_chance:
            # this will allow us to take a greedy action that has been previously learned
            # TODO: I don't like how we have to make this every time
            p1_expectations = np.zeros((3, 3))
            p2_expectations = np.zeros((3, 3))

            all_joint_action_pairs = list(itertools.product([0, 1, 2], [0, 1, 2]))

            for p1_joint_action, p2_joint_action in all_joint_action_pairs:
                state_prime = game_step(current_state, p1_joint_action, p2_joint_action)
                p1_expectations[p1_joint_action][p2_joint_action] = p1_q_values[state_prime]
                p2_expectations[p1_joint_action][p2_joint_action] = p2_q_values[state_prime]

            combined_expectations = p1_expectations + p2_expectations

            p1_action, p2_action = unravel_index(combined_expectations.argmax(), combined_expectations.shape)

        else:
            p1_action = np.random.randint(3)
            p2_action = np.random.randint(3)

        pass





