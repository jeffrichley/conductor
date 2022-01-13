from burgle_env.envs.game.Game import *


def test_set_player_locations():

    game = Game()

    # make sure they start off the board
    assert(game.players[0] == (-1, -1))

    game.set_player_location(0, (1, 1))

    # make sure the player was moved
    assert (game.players[0] == (1, 1))


def test_player_can_move():

    game = EasyGame()

    # move north
    game.set_player_location(0, (0, 2, 1))
    game.move_player(0, 0)
    assert(game.players[0] == (0, 1, 1))

    # move east
    game.set_player_location(0, (0, 2, 0))
    game.move_player(0, 1)
    assert (game.players[0] == (0, 2, 1))

    # move south
    game.set_player_location(0, (0, 0, 0))
    game.move_player(0, 2)
    assert (game.players[0] == (0, 1, 0))

    # move west
    game.set_player_location(0, (0, 2, 1))
    game.move_player(0, 3)
    assert (game.players[0] == (0, 2, 0))


def test_player_cant_move_through_walls():

    game = EasyGame()

    # move north
    game.set_player_location(0, (0, 3, 1))
    game.move_player(0, 0)
    assert(game.players[0] == (0, 3, 1))

    # move east
    game.set_player_location(0, (0, 0, 0))
    game.move_player(0, 1)
    assert (game.players[0] == (0, 0, 0))

    # move south
    game.set_player_location(0, (0, 2, 1))
    game.move_player(0, 2)
    assert (game.players[0] == (0, 2, 1))

    # move west
    game.set_player_location(0, (0, 0, 1))
    game.move_player(0, 3)
    assert (game.players[0] == (0, 0, 1))
