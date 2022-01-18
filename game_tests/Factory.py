from burgle_env.envs.game.Tiles import *


def configure_easy_board(board):

    # create the walls
    for x in range(4):
        for y in range(4):
            if y == 0 and x == 3:
                tile = Vault()
            elif y == 3 and x == 0:
                tile = Stairs('up')
            else:
                tile = BaseTile()

            tile.showing = True
            board.add_tile(0, y, x, tile)

    # verticle walls
    board.add_wall(0, 0, 0, 0, 1)
    board.add_wall(0, 0, 1, 0, 2)
    board.add_wall(0, 1, 0, 1, 1)
    board.add_wall(0, 1, 2, 1, 3)
    board.add_wall(0, 2, 1, 2, 2)

    # horizontal walls
    board.add_wall(0, 0, 3, 1, 3)
    board.add_wall(0, 2, 1, 3, 1)
    board.add_wall(0, 2, 3, 3, 3)
