import random

from turn_util import *
import numpy as np
from numpy import unravel_index
import itertools
from tqdm import tqdm

from turn_turkey_game import *
from turn_prisoner_game import *


def update_rewards(one_reward, two_reward, one_player_action, two_player_action):
    if one_reward == 0 and one_player_action != 2:
        one_reward = -1
    # # if p1_action != 2:
    # #     p1_reward += -1

    if two_reward == 0 and two_player_action != 2:
        two_reward = -1

    return one_reward, two_reward


def train(game, play_game=True):
    # game = TurnTurkey()
    # game = TurnPrisoner()


    # This is where we will keep our COCO-Q values for learning
    p1_q_values = np.zeros((game.num_spaces, game.num_spaces, game.num_actions), dtype=np.float64)
    p2_q_values = np.zeros((game.num_spaces, game.num_spaces, game.num_actions), dtype=np.float64)

    player_policies = [p1_q_values, p2_q_values]
    turn_count = 0

    current_state = game.start_state

    # main loop for training
    # while count < game.num_sessions:
    for _ in tqdm(range(game.num_sessions), mininterval=2):

        # if we finished the game last time, lets go to a random place to start
        if game.is_terminal_state(current_state):
            # go back to the start
            current_state = (3, 5)

            # set Player 1 to be the first player
            turn_count = 0
        else:


            # get the player's sorted out, is it Player 1 or Player 2's turn?
            # current_player_num = turn_count % 2
            # next_player_num = (turn_count + 1) % 2
            current_player_num = 0
            next_player_num = 1

            maximizing_player_q = player_policies[current_player_num]
            minimizing_player_q = player_policies[next_player_num]

            # 1. determine what action we will be taking

            # if we are above the random threshold, take the highest reward action
            if random.random() >= game.epsilon:
                maximizing_player_action, minimizing_player_action = get_best_actions(maximizing_player_q, minimizing_player_q, current_state, game, player_num=current_player_num)
            else:
                maximizing_player_action, minimizing_player_action = np.random.randint(game.num_actions, size=2)


            # if current_state == (1, 7):
            #     maximizing_player_action = 1
            #     minimizing_player_action = 0
            # elif current_state == (2, 6):
            #     maximizing_player_action = 1
            #     minimizing_player_action = 0
            #
            # maximizing_player_action = 1
            # minimizing_player_action = 0


            # 2. take the actions
            p1_new_location, p2_new_location, maximizing_reward = game.game_step(state=current_state, action=maximizing_player_action, player=current_player_num)
            next_state = (p1_new_location, p2_new_location)

            p1_new_location, p2_new_location, minimizing_reward = game.game_step(state=next_state, action=minimizing_player_action, player=next_player_num)
            state_prime = (p1_new_location, p2_new_location)

            maximizing_reward, minimizing_reward = update_rewards(maximizing_reward, minimizing_reward, maximizing_player_action, minimizing_player_action)


            if game.is_terminal_state(state_prime):
                state_prime_prime = state_prime
            else:
                next_maximizing_player_action, _ = get_best_actions(maximizing_player_q, minimizing_player_q, state_prime, game, player_num=current_player_num)
                p1_new_location, p2_new_location, maximizing_reward = game.game_step(state=state_prime, action=maximizing_player_action, player=current_player_num)
                state_prime_prime = (p1_new_location, p2_new_location)





            # 3. build up the payoff matrix of this state
            # maximizing_player_payoff_matrix = maximizing_player_q[current_state]
            # minimizing_player_payoff_matrix = minimizing_player_q[next_state]
            maximizing_player_payoff_matrix = maximizing_player_q[state_prime]
            minimizing_player_payoff_matrix = minimizing_player_q[state_prime_prime]

            # 4. calculate the maxmax value of the two payoff matrices
            # maxmax_value = ((maximizing_player_payoff_matrix + minimizing_player_payoff_matrix) / 2).max()

            # the players are no longer tied to playing at the same time so we can take the individual maxes
            maxmax_value = (maximizing_player_payoff_matrix.max() + minimizing_player_payoff_matrix.max()) / 2

            # 5. calculate the minimax value for each player
            # maximizing_player_minimax_value = turn_based_minimax(maximizing_player_q, minimizing_player_q, current_state, game, player_num=current_player_num) / 2
            maximizing_player_minimax_value = turn_based_minimax(maximizing_player_q, minimizing_player_q, state_prime, game, player_num=current_player_num) / 2
            minimizing_player_minimax_value = -maximizing_player_minimax_value
            # minimizing_player_minimax_value = turn_based_minimax(minimizing_player_q, maximizing_player_q, state_prime_prime, game, player_num=next_player_num) / 2

            # 6. calculate the coco value for the current player
            maximizing_player_coco_value = maxmax_value + maximizing_player_minimax_value
            minimizing_player_coco_value = maxmax_value + minimizing_player_minimax_value

            # 7. perform the Q-Learning update
            # gather up the values for the update
            maximizing_q_s_a = maximizing_player_q[current_state][maximizing_player_action]
            maximizing_player_q[current_state][maximizing_player_action] = maximizing_q_s_a + game.alpha * (maximizing_reward + game.gamma * maximizing_player_coco_value - maximizing_q_s_a)

            minimizing_q_s_a = minimizing_player_q[next_state][minimizing_player_action]
            minimizing_player_q[next_state][minimizing_player_action] = minimizing_q_s_a + game.alpha * (minimizing_reward + game.gamma * minimizing_player_coco_value - minimizing_q_s_a)

            # current_state = next_state
            current_state = state_prime
            turn_count += 1

            # perform decays
            epsilon = max(0.05, game.epsilon * game.epsilon_decay)
            alpha = max(0.001, game.alpha * game.alpha_decay)



    if play_game:
        current_state = game.start_state
        move_count = 0

        # current_state = (1, 7)

        print(p1_q_values.max())
        print(p2_q_values.max())

        while not game.is_terminal_state(current_state) and move_count < 6:

            move_count += 1

            p1_action, p2_action = get_best_actions(p1_q_values, p2_q_values, current_state, game, 0)
            p1_new_location, p2_new_location, p1_reward = game.game_step(state=current_state,
                                                                                 action=p1_action,
                                                                                 player=0)
            next_state = (p1_new_location, p2_new_location)

            print(f'P1: {current_state} -> {game.action_space[p1_action]} -> {next_state}')

            # p2_action = get_best_actions(p2_q_values, p1_q_values, next_state, game, 1)
            p1_new_location, p2_new_location, p2_reward = game.game_step(state=next_state,
                                                                         action=p2_action,
                                                                         player=1)

            current_state = (p1_new_location, p2_new_location)

            print(f'P2: {next_state} -> {game.action_space[p2_action]} -> {current_state}')

    return p1_q_values, p2_q_values


if __name__ == '__main__':
    # game = TurnTurkey()
    game = TurnPrisoner()

    p1_vals = []
    p2_vals = []

    for i in range(100):
        p1_q_values, p2_q_values = train(game, play_game=False)
        p1_vals.append(p1_q_values.max())
        p2_vals.append(p2_q_values.max())

        print(f'\n {i+1} {sum(p1_vals) / len(p1_vals)} {sum(p2_vals) / len(p2_vals)}')
        print(f'{unravel_index(p1_q_values.argmax(), p1_q_values.shape)} {unravel_index(p2_q_values.argmax(), p2_q_values.shape)}')