import numpy as np
import gym
from tqdm import tqdm

q_values = np.load('burgle_one_player_policy.npy')

env_name = 'burgle_env:Burgle-v0'
env = gym.make(env_name)


current_state = env.reset()
num_wins = 0
num_played = 0
score_history = []

# for _ in range(10000):
for t in tqdm(range(10000), mininterval=1):
    for x in range(4):
        for y in range(4):

            done = False
            num_turns = 0
            num_played += 1
            score = 0

            env.game.set_player_location(0, (0, y, x))
            current_state = env.next_observation()
            start_state = current_state

            while not done and num_turns < 100:

                num_turns += 1

                action = q_values[current_state[0]][current_state[1]][current_state[2]][current_state[3]][current_state[4]].argmax()

                next_state, reward, done, _ = env.step(action)

                if reward == 100:
                    num_wins += 1

                # if action == 5 or action == 7:
                #     print(f'{current_state} -> {env.game.action_space[action]} -> {next_state}')

                score += reward
                current_state = next_state

            current_state = env.reset()
            done = False
            score_history.append(score)

            # print(f'turns: {num_turns}  score: {score}  start state: {start_state}')

print(f'min score: {min(score_history)}  max score: {max(score_history)}  avg score: {sum(score_history) / len(score_history)}')
print(f'number of wins: {num_wins} ({(num_wins / num_played) * 100}%)')



