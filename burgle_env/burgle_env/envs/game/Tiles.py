import random


class BaseTile:

    def __init__(self):

        # neighboring tiles
        self.north_tile = None
        self.south_tile = None
        self.east_tile = None
        self.west_tile = None

        # neighboring walls
        self.north_wall = False
        self.south_wall = False
        self.east_wall = False
        self.west_wall = False

        # is the tile showing
        self.showing = False

        # where in the game is this tile?
        self.location = None

        # what is this tile's vault combination number
        self.vault_number = random.randint(1, 6)

    def get_tile_short_hand(self):
        return '•'


class Vault(BaseTile):

    def __init__(self):
        super().__init__()

    def get_tile_short_hand(self):
        return 'V'


class Stairs(BaseTile):

    def __init__(self):
        super().__init__()

    def get_tile_short_hand(self):
        return 'S'
