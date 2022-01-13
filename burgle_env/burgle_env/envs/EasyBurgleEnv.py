import gym
from gym.spaces import Box, Discrete

from burgle_env.envs.game.Board import *
from burgle_env.envs.game.Game import EasyGame

class EasyBurgleEnv(gym.Env):

    def __init__(self):

        self.game = EasyGame()

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def step(self, action):
        observation = 1
        reward = 1
        done = False

        return observation, reward, done, {}

    # def _reset(self):
    def reset(self):


        return self._next_observation()

    def render(self, mode='human', close=False):

        pass

    def _next_observation(self):

        pass