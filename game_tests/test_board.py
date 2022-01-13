from burgle_env.envs.game.Board import *
from burgle_env.envs.game.Tiles import *


def test_adding_tiles():
    board = Board()

    t1 = BaseTile()
    t2 = BaseTile()
    t3 = BaseTile()
    t4 = BaseTile()
    t5 = BaseTile()

    board.add_tile(1, 2, 2, t1)

    board.add_tile(1, 1, 2, t2)
    assert(t2 is t1.north_tile)
    assert(t1 is t2.south_tile)

    board.add_tile(1, 3, 2, t3)
    assert(t3 is t1.south_tile)
    assert(t1 is t3.north_tile)

    board.add_tile(1, 2, 3, t4)
    assert(t4 is t1.east_tile)
    assert(t1 is t4.west_tile)

    board.add_tile(1, 2, 1, t5)
    assert(t5 is t1.west_tile)
    assert(t1 is t5.east_tile)


def test_adding_walls():

    board = Board()

    t1 = BaseTile()
    t2 = BaseTile()
    t3 = BaseTile()
    t4 = BaseTile()
    t5 = BaseTile()

    board.add_tile(1, 2, 2, t1)
    board.add_tile(1, 1, 2, t2)
    board.add_tile(1, 3, 2, t3)
    board.add_tile(1, 2, 3, t4)
    board.add_tile(1, 2, 1, t5)

    assert (not t1.north_wall)
    assert (not t2.south_wall)
    board.add_wall(1, 2, 2, 1, 2)
    assert t1.north_wall
    assert t2.south_wall

    assert (not t1.south_wall)
    assert (not t3.north_wall)
    board.add_wall(1, 2, 2, 3, 2)
    assert t1.south_wall
    assert t3.north_wall

    assert (not t1.east_wall)
    assert (not t4.west_wall)
    board.add_wall(1, 2, 2, 2, 3)
    assert t1.east_wall
    assert t4.west_wall

    assert (not t1.west_wall)
    assert (not t5.east_wall)
    board.add_wall(1, 2, 2, 2, 1)
    assert t1.west_wall
    assert t5.east_wall



