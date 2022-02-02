import numpy as np


class TurnPrisoner():

    def __init__(self):
        self.start_state = (3, 5)
        self.action_space = ['right', 'left', 'stick']

        self.num_actions = len(self.action_space)
        self.num_spaces = 9

        self.num_sessions = 10000
        self.num_plays = 500

        self.alpha = 0.25
        self.alpha_decay = 0.99995
        self.gamma = 0.99
        self.epsilon_decay = 0.99999
        self.min_epsilon = 0.05
        self.max_epsilon = 0.99
        self.epsilon = 0.99


    def random_state(self):
        p1 = np.random.randint(1, 4)
        p2 = np.random.randint(5, 8)
        return p1, p2


    def semi_random_state(self, e):
        if np.random.rand() < e:
            return self.start_state
        else:
            return self.random_state()


    def get_next_location(self, current_location, action):

        new_location = current_location

        if action == 0:
            new_location += 1
        elif action == 1:
            new_location -= 1

        return new_location


    # def game_step(self, state, p1_action, p2_action):
    def game_step(self, state, action, player):

        state_prime = None

        p1_location, p2_location = state
        p1_new_location, p2_new_location = state

        # p1_new_location = self.get_next_location(p1_location, p1_action)
        # p2_new_location = self.get_next_location(p2_location, p2_action)
        if player == 0:
            p1_new_location = self.get_next_location(p1_location, action)
        elif player == 1:
            p2_new_location = self.get_next_location(p2_location, action)

        player_move = np.random.randint(2)

        # make sure they stay inside the bounds
        if p1_new_location == -1:
            p1_new_location = 0

        if p2_new_location == 9:
            p2_new_location = 8

        # if they moved to the same spot only one can move
        if player_move == 1:  # first player
            if p1_new_location == p2_new_location:
                p1_new_location = p1_location
        elif player_move == 0:  # second player
            if p2_new_location == p1_new_location:
                p2_new_location = p2_location
        else:
            raise Exception('Bad player move')

        # make sure they didn't cross
        if p2_new_location < p1_new_location:
            p1_new_location = p1_location
            p2_new_location = p2_location

        # get the reward
        p1_reward, p2_reward = self.get_rewards((p1_new_location, p2_new_location))
        reward = 0
        if player == 0:
            reward = p1_reward
        elif player == 1:
            reward = p2_reward

        return p1_new_location, p2_new_location, reward


    def get_rewards(self, state):
        p1_reward = 0
        p2_reward = 0

        p1, p2 = state

        if p1 == 0 or p1 == 4:
            p1_reward = 100

        if p2 == 4 or p2 == 8:
            p2_reward = 100

        return p1_reward, p2_reward


    def is_terminal_state(self, state):
        return state[0] == 0 or state[0] == 4 or state[1] == 4 or state[1] == 8



