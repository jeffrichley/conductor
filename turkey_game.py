import random
import numpy as np

start_state = (9, 11)
action_space = ['right', 'left', 'stick', 'up', 'down']
num_actions = len(action_space)

# num_sessions = 1000000
num_sessions = 100000
num_plays = 500

alpha = 0.6
alpha_decay = 0.99995
gamma = 0.99
epsilon_decay = 0.99999
min_epsilon = 0.05
max_epsilon = 0.99
epsilon = 0.99

semi_wall_probability = 0.5


def is_terminal_state(state):
    return state[0] == 0 or state[0] == 4 or state[1] == 4 or state[1] == 2


def get_next_location(current_location, action):

    new_location = current_location

    if (current_location == 2 or current_location == 5 or current_location == 8 or current_location == 11) and (action == 0):
        new_location = current_location
    elif (current_location == 0 or current_location == 3 or current_location == 6 or current_location == 9) and (action == 1):
        new_location = current_location
    elif (current_location == 0 or current_location == 1 or current_location == 2) and (action == 3):
        new_location = current_location
    elif (current_location == 9 or current_location == 10 or current_location == 11) and (action == 4):
        new_location = current_location
    elif (current_location == 9 or current_location == 11) and action == 3:
        if random.random() > semi_wall_probability:
            new_location = current_location - 3
        else:
            new_location = current_location
    elif (current_location == 6 or current_location == 8) and action == 4:
        if random.random() > semi_wall_probability:
            new_location = current_location + 3
        else:
            new_location = current_location
    elif action == 0:
        new_location = current_location + 1
    elif action == 1:
        new_location = current_location - 1
    elif action == 3:
        new_location = current_location - 3
    elif action == 4:
        new_location = current_location + 3

    return new_location


def game_step(state, p1_action, p2_action):
    p1_location, p2_location = state

    p1_new_location = get_next_location(p1_location, p1_action)
    p2_new_location = get_next_location(p2_location, p2_action)

    if p1_new_location == p2_new_location:
        if p1_action == 2:
            p2_new_location = p2_location
        elif p2_action == 2:
            p1_new_location = p1_location
        else:
            player_move = np.random.randint(2)
            if player_move == 0:
                p2_new_location = p2_location
            else:
                p1_new_location = p1_location

    return p1_new_location, p2_new_location


def get_rewards(state):
    p1_reward = 0
    p2_reward = 0

    p1, p2 = state

    if p1 == 0 or p1 == 4:
        p1_reward = 100

    if p2 == 4 or p2 == 2:
        p2_reward = 100

    return p1_reward, p2_reward
