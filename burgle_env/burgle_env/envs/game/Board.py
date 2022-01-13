from burgle_env.envs.game.Tiles import *


class Board:

    def __init__(self, num_floors = 1):

        self._tiles = {}

    def add_tile(self, floor, y, x, tile):

        # add the tile to the list of tiles, indexed by its location in the game
        self._tiles[(floor, y, x)] = tile

        # tell the tile where it lives
        tile.location = (floor, y, x)

        # connect this tile with its neighbors
        # north
        if y - 1 >= 0 and (floor, y - 1, x) in self._tiles:
            tile.north_tile = self._tiles[(floor, y - 1, x)]
            self._tiles[(floor, y - 1, x)].south_tile = tile

        # south
        if y + 1 <= 3 and  (floor, y + 1, x) in self._tiles:
            tile.south_tile = self._tiles[(floor, y + 1, x)]
            self._tiles[(floor, y + 1, x)].north_tile = tile

        # east
        if x + 1 <= 3 and (floor, y, x + 1) in self._tiles:
            tile.east_tile = self._tiles[(floor, y, x + 1)]
            self._tiles[(floor, y, x + 1)].west_tile = tile

        # west
        if x - 1 >= 0 and (floor, y, x - 1) in self._tiles:
            tile.west_tile = self._tiles[(floor, y, x - 1)]
            self._tiles[(floor, y, x - 1)].east_tile = tile

    def get_tile(self, floor, y, x):
        return self._tiles[(floor, y, x)]

    def add_wall(self, floor, y1, x1, y2, x2):

        # north
        if y1 - y2 == 1 and x1 - x2 == 0:
            self._tiles[(floor, y1, x1)].north_wall = True
            self._tiles[(floor, y2, x2)].south_wall = True

        # south
        elif y2 - y1 == 1 and x1 - x2 == 0:
            self._tiles[(floor, y1, x1)].south_wall = True
            self._tiles[(floor, y2, x2)].north_wall = True

        # east
        elif y1 - y2 == 0 and x2 - x1 == 1:
            self._tiles[(floor, y1, x1)].east_wall = True
            self._tiles[(floor, y2, x2)].west_wall = True

        # west
        elif y1 - y2 == 0 and x1 - x2 == 1:
            self._tiles[(floor, y1, x1)].west_wall = True
            self._tiles[(floor, y2, x2)].east_wall = True

