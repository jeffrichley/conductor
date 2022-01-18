import numpy as np
from utils import *
from turkey_game import *
from numpy import unravel_index

class A:

    t = None

    @staticmethod
    def fill():
        print('run')
        A.t = 'happy'

    def __init__(self):
        if A.t is None:
            A.fill()

one = A()
two = A()
three = A()

print(one.t)
print(two.t)
print(three.t)
print(A.t)
