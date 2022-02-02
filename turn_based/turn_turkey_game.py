import random
import numpy as np

class TurnTurkey:

    def __init__(self):

        self.start_state = (9, 11)
        self.action_space = ['right', 'left', 'stick', 'up', 'down']

        self.num_actions = len(self.action_space)
        self.num_spaces = 12

        self.num_sessions = 1000000
        self.num_plays = 500

        self.alpha = 0.6
        self.alpha_decay = 0.99995
        self.gamma = 0.99
        self.epsilon_decay = 0.99999
        self.min_epsilon = 0.05
        self.max_epsilon = 0.99
        self.epsilon = 0.99

        self.semi_wall_probability = 0.5


    def is_terminal_state(self, state):
        return state[0] == 0 or state[0] == 4 or state[1] == 4 or state[1] == 2


    def get_next_location(self, current_location, action):

        new_location = current_location

        if (current_location == 2 or current_location == 5 or current_location == 8 or current_location == 11) and (action == 0):
            new_location = current_location
        elif (current_location == 0 or current_location == 3 or current_location == 6 or current_location == 9) and (action == 1):
            new_location = current_location
        elif (current_location == 0 or current_location == 1 or current_location == 2) and (action == 3):
            new_location = current_location
        elif (current_location == 9 or current_location == 10 or current_location == 11) and (action == 4):
            new_location = current_location
        elif (current_location == 9 or current_location == 11) and action == 3:
            if random.random() > self.semi_wall_probability:
                new_location = current_location - 3
            else:
                new_location = current_location
        elif (current_location == 6 or current_location == 8) and action == 4:
            if random.random() > self.semi_wall_probability:
                new_location = current_location + 3
            else:
                new_location = current_location
        elif action == 0:
            new_location = current_location + 1
        elif action == 1:
            new_location = current_location - 1
        elif action == 3:
            new_location = current_location - 3
        elif action == 4:
            new_location = current_location + 3

        return new_location


    # def game_step(state, p1_action, p2_action):
    def game_step(self, state, action, player):
        p1_location, p2_location = state
        p1_new_location, p2_new_location = state

        if player == 0:
            p1_new_location = self.get_next_location(p1_location, action)
        elif player == 1:
            p2_new_location = self.get_next_location(p2_location, action)

        # if p1_new_location == p2_new_location:
        #     if p1_action == 2:
        #         p2_new_location = p2_location
        #     elif p2_action == 2:
        #         p1_new_location = p1_location
        #     else:
        #         player_move = np.random.randint(2)
        #         if player_move == 0:
        #             p2_new_location = p2_location
        #         else:
        #             p1_new_location = p1_location

        if p1_new_location == p2_new_location:
            if player == 0:
                p1_new_location = p1_location
            elif player == 1:
                p2_new_location = p2_location

        p1_reward, p2_reward = self.get_rewards((p1_new_location, p2_new_location))
        reward = 0
        if player == 0:
            reward = p1_reward
        elif player == 1:
            reward = p2_reward

        return p1_new_location, p2_new_location, float(reward)


    def get_rewards(self, state):
        p1_reward = 0
        p2_reward = 0

        p1, p2 = state

        if p1 == 0 or p1 == 4:
            p1_reward = 100

        if p2 == 4 or p2 == 2:
            p2_reward = 100

        return p1_reward, p2_reward
