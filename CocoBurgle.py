import gym


env_name = 'burgle_env:Burgle-v0'
env = gym.make(env_name)

print(env.env.game)