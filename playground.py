import numpy as np
from utils import *
from prisoner_game import *

p1_q_values = np.load('p1_policy.npy', allow_pickle=True)
p2_q_values = np.load('p2_policy.npy', allow_pickle=True)

p1_start = 3
p2_start = 5

p1 = p1_q_values[p1_start][p2_start]
p2 = p2_q_values[p1_start][p2_start]

p = p1 + p2

p1_action_coco, p2_action_coco = np.unravel_index(p.argmax(), p.shape)

print(action_space[p1_action_coco], action_space[p2_action_coco])

coco = get_coco_value(p1, p2)
p1_side_payment = coco - p1[p1_action_coco][p2_action_coco]

print(p1)
print(p2)
print(p)

print((p1 + p2).max())
print(((p1 + p2)/2).max() + minimax_value((p1 - p2)/2) + ((p2 + p1)/2).max() + minimax_value((p2 - p1)/2))


p1_total = p1[p1_action_coco][p2_action_coco] + p1_side_payment
p2_total = p2[p1_action_coco][p2_action_coco] - p1_total

print('coco', coco)
print(f'p1 side payment {p1_side_payment} and reward {p1_total}')
print(f'p2 reward {p2_total}')

# print((p1 + coco) + (p2 - coco))

first_p1 = p1
first_p2 = p2

print('--------------')
# p1_q_values = np.load('p1_normal_policy.npy', allow_pickle=True)
# p2_q_values = np.load('p2_normal_policy.npy', allow_pickle=True)
# p1 = p1_q_values[p1_start][p2_start]
# p2 = p2_q_values[p1_start][p2_start]
# p1_coco = get_coco_value(p1, p2)
# p2_coco = get_coco_value(p2, p1)
#
# print(p1)
# print(p2)
#
# print(f'p1 coco {p1_coco}')
# print(f'p2_coco {p2_coco}')
# print(f'p1_coco + p2_coco = {p1_coco + p2_coco}')
# print(f'max max U + Ubar {(p1 + p2).max()}')


# print(p1 + p2)
# print(((p1 + p2)/2).max() + minimax_value((p1 - p2)/2) + ((p2 + p1)/2).max() + minimax_value((p2 - p1)/2))

# print(minimax_value(p1, p2))

print('done')
