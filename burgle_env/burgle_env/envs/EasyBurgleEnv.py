import numpy as np

import gym
from gym.spaces import Box, Discrete

from burgle_env.envs.game.Board import *
from burgle_env.envs.game.Game import EasyGame
from burgle_env.envs.ScoringObservers import *

class EasyBurgleEnv(gym.Env):

    def __init__(self, use_guard=False):

        self.use_guard = use_guard

        self.game = EasyGame(use_guard=self.use_guard)
        self.scoring = BasicScoringObserver(self.game)

        # how many actions do we have to learn?
        self.action_space = Discrete(8)

        # what the agent sees for observations
        self.observation_space = Box(low=0, high=16, shape=(1, 5), dtype=np.int)

        self.total_turns = 0

    def step(self, action):

        self.scoring.before_action()

        # take the action in the game
        self.game.take_action(self.game.current_player, action)

        observation = self.next_observation()
        # done = self.game.players_won()

        if self.total_turns > 200:
            return observation, -100, True, {}

        reward, done = self.scoring.after_action()

        # if the current player has taken their 4 turns, go to the next player
        if self.game.num_current_player_turns >= 4:
            self.game.next_players_turn()
            self.total_turns += 1

        return observation, reward, done, {}

    def create_game(self):
        return EasyGame(use_guard=self.use_guard)

    # def _reset(self):
    def reset(self):

        # TODO: we can make this more efficient than just creating a new game
        # self.game = EasyGame(use_guard=self.use_guard)
        self.game = self.create_game()
        self.scoring = BasicScoringObserver(self.game)
        self.total_rounds = 0
        self.total_turns = 0

        return self.next_observation()

    def render(self, mode='human', close=False):

        pass

    def next_observation(self):

        new_observation = np.zeros((5), dtype=np.int)

        # add the player information
        player_location = self.game.players[self.game.current_player].location
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


class EasyGuardBurgleEnv(EasyBurgleEnv):

    def __init__(self):
        super().__init__(use_guard=True)

    def next_observation(self):

        new_observation = np.zeros((9), dtype=np.int)

        # add the player information
        player_location = self.game.players[self.game.current_player].location
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

        # tell where the guard is and where they are going
        guard_location = self.game.guard.location
        guard_detination = self.game.guard.destination

        new_observation[5] = guard_location[1]
        new_observation[6] = guard_location[2]
        new_observation[7] = guard_detination[1]
        new_observation[8] = guard_detination[2]

        return new_observation