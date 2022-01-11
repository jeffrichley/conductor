import numpy as np
from utils import *
from prisoner_game import *
from numpy import unravel_index

values = np.array( [[ 99.,      99.,     100.    ],
 [192.04,    99.,     194.03  ],
 [194.03,   100.,     192.0897]])

counts = {}

for _ in range(1000000):
    action = unravel_index(values.argmax(), values.shape)

    if action in counts:
        counts[action] = counts[action] + 1
    else:
        counts[action] = 1

print(counts)
