import numpy as np
from cvxopt.modeling import op
from cvxopt.modeling import variable
from cvxopt.solvers import options
options['show_progress'] = False

# chicken
# p1 = np.array([[0., -1.],
#                [1., -5.]])
#
# p2 = np.array([[0., 1.],
#                [-1., -5.]])

# coco-q banana
p1 = np.array([[2., 0.],
               [2., 4.]])
p1_actions = ['reach', 'climb']

p2 = np.array([[0., 0.],
               [0., 0.]])
p2_actions = ['don\'t boost', 'boost']

def solve(player, actions):
    v = variable()
    t = variable(1, actions[0])
    s = variable(1, actions[1])

    constraints = list()

    constraints.append(t + s == 1.0)

    constraints.append(t >= 0)
    constraints.append(s >= 0)

    constraint = float(player[0][0]) * t + float(player[0][1]) * s >= v
    constraints.append(constraint)

    constraint = float(player[1][0]) * t + float(player[1][1]) * s >= v
    constraints.append(constraint)

    lp = op(-v, constraints)
    lp.solve()

    # print(v.value)
    # print(v.value[0])
    # print(s.name, s.value)
    # print(t.name, t.value)
    # print("greater", t.value[0] > s.value[0])
    # print('----------------------------')

    if t.value[0] > s.value[0]:
        return t.name, 0
    else:
        return s.name, 1

def maximax(p1_values, p2_values):

    return p1_values.max(), p2_values.max()


p1_action, p2_index = solve(p1, p1_actions)
p2_action, p1_index = solve(p2, p2_actions)

p1_mini_max_value = p1[p1_index][p2_index]
p2_mini_max_value = p2[p1_index][p2_index]

# print("Player 1 value:", p1[p1_action][p2_action])
# print("Player 2 value:", p2[p1_action][p2_action])
print("Player 1 value:", p1_mini_max_value, p1_action, p1_index)
print("Player 2 value:", p2_mini_max_value, p2_action, p2_index)

p1_maxi_max_value, p2_maxi_max_value = maximax(p1, p2)

print('Player 1 max:', p1_maxi_max_value)
print('Player 2 max:', p2_maxi_max_value)

p1_coco_value = ((p1_maxi_max_value + p2_maxi_max_value) / 2) + ((p1_mini_max_value - p2_mini_max_value) / 2)
p2_coco_value = ((p2_maxi_max_value + p1_maxi_max_value) / 2) + ((p2_mini_max_value - p1_mini_max_value) / 2)

print("Player 1 Coco Value", p1_coco_value)
print("Player 2 Coco Value", p2_coco_value)

print('done')