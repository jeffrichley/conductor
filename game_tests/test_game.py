from burgle_env.envs.game.Game import *


def test_set_player_locations():

    game = Game()

    # make sure they start off the board
    assert(game.players[0] == (-1, -1))

    game.set_player_location(0, (1, 1))

    # make sure the player was moved
    assert (game.players[0] == (1, 1))
