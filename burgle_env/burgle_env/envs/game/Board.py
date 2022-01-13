from burgle_env.envs.game.Tiles import *


class Board:

    def __init__(self, num_floors = 1):

        self._tiles = {}

    def set_tile(self, floor, y, x, tile):

        # add the tile to the list of tiles, indexed by its location in the game
        self._tiles[(floor, y, x)] = tile

        # connect this tile with its neighbors
        # north
        if y - 1 >= 0 and (floor, y - 1, x) in self._tiles:
            tile.north = self._tiles[(floor, y - 1, x)]
            self._tiles[(floor, y - 1, x)].sout = tile

        # south
        if y + 1 <= 3 and  (floor, y + 1, x) in self._tiles:
            tile.south = self._tiles[(floor, y + 1, x)]
            self._tiles[(floor, y + 1, x)].north = tile

        # east
        if x + 1 <= 3 and (floor, y, x + 1) in self._tiles:
            tile.east = self._tiles[(floor, y, x + 1)]
            self._tiles[(floor, y, x + 1)].west = tile

        # west
        if x - 1 >= 0 and (floor, y, x - 1) in self._tiles:
            tile.west = self._tiles[(floor, y, x - 1)]
            self._tiles[(floor, y, x - 1)].east = tile

    def get_tile(self, floor, y, x):

        return self._tiles[(floor, y, x)]

