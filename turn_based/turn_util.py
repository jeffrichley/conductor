import numpy as np
from numpy import unravel_index

def get_best_actions(max_player_q, min_player_q, state, game, player_num):

    best_score = -9999999
    best_p1_action = -1
    best_p2_action = -1

    # have the first player look at their turns
    for p1_action in range(game.num_actions):
        p1_reward = max_player_q[state][p1_action]
        p1_new_location, p2_new_location, _ = game.game_step(state, p1_action, player_num)
        next_state = (p1_new_location, p2_new_location)

        # look at the best the second player could do in the next state
        p2_action = min_player_q[next_state].argmax()
        p2_reward = min_player_q[next_state][p2_action]

        # now lets see if we found a better reward
        combined = p1_reward + p2_reward
        if combined > best_score:
            best_score = combined
            best_p1_action = p1_action
            best_p2_action = p2_action

    return best_p1_action, best_p2_action


def turn_based_minimax(max_player_q, min_player_q, state, game, player_num):
    best_score = -9999999
    best_p1_action = -1

    # have the first player look at their turns
    for p1_action in range(game.num_actions):
        p1_value = max_player_q[state][p1_action]
        p1_new_location, p2_new_location, _ = game.game_step(state, p1_action, player_num)
        next_state = (p1_new_location, p2_new_location)

        # look at the best the second player could do in the next state
        p2_value = min_player_q[next_state].max()

        # now lets see if we found a better reward
        combined = p1_value - p2_value
        if combined > best_score:
            best_score = combined
            best_p1_action = p1_action

    # return best_p1_action
    return best_score


# def get_move_for_player(the_state, p1_values, p2_values, player_num):
#     combined = p1_values[the_state] + p2_values[the_state]
#     p1_action, p2_action = unravel_index(combined.argmax(), combined.shape)
#
#     if player_num == 0:
#         action = p1_action
#     else:
#         action = p2_action
#
#     return action
#
#
# def minimax_value(state, depth, maximizing_player, player_num, game):
#
#     next_player_num = player_num + 1
#     if next_player_num > 1:
#         next_player_num = 0
#
#     if depth == 0:
#         # TODO: should return some sort of heuristic, not sure what this should be but 0 will probably be
#         # TODO: good because there will be other states that are more negative or positive
#         return 0
#
#     elif game.is_terminal_state(state):
#         reward1, reward2 = game.get_rewards(state)
#         # if player_num == 0:
#         #     return reward1
#         # else:
#         #     return reward2
#         return reward1
#
#     elif maximizing_player:
#         value = -999999
#
#         # check each action
#         for action in range(len(game.action_space)):
#             p1_new_location, p2_new_location, reward = game.game_step(state, action, player_num)
#             next_state = (p1_new_location, p2_new_location)
#
#             if game.is_terminal_state(next_state):
#                 reward1, reward2 = game.get_rewards(next_state)
#                 # if player_num == 0:
#                 #     value = reward1
#                 # else:
#                 #     value = reward2
#                 value = reward1
#             else:
#                 value = max(value, minimax_value(state=next_state, depth=depth-1, maximizing_player=False, player_num=next_player_num, game=game))
#
#         return value
#
#     elif not maximizing_player:
#
#         value = 999999
#
#         # check each action
#         for action in range(len(game.action_space)):
#             p1_new_location, p2_new_location, reward = game.game_step(state, action, player_num)
#             next_state = (p1_new_location, p2_new_location)
#
#             if game.is_terminal_state(next_state):
#                 reward1, reward2 = game.get_rewards(next_state)
#                 # if player_num == 0:
#                 #     value = reward1
#                 # else:
#                 #     value = reward2
#                 value = reward1
#             else:
#
#                 value = min(value, minimax_value(state=next_state, depth=depth-1, maximizing_player=True, player_num=next_player_num, game=game))
#
#         return value
#
#     raise Exception('Found something that went wrong, should have already been handled')

