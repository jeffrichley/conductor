import numpy as np
from numpy import unravel_index


def get_move_for_player(the_state, p1_values, p2_values, player_num):
    combined = p1_values[the_state] + p2_values[the_state]
    p1_action, p2_action = unravel_index(combined.argmax(), combined.shape)

    if player_num == 0:
        action = p1_action
    else:
        action = p2_action

    return action


def minimax_value(state, depth, maximizing_player, player_num, game):

    next_player_num = player_num + 1
    if next_player_num > 1:
        next_player_num = 0

    if depth == 0:
        # TODO: should return some sort of heuristic, not sure what this should be but 0 will probably be
        # TODO: good because there will be other states that are more negative or positive
        return 0

    elif game.is_terminal_state(state):
        reward1, reward2 = game.get_rewards(state)
        # if player_num == 0:
        #     return reward1
        # else:
        #     return reward2
        return reward1

    elif maximizing_player:
        value = -999999

        # check each action
        for action in range(len(game.action_space)):
            p1_new_location, p2_new_location, reward = game.game_step(state, action, player_num)
            next_state = (p1_new_location, p2_new_location)

            if game.is_terminal_state(next_state):
                reward1, reward2 = game.get_rewards(next_state)
                # if player_num == 0:
                #     value = reward1
                # else:
                #     value = reward2
                value = reward1
            else:
                value = max(value, minimax_value(state=next_state, depth=depth-1, maximizing_player=False, player_num=next_player_num, game=game))

        return value

    elif not maximizing_player:

        value = 999999

        # check each action
        for action in range(len(game.action_space)):
            p1_new_location, p2_new_location, reward = game.game_step(state, action, player_num)
            next_state = (p1_new_location, p2_new_location)

            if game.is_terminal_state(next_state):
                reward1, reward2 = game.get_rewards(next_state)
                # if player_num == 0:
                #     value = reward1
                # else:
                #     value = reward2
                value = reward1
            else:

                value = min(value, minimax_value(state=next_state, depth=depth-1, maximizing_player=True, player_num=next_player_num, game=game))

        return value

    raise Exception('Found something that went wrong, should have already been handled')

