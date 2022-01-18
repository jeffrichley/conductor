import gym
from tqdm import tqdm

import numpy as np
import random
from collections import deque

# moving_average = deque(maxlen=500)


alpha = 0.25
alpha_decay = 0.99995
gamma = 0.99
# epsilon_decay = 0.99999
epsilon_decay = 0.99999
min_epsilon = 0.05
max_epsilon = 0.99
# epsilon = 0.99
epsilon = 0.99999

env_name = 'burgle_env:Burgle-v0'
env = gym.make(env_name)

action_space = env.action_space

# tile y, tile x, vault cracked T/F, # vault dice, turn number, action
q_values = np.zeros((4, 4, 2, 7, 5, 8))

current_state = env.reset()
# all_scores = np.array([])

games_played = 0
score = 0

done = False

# play a bunch of games
# while games_played < 1000000:
# while games_played < 1000000 and (len(moving_average) == 0 or (sum(moving_average) / len(moving_average) < 91 and min(moving_average))) < 85:

num_turns_to_train = 1000000000
# num_turns_to_train = 10000000
for t in tqdm(range(num_turns_to_train), mininterval=5):

    # if we finished the game last time, lets go to a random place to start
    if done:
        games_played += 1
        current_state = env.reset()
        done = False

        # moving_average.append(score)
        # all_scores = np.append(all_scores, score)

        score = 0

        # if games_played % 5000 == 0 and games_played > 0:
        #     print(games_played, min(moving_average), sum(moving_average) / len(moving_average))

    else:
        # if we are above the random threshold, take the highest reward action
        if random.random() >= epsilon:
            action = q_values[current_state[0]][current_state[1]][current_state[2]][current_state[3]][current_state[4]].argmax()
        else:
            action = action_space.sample()

        next_state, reward, done, _ = env.step(action)

        score += reward

        # print(f'{current_state} -> {env.game.action_space[action]} -> {next_state}')

        # gather up the values for the update
        q_s_a = q_values[current_state[0]][current_state[1]][current_state[2]][current_state[3]][current_state[4]][action]
        next_q = q_values[next_state[0]][next_state[1]][next_state[2]][next_state[3]][next_state[4]].max()

        q_values[current_state[0]][current_state[1]][current_state[2]][current_state[3]][current_state[4]][action] = q_s_a + alpha * (reward + gamma * next_q - q_s_a)

        # epsilon = decay_epsilon(count, 0.99)
        epsilon = max(0.05, epsilon * epsilon_decay)
        alpha = max(0.001, alpha * alpha_decay)

        current_state = next_state

# print(all_scores)
# np.save('burgle_one_player_scores', all_scores, allow_pickle=True)
np.save('burgle_one_player_policy', q_values, allow_pickle=True)

print(f'Trained on {games_played} games')

