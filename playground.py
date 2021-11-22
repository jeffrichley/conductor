import numpy as np
from cvxopt.modeling import op
from cvxopt.modeling import variable
from cvxopt.solvers import options
options['show_progress'] = False

p1 = np.array([[0., -1.],
               [1., -5.]])

p2 = np.array([[0., 1.],
               [-1., -5.]])

# p1 = [[0., -1.],
#       [1., -5.]]
#
# p2 = [[0., 1.],
#       [-1., -5.]]


def solve(player):
    v = variable()
    t = variable(1, 'turn')
    s = variable(1, 'straight')

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
    print(v.value[0])
    print("straight", s.value)
    print("turn", t.value)
    print("greater", t.value[0] > s.value[0])
    print('----------------------------')

    if t.value[0] > s.value[0]:
        return 0
    else:
        return 1

p1_action = solve(p1)
p2_action = solve(p2)

print("Player 1 value:", p1[p1_action][p2_action])
print("Player 2 value:", p2[p1_action][p2_action])