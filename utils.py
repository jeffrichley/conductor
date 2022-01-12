import math
import itertools
from numpy import unravel_index

from prisoner_game import *
# from turkey_game import *

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
    # epsilon_decay = 0.99997
    min_epsilon = 0.05
    # max_epsilon = 0.99

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


def get_coco_values(player1_vals, player2_vals):

    plus = player1_vals + player2_vals
    max_value = (plus / 2).max()

    # TODO: this is using maximin? Need to verify which version this is computing
    # minimax_probability_value = maxmin_value(player1_vals, player2_vals)
    minus = player1_vals - player2_vals
    minimax_probability_value = minimax_value(minus/2)

    p1_coco_value = max_value + minimax_probability_value
    p2_coco_value = max_value - minimax_probability_value

    return p1_coco_value, p2_coco_value


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
    # first try
    # probs = maxmin(x)
    # intermediate = np.multiply(vals, np.array(probs))
    # maxes = intermediate.sum(axis=0)
    # answer = maxes.min()
    # return minimum

    # second try
    # answer = np.multiply(vals, np.array(maxmin(vals))).sum(axis=0).min()

    # third try
    mm1 = maxmin(vals)
    mm2 = maxmin(-vals.transpose())
    probs = np.outer(mm1, mm2)
    tots = vals * probs
    answer = tots.sum()

    return answer


def get_rewards_for_state_joint_action(current_state, p1_action, p2_action):
    state_prime = game_step(current_state, p1_action, p2_action)
    p1_reward, p2_reward = get_rewards(state_prime)

    # TODO: why is their (1, 5) left left == 198?  Mine is 200.
    # p1_reward -= 1
    # p2_reward -= 1

    # if it is a non-terminal state and they didn't stand still, we deduct a point
    # TODO: not sure if they should end up with 100 or 99 when going into the goal
    if p1_reward == 0 and p1_action != 2:
        p1_reward = -1
    # # if p1_action != 2:
    # #     p1_reward += -1

    if p2_reward == 0 and p2_action != 2:
        p2_reward = -1
    # # if p2_action != 2:
    # #     p2_reward += -1

    return p1_reward, p2_reward


def get_payoff_matrices_for_state(current_state, p1_q_values, p2_q_values):
    # initialize the matrices
    p1_payoff = np.zeros((3, 3))
    p2_payoff = np.zeros((3, 3))

    # get all joint action pairs
    all_joint_action_pairs = list(itertools.product([0, 1, 2], [0, 1, 2]))

    # TODO: I'm not sure if we need to rotate the p2 payoff matrice but I don't think so
    for p1_action, p2_action in all_joint_action_pairs:

        # get the reward we would have received had we taken this action
        if is_terminal_state(current_state):
            q_p1 = 0
            q_p2 = 0
        else:
            p1_reward, p2_reward = get_rewards_for_state_joint_action(current_state, p1_action, p2_action)
            state_prime = game_step(current_state, p1_action, p2_action)
            # p1_reward, p2_reward = get_rewards(state_prime)
            #
            # # if it is a non-terminal state and they didn't stand still, we deduct a point
            # if p1_reward == 0 and p1_action != 2:
            #     p1_reward = -1
            #
            # if p2_reward == 0 and p2_action != 2:
            #     p2_reward = -1

            # get the next state's value
            p1_state_prime_q_value = p1_q_values[state_prime]
            p2_state_prime_q_value = p2_q_values[state_prime]

            # calculate this cells value
            # value = reward + (next state's q value * discount)
            discount = 1.0
            q_p1 = p1_reward + (p1_state_prime_q_value * discount)
            q_p2 = p2_reward + (p2_state_prime_q_value * discount)
            # q_p1 = p1_reward + (p1_state_prime_q_value)
            # q_p2 = p2_reward + (p2_state_prime_q_value)

        # set the payoff matrices' cell values
        p1_payoff[p1_action][p2_action] = q_p1
        p2_payoff[p1_action][p2_action] = q_p2

    return p1_payoff, p2_payoff


def play_game(p1_policy, p2_policy, start_position, max_steps=10):

    step_count = 0

    state = start_position

    print('state     actions       resulting state')
    print(f'start                   {state}')
    while not is_terminal_state(state):

        step_count += 1

        combined = p1_policy[state] + p2_policy[state]
        p1_action, p2_action = unravel_index(combined.argmax(), combined.shape)
        next_state = game_step(state, p1_action, p2_action)

        print(f'\t{state} -> {action_space[p1_action]} {action_space[p2_action]:5} -> {next_state}')

        state = next_state

        if step_count >= max_steps:
            break


if __name__ == '__main__':

    # p1_probs = np.array([0.5, 0.25, 0.25])
    # p2_probs = np.array([0.5, 0.25, 0.25])
    # answer = (np.expand_dims(p1_probs, axis=0) * np.expand_dims(p2_probs, axis=1))
    # print(answer)

    x = np.array([[-1., -1., 4.],
                  [2., 3., 1.],
                  [3., 1., 2.]])

    y = np.array([[3., -1., 4.],
                  [2., -4., 5.],
                  [3., 5., 2.]])

    print(minimax_value(x))
    print(minimax_value(y))

    coco_1 = get_coco_value(x, y)
    coco_2 = get_coco_value(y, x)

    maxmax_1 = ((x + y)/2).max()
    minmax_1 = minimax_value((x - y)/2)
    maxmax_2 = ((y + x)/2).max()
    minmax_2 = minimax_value((y-x)/2)

    maxmax = (x+y).max()
    minmax_diff = minimax_value(x - y)

    print('maxmax_1', maxmax_1)
    print('minmax_1', minmax_1)
    print('coco_1', coco_1)
    print('maxmax_2', maxmax_2)
    print('minmax_2', minmax_2)
    print('coco_2', coco_2)
    print('maxmax', maxmax)

    from math import isclose
    check1 = isclose(maxmax_1 + minmax_1 + maxmax_2 + minmax_2, coco_1 + coco_2) and isclose(maxmax, coco_1 + coco_2)
    print('check 1', check1, maxmax_1 + minmax_1 + maxmax_2 + minmax_2 , coco_1 + coco_2, maxmax)

    check2 = isclose((maxmax_1 + minmax_1) - (maxmax_2 + minmax_2), coco_1 - coco_2) and isclose(coco_1 - coco_2, minmax_diff)
    print('check 2', check2, (maxmax_1 + minmax_1) - (maxmax_2 + minmax_2), coco_1 - coco_2, minmax_diff)

    first = -minimax_value(x)
    second = minimax_value(-x)
    print('check 3', isclose(first, second), first, second)

