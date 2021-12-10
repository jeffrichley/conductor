import math
from prisoner_game import *
from cvxopt import matrix, solvers
from cvxopt.modeling import op
from cvxopt.modeling import variable
from cvxopt.solvers import options
options['show_progress'] = False
solvers.options['show_progress'] = False # disable solver output
solvers.options['glpk'] = {'msg_lev': 'GLP_MSG_OFF'}  # cvxopt 1.1.8
solvers.options['LPX_K_MSGLEV'] = 0  # previous versions


def decay_alpha(t, alpha):
    alpha = max(0.001, alpha * 0.999994)
    return alpha


def decay_epsilon(t, epsilon):
    epsilon = min_epsilon + (max_epsilon - min_epsilon) * math.exp(-epsilon_decay * t)
    if epsilon < min_epsilon:
        epsilon = min_epsilon

    return epsilon


def solve_depricated(player, actions):
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

    if right.value[0] >= left.value[0] and right.value[0] >= stick.value[0]:
        return right.name, 0
    elif left.value[0] >= stick.value[0]:
        return left.name, 1
    else:
        return stick.name, 2


def maximax_depricated(p1_values, p2_values):

    return p1_values.max(), p2_values.max()


def compute_minimax_lp(player, actions):
    v = variable()

    variables = []
    for action in actions:
        action_var = variable(1, action)
        variables.append(action_var)

    constraints = list()

    tmp = 0
    for var in variables:
        tmp += var
    constraints.append((tmp == 1.0))

    for var in variables:
        constraints.append(var >= 0)

    for i in range(len(actions)):
        constraint = 0
        for j in range(len(actions)):
            constraint += float(player[i][j]) * variables[j]
        constraints.append((constraint >= v))

    lp = op(-v, constraints)
    lp.solve()

    return [x.value[0] for x in variables]


def get_coco_value(player1_vals, player2_vals):

    plus = player1_vals + player2_vals
    max_value = (plus / 2).max()

    # TODO: this is using maximin? Need to verify which version this is computing
    # minimax_probability_value = maxmin_value(player1_vals, player2_vals)
    minus = player1_vals - player2_vals
    minimax_probability_value = minimax_value(minus/2)

    coco_value = max_value + minimax_probability_value

    return coco_value

def maxmin(A, solver="glpk"):

    original_A = A.copy()

    # https://adamnovotnycom.medium.com/linear-programming-in-python-cvxopt-and-game-theory-8626a143d428

    num_vars = len(A)
    # minimize matrix c
    c = [-1] + [0 for i in range(num_vars)]
    c = np.array(c, dtype="float")
    c = matrix(c)

    # constraints G*x <= h
    G = np.matrix(A, dtype="float").T # reformat each variable is in a row
    G *= -1 # minimization constraint
    G = np.vstack([G, np.eye(num_vars) * -1]) # > 0 constraint for all vars
    new_col = [1 for i in range(num_vars)] + [0 for i in range(num_vars)]
    G = np.insert(G, 0, new_col, axis=1) # insert utility column
    G = matrix(G)
    h = ([0 for i in range(num_vars)] +
         [0 for i in range(num_vars)])
    h = np.array(h, dtype="float")
    h = matrix(h)

    # contraints Ax = b
    A = [0] + [1 for i in range(num_vars)]
    A = np.matrix(A, dtype="float")
    A = matrix(A)
    b = np.matrix(1, dtype="float")
    b = matrix(b)
    sol = solvers.lp(c=c, G=G, h=h, A=A, b=b, solver=solver)

    # TODO: why does it crash sometimes?  I've noticed there are times when all values are negative.
    # This may cause the LP to become unbounded.
    if sol['x'] is None:
        print(original_A)

    probs = sol['x'][1:]

    return probs

def maxmin_value_depricated(player1_vals, player2_vals, solver="glpk"):
    minus = (player1_vals - player2_vals) / 2
    p1_probs = maxmin(minus)

    p2_probs = maxmin(minus.transpose())

    # following line takes both three dimentional probabilities and multiplies them together to get a 3x3
    # representation of the full join action space probabilities.  It then multiplies those probabilities
    # with the values previously calculated and sums these values for the answer.

    # p1_probs = np.array([0.5, 0.25, 0.25])
    # p2_probs = np.array([0.5, 0.25, 0.25])
    # (np.expand_dims(p1_probs, axis=0) * np.expand_dims(p2_probs, axis=1))
    value = (minus * (np.expand_dims(p1_probs, axis=0) * np.expand_dims(p2_probs, axis=1))).sum()

    return value


def minimax_value(vals):
    # probs = maxmin(x)
    # intermediate = np.multiply(vals, np.array(probs))
    # maxes = intermediate.sum(axis=0)
    # answer = maxes.min()
    # return minimum

    answer = np.multiply(vals, np.array(maxmin(vals))).sum(axis=0).min()

    return answer




# if __name__ == '__main__':

    # p1_probs = np.array([0.5, 0.25, 0.25])
    # p2_probs = np.array([0.5, 0.25, 0.25])
    # answer = (np.expand_dims(p1_probs, axis=0) * np.expand_dims(p2_probs, axis=1))
    # print(answer)

    # x = np.array([[1., 2., 3.],
    #               [2., 3., 1.],
    #               [3., 1., 2.]])
    #
    # print(minimax(x))

    # first = -minimax(x)
    # second = minimax(-x)
    # print(first, second)

