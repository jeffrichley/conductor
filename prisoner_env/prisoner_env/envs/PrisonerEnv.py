import numpy as np

import gym
from gym.spaces import Box, Discrete

from prisoner_env.prisoner_env.envs.prisoner_game import *

class PrisonerEnv(gym.Env):

    def __init__(self, use_guard=False):

        self.state = start_state

    def step(self, action):

        p1_action, p2_action = action

        next_state = game_step(self.state, p1_action, p2_action)

        p1_reward, p2_reward = get_rewards(next_state)

        observation = next_state
        done = is_terminal_state(next_state)
        reward = (p1_reward, p2_reward)

        self.state = next_state

        return observation, reward, done, {}

    def reset(self):

        self.state = start_state

        return self.next_observation()

    def render(self, mode='human', close=False):

        return str(self.state)

