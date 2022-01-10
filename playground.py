import numpy as np
from utils import *
from prisoner_game import *

p1_q_values = np.load('p1_policy.npy', allow_pickle=True)
p2_q_values = np.load('p2_policy.npy', allow_pickle=True)

p1_start = 3
p2_start = 5

p1 = p1_q_values[p1_start][p2_start]
p2 = p2_q_values[p1_start][p2_start].transpose()

p = p1 + p2




p1_probs = np.array(maxmin(p1))
p1_value = minimax_value(p1)

p2_probs = np.array(maxmin(p2))
p2_value = minimax_value(p2)

print('p1')
print(p1)
print('p1_probs\n', p1_probs)
print('p1_value', p1_value)

print()

print('p2')
print(p2)
print('p2_probs\n', p2_probs)
print('p2_value', p2_value)

print()

plus = p1 + p2_q_values[p1_start][p2_start]
# plus = p1 + p2
plus_probs = np.array(maxmin(plus))
maxes = np.multiply(plus, np.array(maxmin(plus))).sum(axis=0)
print(plus)
print(plus_probs)
print(maxes)

coco = get_coco_value(p1, p2)
print(coco)

# print(np.multiply(plus, np.array(maxmin(plus))))

# print('done')
