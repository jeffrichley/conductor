import numpy as np
from utils import *
from prisoner_game import *

p1_q_values = np.load('p1_policy.npy', allow_pickle=True)
p2_q_values = np.load('p2_policy.npy', allow_pickle=True)

state = start_state

while not is_terminal_state(state):
    p1_start = state[0]
    p2_start = state[1]

    p1 = p1_q_values[p1_start][p2_start]
    p2 = p2_q_values[p1_start][p2_start]

    p = p1 + p2

    p1_action_coco, p2_action_coco = np.unravel_index(p.argmax(), p.shape)

    next_state = game_step(state, p1_action_coco, p2_action_coco)

    print(state, action_space[p1_action_coco], action_space[p2_action_coco], next_state)

    state = next_state

