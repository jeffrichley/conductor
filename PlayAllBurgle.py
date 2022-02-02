import numpy as np
import gym
from tqdm import tqdm

from os import listdir
from os.path import isfile, join

write_game = True

mypath = './tmp_training/'

policy_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for policy_file in policy_files:
    # q_values = np.load('policies/Burgle-v0/30000000_burgle_one_player_policy.npy')
    # q_values = np.load('5000000000_burgle_one_player_guard_policy.npy')

    if not policy_file.endswith('.npy'):
        continue

    # policy_file = '5000000000_burgle_one_player_guard_policy.npy'

    q_values = np.load(join(mypath, policy_file), allow_pickle=True)

    # env_name = 'burgle_env:Burgle-v0'
    env_name = 'burgle_env:BurgleGuard-v0'
    env = gym.make(env_name)


    current_state = env.reset()
    num_wins = 0
    num_played = 0
    score_history = []

    num_rounds = 1000

    if write_game:
        f = open("game_play.txt", "w")

    for t in tqdm(range(num_rounds), mininterval=1):
        for x in range(4):
            for y in range(4):

                done = False
                num_turns = 0
                num_played += 1
                score = 0

                env.game.set_player_location(0, (0, y, x))
                current_state = env.next_observation()
                start_state = current_state

                if write_game:
                    f.write(f'{env.game}\n')

                while not done and num_turns < 100:

                    num_turns += 1

                    # action = q_values[current_state[0]][current_state[1]][current_state[2]][current_state[3]][current_state[4]].argmax()
                    values = q_values
                    for part in current_state:
                        values = values[part]

                    action = values.argmax()

                    next_state, reward, done, _ = env.step(action)

                    if reward == 100:
                        num_wins += 1

                    # if action == 5 or action == 7:
                    #     print(f'{current_state} -> {env.game.action_space[action]} -> {next_state}')

                    if write_game:
                        f.write(f'{current_state} -> {env.game.action_space[action]} -> {next_state}\n')
                        f.write(f'{env.game}\n')


                    score += reward
                    current_state = next_state

                # print(y, x, score)

                current_state = env.reset()
                done = False
                score_history.append(score)

                # print(f'turns: {num_turns}  score: {score}  start state: {start_state}')

                if write_game:
                    f.close()

    print('\n--------------------------------')
    print(policy_file)
    print(f'min score: {min(score_history)}  max score: {max(score_history)}  avg score: {sum(score_history) / len(score_history)}')
    print(f'number of wins: {num_wins} ({(num_wins / num_played) * 100}%)')



