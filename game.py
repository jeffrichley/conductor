import numpy as np
import math

# how many iterations to run
num_sessions = 1000000
num_plays = 500

# some basic constants for the learning
# values taken directly from the paper
gamma = 0.9
# alpha = 0.1
alpha = 0.2
min_alpha = 0.001
max_alpha = 0.5
# alpha_decay = 0.00001 : best
# alpha_decay = 0.00001
alpha_decay = 0.00001
# a_decay = (alpha)/(num_sessions)


epsilon = 0.5
min_epsilon = 0.001
max_epsilon = 0.5
# epsilon_decay = 0.000001 : best
# epsilon_decay = 0.00001 : spreading out, went to 400K
epsilon_decay = 0.00008
# epsilon_decay = 0.00001
# e_decay = (epsilon-.001)/(num_sessions-100000)



# stuff about the game



# always start in this state because the paper said so
start_state = (1, 2, 1)

possible_starts = [1,2,5,6]

state_space_tmp = []
for i in [0,1]: # who has the ball
    for j in range(8): # p1's location
        for k in range(8): # p2's location
            if j != k: # we can't have them standing in the same spot
                new_state = [i, j, k]
                state_space_tmp.append(new_state)
state_space = np.array(state_space_tmp)

action_space = ['right', 'left', 'up', 'down', 'stick']

def semi_random_state(e):
    if np.random.rand() < e:
        return start_state
    else:
        return random_state()



def random_state():
    ball = np.random.randint(2)
    p1 = np.random.randint(8)
    p2 = p1
    while p2 == p1:
        p2 = np.random.randint(8)

    return (ball, p1, p2)

def decay_alpha(t, alpha):
    alpha = max(0.001, alpha * 0.999994)
    return alpha

def decay_epsilon(t, epsilon):
    epsilon = min_epsilon + (max_epsilon - min_epsilon) * math.exp(-epsilon_decay * t)
    if epsilon < min_epsilon:
        epsilon = min_epsilon

    return epsilon

# this implementation is embarrassing
def get_next_location(current_location, action):
    next_location = current_location

    if current_location == 0:
        if action == 0:
            next_location = 1
        elif action == 3:
            next_location = 4
    elif current_location == 1:
        if action == 0:
            next_location = 2
        elif action == 1:
            next_location = 0
        elif action == 3:
            next_location = 5
    elif current_location == 2:
        if action == 0:
            next_location = 3
        elif action == 1:
            next_location = 1
        elif action == 3:
            next_location = 6
    elif current_location == 3:
        if action == 1:
            next_location = 2
        elif action == 3:
            next_location = 7
    elif current_location == 4:
        if action == 0:
            next_location = 5
        elif action == 2:
            next_location = 0
    elif current_location == 5:
        if action == 0:
            next_location = 6
        elif action == 1:
            next_location = 4
        elif action == 2:
            next_location = 1
    elif current_location == 6:
        if action == 0:
            next_location = 7
        elif action == 1:
            next_location == 5
        elif action == 2:
            next_location == 2
    elif current_location == 7:
        if action == 1:
            next_location = 6
        elif action == 2:
            next_location = 3

    return next_location


def game_step(state, p1_action, p2_action):
    state_prime = None

    player_with_ball, p1_location, p2_location = state

    p1_new_location = get_next_location(p1_location, p1_action)
    p2_new_location = get_next_location(p2_location, p2_action)

    player_move = np.random.randint(2)

    # todo: need to make sure bumping is working properly
    # first move
    if player_move == 0: # first player
        if p1_new_location == p2_location:
            p1_new_location = p1_location # bumped into other player and stays
    else: # second player
        if p2_new_location == p1_location:
            p2_new_location = p2_location # bumped into other player and stays

    # second move
    if player_move != 0: # first player
        if p1_new_location == p2_new_location:
            p1_new_location = p1_location
            player_with_ball = 1
    else: # second player
        if p2_new_location == p1_new_location:
            p2_new_location = p2_location
            player_with_ball = 0

    if p1_new_location < 0 or p2_new_location < 0:
        print('nope')

    return (player_with_ball, p1_new_location, p2_new_location)

def get_rewards(state):
    p1_reward = 0
    p2_reward = 0

    ball, p1, p2 = state

    if (p1 == 0 or p1 == 4) and ball == 0: # p1 scored for other guy
        p1_reward = -100
        p2_reward = 100
    elif (p2 == 0 or p2 == 4) and ball == 1: # p2 scored for himself
        p1_reward = -100
        p2_reward = 100
    elif (p1 == 3 or p1 == 7) and ball == 0:  # p1 scored for himself
        p1_reward = 100
        p2_reward = -100
    elif (p2 == 3 or p2 == 7) and ball == 1: # p1 scored for himself
        p1_reward = 100
        p2_reward = -100

    return (p1_reward, p2_reward)