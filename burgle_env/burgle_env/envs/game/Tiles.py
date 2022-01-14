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

    def can_take_action(self, action):

        answer = True

        # check north
        if action == 0:
            answer = not self.north_wall

        # check east
        elif action == 1:
            answer = not self.east_wall

        # check south
        elif action == 2:
            answer = not self.south_wall

        # check west
        elif action == 3:
            answer = not self.west_wall

        # check stick
        elif action == 4:
            answer = True

        return answer

    def get_tile_short_hand(self):
        return '•'


class Vault(BaseTile):

    def __init__(self):
        super().__init__()

    def get_tile_short_hand(self):
        return 'V'


class Stairs(BaseTile):

    def __init__(self, direction):
        super().__init__()

    def get_tile_short_hand(self):
        return 'S'
