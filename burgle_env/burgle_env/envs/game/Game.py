from burgle_env.envs.game.Board import Board
from burgle_env.envs.game.Tiles import *

class Game:

    def __init__(self):
        self._board = Board()


class EasyGame(Game):

    def __init__(self):
        super().__init__()

        for x in range(4):
            for y in range(4):
                self._board.add_tile(0, y, x, BaseTile())