from turn_based.turn_prisoner_game import *
from turn_based.turn_util import *

game = TurnPrisoner()

# current_state = (3, 5)
current_state = (1, 5)

value = minimax_value(current_state, 6, True, 0, game)

print(value)