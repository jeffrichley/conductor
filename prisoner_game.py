import numpy as np

start_state = (9, 11)
action_space = ['right', 'left', 'stick']
num_actions = len(action_space)

num_sessions = 10000
num_plays = 500

alpha = 0.25
alpha_decay = 0.99995
gamma = 0.99
epsilon_decay = 0.99999
min_epsilon = 0.05
max_epsilon = 0.99
epsilon = 0.99


def random_state():
    p1 = np.random.randint(1, 4)
    p2 = np.random.randint(5, 8)
    return p1, p2


def semi_random_state(e):
    if np.random.rand() < e:
        return start_state
    else:
        return random_state()


def get_next_location(current_location, action):

    new_location = current_location

    if action == 0:
        new_location += 1
    elif action == 1:
        new_location -= 1

    return new_location


def game_step(state, p1_action, p2_action):

    state_prime = None

    p1_location, p2_location = state

    p1_new_location = get_next_location(p1_location, p1_action)
    p2_new_location = get_next_location(p2_location, p2_action)

    player_move = np.random.randint(2)

    # make sure they stay inside the bounds
    if p1_new_location == -1:
        p1_new_location = 0

    if p2_new_location == 9:
        p2_new_location = 8

    # if they moved to the same spot only one can move
    if player_move == 1:  # first player
        if p1_new_location == p2_new_location:
            p1_new_location = p1_location
    elif player_move == 0:  # second player
        if p2_new_location == p1_new_location:
            p2_new_location = p2_location
    else:
        raise Exception('Bad player move')

    # make sure they didn't cross
    if p2_new_location < p1_new_location:
        p1_new_location = p1_location
        p2_new_location = p2_location

    return p1_new_location, p2_new_location


def get_rewards(state):
    p1_reward = 0
    p2_reward = 0

    p1, p2 = state

    if p1 == 0 or p1 == 4:
        p1_reward = 100

    if p2 == 4 or p2 == 8:
        p2_reward = 100

    return p1_reward, p2_reward


def is_terminal_state(state):
    return state[0] == 0 or state[0] == 4 or state[1] == 4 or state[1] == 8



