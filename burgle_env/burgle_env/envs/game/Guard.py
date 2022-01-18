import random
from queue import PriorityQueue
from collections import deque
from copy import copy

class Guard():

    all_paths = None

    def __init__(self, floor, num_players, game):

        self.game = game
        self.board = self.game.get_board()

        if Guard.all_paths is None:
            self.calculate_all_paths()

        # resetting the patrol deck will bump this up by one
        self.num_patrol_moves = floor + 1
        self.floor_num = floor

        self.patrol_cards = [(floor, y, x) for y in range(4) for x in range(4)]
        random.shuffle(self.patrol_cards)

        if num_players == 1:
            num_discard = 9
        elif num_players == 2:
            num_discard = 6
        else:
            num_discard = 3

        # we need to remove a certain number of cards depending on the number of players
        self.patrol_cards = self.patrol_cards[:(16-num_discard)]
        self.patrol_deck = None
        self.reset_patrol_deck()

        # where does the guard start?
        self.location = self.patrol_deck.pop()
        self.destination = self.patrol_deck.pop()
        # self.current_move_counts = None
        self.current_path = None
        self.path = self.calculate_path()

    def reset_patrol_deck(self):
        random.shuffle(self.patrol_cards)
        self.patrol_deck = deque(self.patrol_cards)
        self.num_patrol_moves += 1

    def move(self):

        prev_location = self.location

        if len(self.current_path) == 0:
            self.new_destination()

        self.location = self.current_path.pop()

        if self.location == self.destination:
            self.new_destination()

    def new_destination(self):
        if len(self.patrol_deck) == 0:
            self.reset_patrol_deck()

        self.destination = self.patrol_deck.pop()

        # just in case we pulled the destination for where we are
        if self.destination == self.location:
            self.new_destination()
        else:
            self.calculate_path()
        # print(len(self.patrol_deck))

    def calculate_path(self):
        self.current_path = copy(Guard.all_paths[(self.location, self.destination)])

    def calculate_all_paths(self):
        Guard.all_paths = {}

        for floor in range(self.game.num_floors):
            for current_y in range(4):
                for current_x in range(4):
                    location = (floor, current_y, current_x)

                    for destination_y in range(4):
                        for destination_x in range(4):
                            destination = (floor, destination_y, destination_x)

                            # run a basic A* following the clockwise rule of movement

                            current_path = None

                            q = PriorityQueue()
                            visited = [location]

                            # step count, location, path to take
                            q.put((0, location, []))
                            _, y, x = location

                            if location == destination:
                                current_path = deque([])

                            while not q.empty() and current_path == None:
                                value, parent_location, parent_path = q.get()
                                parent_tile = self.board.get_tile(parent_location[0], parent_location[1], parent_location[2])

                                new_value = value + 1

                                for child_tile, wall in [(parent_tile.north_tile, parent_tile.north_wall), (parent_tile.east_tile, parent_tile.east_wall), (parent_tile.south_tile, parent_tile.south_wall), (parent_tile.west_tile, parent_tile.west_wall)]:
                                    # child_tile = getattr(parent_tile, direction)
                                    if child_tile is not None and child_tile.location not in visited and not wall:
                                        child_path = copy(parent_path)
                                        child_path.append(child_tile.location)
                                        q.put((new_value, child_tile.location, child_path))
                                        visited.append(child_tile.location)

                                        # _, y, x = child_tile.location
                                        # self.current_move_counts[y][x] = new_value

                                        if child_tile.location == destination:
                                            current_path = deque(child_path)

                            Guard.all_paths[(location, destination)] = current_path




