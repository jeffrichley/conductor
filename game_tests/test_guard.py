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

    attempt = 0
    moved = False
    while attempt < 50 and not moved:
        guard.move()
        moved = guard.location != guard_initial_location

    assert moved


def test_guard_getting_faster():

    game = EasyGame()

    guard = Guard(floor=0, num_players=1, game=game)
    assert (guard.num_patrol_moves == 2)

    attempt = 0
    increased = False
    while attempt < 1000 and not increased:
        guard.move()
        increased = guard.num_patrol_moves > 2

    assert increased


def test_catching_player():

    game = EasyGame(use_guard=True)
    guard = game.guard

    next_patrol_step = guard.current_path[0]

    game.players[0].location = next_patrol_step

    assert game.players[0].num_stealth_tokens == 3

    guard.move()

    assert game.players[0].num_stealth_tokens == 2

