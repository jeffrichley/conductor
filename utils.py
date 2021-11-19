from game import *

def decay_alpha(t, alpha):
    alpha = max(0.001, alpha * 0.999994)
    return alpha

def decay_epsilon(t, epsilon):
    epsilon = min_epsilon + (max_epsilon - min_epsilon) * math.exp(-epsilon_decay * t)
    if epsilon < min_epsilon:
        epsilon = min_epsilon

    return epsilon