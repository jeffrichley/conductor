import random

from turn_util import *
import numpy as np
from numpy import unravel_index
import itertools
from tqdm import tqdm

from turn_turkey_game import *
from turn_prisoner_game import *


# game = TurnTurkey()
game = TurnPrisoner()


# This is where we will keep our COCO-Q values for learning
p1_q_values_final = np.zeros((game.num_spaces, game.num_spaces, game.num_actions), dtype=np.float64)
p2_q_values_final = np.zeros((game.num_spaces, game.num_spaces, game.num_actions), dtype=np.float64)

last_p1_values = p1_q_values_final.copy()
last_p2_values = p2_q_values_final.copy()

max_change = 10000
min_change = 10000
count = 0
changes = np.zeros(1000)

current_state = game.start_state
previous_state = current_state


def get_max_moves():
    best_score = -9999999
    best_p1_action = None
    best_p2_action = None

    # look at all the combos of moves to find the maximum combined scoring move
    for p1_temp_action in range(game.num_actions):
        p1_value = p1_q_values_final[current_state][p1_temp_action]

        # let the first player take a step
        p1_new_location_tmp, p2_new_location_tmp, reward_tmp = game.game_step(current_state, p1_temp_action, 0)
        next_state_tmp = (p1_new_location_tmp, p2_new_location_tmp)

        # now let p2 take check for their max
        p2_temp_action = p2_q_values_final[next_state_tmp].argmax()
        p2_value = p2_q_values_final[next_state_tmp][p2_temp_action]

        if p1_value + p2_value > best_score:
            best_score = p1_value + p2_value
            best_p1_action = p1_temp_action
            best_p2_action = p2_temp_action

    return best_p1_action, best_p2_action, best_score


# main loop for training
# while count < game.num_sessions:
for _ in tqdm(range(game.num_sessions), mininterval=2):
    count += 1


    # if we finished the game last time, lets go to a random place to start
    if game.is_terminal_state(current_state):
        # current_state = random_state()
        current_state = game.start_state
    else:
        # if we are above the random threshold, take the highest reward action
        if random.random() >= game.epsilon or True:
            # combined = p1_q_values_final[current_state] + p2_q_values_final[current_state]
            # p1_action, p2_action = combined.argmax()

            p1_action, p2_action, best_score = get_max_moves()
            # print('best score', best_score)

        else:
            p1_action = np.random.randint(game.num_actions)
            p2_action = np.random.randint(game.num_actions)

        # take the actions
        # p1 takes his turn
        p1_new_location_tmp, p2_new_location_tmp, p1_reward = game.game_step(current_state, p1_action, 0)
        intermediate_state_prime = (p1_new_location_tmp, p2_new_location_tmp)

        # then p2 takes their turn
        p1_new_location_tmp, p2_new_location_tmp, p2_reward = game.game_step(intermediate_state_prime, p2_action, 1)
        state_prime = (p1_new_location_tmp, p2_new_location_tmp)

        # print('actual score', p1_reward + p2_reward)

        # print(f'{current_state} -> {action_space[p1_action]} -> {intermediate_state_prime}')
        # print(f'{intermediate_state_prime} -> {action_space[p2_action]} -> {state_prime}')
        # print(state_prime)

        # 1. build up the payoff matrix of this state
        # TODO does this need to be intermediate_state_prime and state_prime?
        p1_payoff = p1_q_values_final[state_prime]
        p2_payoff = p2_q_values_final[state_prime]

        # 2. calculate the maxmax value of the two payoff matrices
        maxmax_value = ((p1_payoff + p2_payoff) / 2).max()


        # 3. calculate the minimax value for each player
        # p1_minimax_value = minimax_value((p1_payoff - p2_payoff) / 2)
        p1_minimax_value = minimax_value(state_prime, 8, 0, 0, game)
        p2_minimax_value = -p1_minimax_value

        # 4. calculate the coco value for each player



        current_state = state_prime

