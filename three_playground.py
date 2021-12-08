import numpy as np
from cvxopt.modeling import op
from cvxopt.modeling import variable
from cvxopt.solvers import options
options['show_progress'] = False



def solveabc(player, actions):
    v = variable()
    right = variable(1, actions[0])
    left = variable(1, actions[1])
    stick = variable(1, actions[2])

    constraints = list()

    constraints.append(right + left + stick == 1.0)

    constraints.append(right >= 0)
    constraints.append(left >= 0)
    constraints.append(stick >= 0)

    constraint = float(player[0][0]) * right + float(player[0][1]) * left + float(player[0][2]) * stick >= v
    constraints.append(constraint)

    constraint = float(player[1][0]) * right + float(player[1][1]) * left + float(player[1][2]) * stick >= v
    constraints.append(constraint)

    constraint = float(player[2][0]) * right + float(player[2][1]) * left + float(player[2][2]) * stick >= v
    constraints.append(constraint)

    lp = op(-v, constraints)
    lp.solve()

    # print(v.value)
    # print(v.value[0])
    # print(s.name, s.value)
    # print(t.name, t.value)
    # print("greater", t.value[0] > s.value[0])
    # print('----------------------------')

    if right.value[0] >= left.value[0] and right.value[0] >= stick.value[0]:
        return right.name, 0
    elif left.value[0] >= stick.value[0]:
        return left.name, 1
    else:
        return stick.name, 2

def maximax(p1_values, p2_values):

    return p1_values.max(), p2_values.max()


def compute_minimax_lp(player, actions):
    v = variable()

    # right = variable(1, actions[0])
    # left = variable(1, actions[1])
    # stick = variable(1, actions[2])
    variables = []
    for action in actions:
        action_var = variable(1, action)
        variables.append(action_var)

    constraints = list()

    # constraints.append(right + left + stick == 1.0)
    tmp = 0
    for var in variables:
        tmp += var
    constraints.append((tmp == 1.0))
    # constraints.append(sum(variables) == 1.0)

    # constraints.append(right >= 0)
    # constraints.append(left >= 0)
    # constraints.append(stick >= 0)
    for var in variables:
        constraints.append(var >= 0)

    # # constraint = float(player[0][0]) * right + float(player[0][1]) * left + float(player[0][2]) * stick >= v
    # constraint = float(player[0][0]) * right + float(player[1][0]) * left + float(player[2][0]) * stick >= v
    # constraints.append(constraint)
    #
    # # constraint = float(player[1][0]) * right + float(player[1][1]) * left + float(player[1][2]) * stick >= v
    # constraint = float(player[0][1]) * right + float(player[1][1]) * left + float(player[2][1]) * stick >= v
    # constraints.append(constraint)
    #
    # # constraint = float(player[2][0]) * right + float(player[2][1]) * left + float(player[2][2]) * stick >= v
    # constraint = float(player[0][2]) * right + float(player[1][2]) * left + float(player[2][2]) * stick >= v
    # constraints.append(constraint)
    for i in range(len(actions)):
        constraint = 0
        for j in range(len(actions)):
            # print(j, float(player[j][i]), variables[j])
            # constraint += float(player[j][i]) * variables[j]
            constraint += float(player[i][j]) * variables[j]
        constraints.append((constraint >= v))
        # print(constraint)

    lp = op(-v, constraints)
    lp.solve()

    # print(v.value)
    # print(v.value[0])
    # print(s.name, s.value)
    # print(t.name, t.value)
    # print("greater", t.value[0] > s.value[0])
    # print('----------------------------')

    # return right.value[0], left.value[0], stick.value[0]
    for var in variables:
        print(var.name, var.value[0])
    return [x.value[0] for x in variables]


def compute_minimax(values):
    p2_action = np.argmin(values.max(axis=0))
    p1_action = np.argmax(values[:, p2_action])

    # print('values\n', values)
    # print(f'p1_action {p1_action}')
    # print(f'p2_action {p2_action}')
    # print(f'minimax value {values[p1_action][p2_action]}')
    # print()

    return values[p1_action][p2_action], p1_action, p2_action


def compute_vals(p1, p2):

    print('-------------------')

    print('p1\n', p1)
    print('p2\n', p2)

    plus = p1 + p2
    max_value = (plus / 2).max()

    print('plus\n', plus)
    print('max value', max_value)

    minus = (p1 - p2) / 2
    # min_value, p1_minimax_action, p2_minimax_action = compute_minimax(minus)


    print('minus\n', minus)
    p1_probs = compute_minimax_lp(minus, p1_actions)
    # p2_probs = compute_minimax_lp(minus.transpose(), p2_actions)
    print('p1_probs', p1_probs)
    # print('p2_probs', p2_probs)



    minimax_probability_value = (minus.min(axis=1) * p1_probs).sum()
    print('minimax_probability_value', minimax_probability_value)

    # print('test ***', ((-minus).min(axis=1) * compute_minimax_lp((-minus), p1_actions)).sum())

    # tmp = 0.0
    # for i, prob1 in zip(range(len(p1_actions)), p1_probs):
    #     for j, prob2 in zip(range(len(p2_actions)), p2_probs):
    #         tmp += minus[j][i] * prob1 * prob2
    # print(tmp)




    coco_value = max_value + minimax_probability_value

    print('coco value', coco_value)

    # _, action = solve(minus, p1_actions)
    # pmin = minus[action].max()
    # coco = pmax + pmin

    # tmp_plus = p1 + p2
    # print('plus\n', plus)
    p1_action, p2_action = np.unravel_index(plus.argmax(), plus.shape)
    print('p1 action', p1_action, p1_actions[p1_action])
    print('p2 action', p2_action, p2_actions[p2_action])

    side_payment_p1 = coco_value - p1[p1_action][p2_action]
    # side_payment_p2 = coco_value - p2[p1_action][p2_action]
    # side_payment_p2 = -side_payment_p1

    print('side_payment_p1', side_payment_p1)
    # print('side_payment_p2', side_payment_p2)

    p1_reward = p1[p1_action][p2_action] + side_payment_p1
    p2_reward = p2[p1_action][p2_action] - side_payment_p1

    print('p1_reward', p1_reward)
    print('p2_reward', p2_reward)


    print('done')

    return p1_reward, p2_reward


# test_data = np.array([[1, 2, 3],
#                       [4, 5, 6],
#                       [7, 8, 9]])
# compute_minimax(test_data)

p1_actions = ['right', 'left', 'stick']
p2_actions = ['right', 'left', 'stick']


# coco-q prisoner
p1_value = np.array([[100.,   0., 100.],
                     [  0.,   0.,   0.],
                     [  0.,   0.,   0.]])

p2_value = np.array([[  0., 100.,   0.],
                     [  0., 100.,   0.],
                     [  0., 100.,   0.]])

# compute_vals(p1_value, p2_value)



p1_value = np.array([[  0.,   0.,   0.],
                     [100., 100., 100.],
                     [  0. ,  0.,   0.]])

p2_value = np.array([[100.,   0.,   0.],
                     [100.,   0.,   0.],
                     [100.,   0.,   0.]])

compute_vals(p1_value, p2_value)




# bananas
p1_actions = ['dont boost', 'boost']
p2_actions = ['reach', 'climb']
p1_value = np.array([[0., 0.],
                     [0., 0.]])
p2_value = np.array([[2., 0.],
                     [2., 4.]])
# compute_vals(p1_value, p2_value)