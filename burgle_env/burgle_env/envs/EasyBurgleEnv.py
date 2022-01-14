import numpy as np

import gym
from gym.spaces import Box, Discrete

from burgle_env.envs.game.Board import *
from burgle_env.envs.game.Game import EasyGame

class EasyBurgleEnv(gym.Env):

    def __init__(self):

        self.game = EasyGame()

        # how many actions do we have to learn?
        self.action_space = Discrete(8)

        # what the agent sees for observations
        self.observation_space = Box(low=0, high=16, shape=(1, 5), dtype=np.int)

    def step(self, action):

        vault_was_opened = self.game.vault_opened
        # we need to subtract 1 because it is 1 based and will never have 0 be False
        previous_cracked_number = self.game.vault_combination_cracked.count(True) - 1

        # take the action in the game
        self.game.take_action(self.game.current_player, action)

        observation = self.next_observation()
        done = self.game.players_won()

        # we need to subtract 1 because it is 1 based and will never have 0 be False
        current_cracked_number = self.game.vault_combination_cracked.count(True) - 1

        # Rewards
        # 100 for winning
        # -100 for losing
        # 10 for cracking the safe
        # 1 for cracking a number of the safe
        # -1 for any other actions
        all_players_left = True
        for player in self.game.players:
            if player[0] == 0:
                all_players_left = False

        reward = -1
        if self.game.players_won():
            reward = 100
            done = True
        elif all_players_left:
            reward = -100
            done = True
        elif self.game.vault_opened and not vault_was_opened:
            reward = 10
        elif current_cracked_number > previous_cracked_number:
            reward = 1

        # if the current player has taken their 4 turns, go to the next player
        if self.game.num_current_player_turns >= 4:
            self.game.next_players_turn()

        return observation, reward, done, {}

    # def _reset(self):
    def reset(self):
        # TODO: we can make this more efficient than just creating a new game
        self.game = EasyGame()
        return self.next_observation()

    def render(self, mode='human', close=False):

        pass

    def next_observation(self):

        new_observation = np.zeros((5), dtype=np.int)

        # add the player information
        player_location = self.game.players[self.game.current_player]
        new_observation[0] = int(player_location[1])
        new_observation[1] = int(player_location[2])

        # tell if the vault is cracked
        if self.game.vault_opened:
            new_observation[2] = 1
        else:
            new_observation[2] = 0

        # tell how many dice are added to the vault
        new_observation[3] = int(self.game.num_vault_dice)

        # tell what turn the player is on
        new_observation[4] = int(self.game.num_current_player_turns)

        return new_observation