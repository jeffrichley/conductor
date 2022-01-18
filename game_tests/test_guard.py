from burgle_env.envs.game.Guard import *
from burgle_env.envs.game.Board import *
from burgle_env.envs.game.Game import *

def test_guard_init():

    game = EasyGame()

    guard = Guard(floor=0, num_players=1, game=game)
    assert (guard.num_patrol_moves == 2)

    # guard = Guard(floor=1, num_players=1, game=game)
    # assert (guard.num_patrol_moves == 3)

    # guard = Guard(floor=2, num_players=1, game=game)
    # assert (guard.num_patrol_moves == 4)

    guard = Guard(floor=0, num_players=1, game=game)
    assert(len(guard.patrol_cards) == 7)

    guard = Guard(floor=0, num_players=2, game=game)
    assert(len(guard.patrol_cards) == 10)

    guard = Guard(floor=0, num_players=3, game=game)
    assert(len(guard.patrol_cards) == 13)

    guard = Guard(floor=0, num_players=4, game=game)
    assert(len(guard.patrol_cards) == 13)

    assert(guard.location is not None)
    assert (guard.destination is not None)


def test_guard_moved():
    game = EasyGame()
    guard = Guard(floor=0, num_players=1, game=game)
    guard_initial_location = guard.location

    guard.move()

    assert(guard.location != guard_initial_location)


def test_guard_getting_faster():

    game = EasyGame()

    guard = Guard(floor=0, num_players=1, game=game)
    assert (guard.num_patrol_moves == 2)

    while len(guard.patrol_deck) > 0:
        guard.move()

    guard.move()

    assert (guard.num_patrol_moves == 3)


