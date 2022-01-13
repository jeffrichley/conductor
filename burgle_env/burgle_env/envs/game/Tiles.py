

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
