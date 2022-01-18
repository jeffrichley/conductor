import random
from queue import PriorityQueue
from collections import deque
from copy import copy

class Guard():

    def __init__(self, floor, num_players, game):

        self.game = game
        self.board = self.game.get_board()

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

        # make sure we don't go back to where we are
        # floor, y, x = self.location
        # self.current_move_counts[y][x] = 1000000
        #
        # # look for the smallest value going in a clockwise rotation
        # next_direction = (0, 0)
        # current_tile = self.board.get_tile(floor, y, x)
        # current_best = 9999
        #
        # # north
        # if current_tile.north_tile is not None and not current_tile.north_wall:
        #     current_best = self.current_move_counts[y-1][x]
        #     next_direction = (-1, 0)
        #
        # # east
        # if current_tile.east_tile is not None and not current_tile.east_wall:
        #     if self.current_move_counts[y][x+1] < current_best:
        #         current_best = self.current_move_counts[y][x+1]
        #         next_direction = (0, 1)
        #
        # # south
        # if current_tile.south_tile is not None and not current_tile.south_wall:
        #     if self.current_move_counts[y+1][x] < current_best:
        #         current_best = self.current_move_counts[y+1][x]
        #         next_direction = (1, 0)
        #
        # # west
        # if current_tile.west_tile is not None and not current_tile.west_wall:
        #     if self.current_move_counts[y][x-1] < current_best:
        #         current_best = self.current_move_counts[y][x-1]
        #         next_direction = (0, -1)
        #
        # self.location = (floor, y + next_direction[0], x + next_direction[1])

        prev_location = self.location
        self.location = self.current_path.pop()
        # print(prev_location, self.location, self.destination)


        if self.location == self.destination:
            self.new_destination()

    def new_destination(self):
        if len(self.patrol_deck) == 0:
            self.reset_patrol_deck()

        self.destination = self.patrol_deck.pop()

        # just in case we pulled the destination for where we are
        if self.destination == self.location:
            self.new_destination()

        self.calculate_path()
        # print(len(self.patrol_deck))

    def calculate_path(self):
        # self.current_move_counts = [[None for i in range(4)] for j in range(4)]

        # start_tile = self.board.get_tile(self.location[0], self.location[1], self.location[2])

        self.current_path = None

        q = PriorityQueue()
        visited = [self.location]

        # step count, location, path to take
        q.put((0, self.location, []))
        _, y, x = self.location
        # self.current_move_counts[y][x] = 0

        while not q.empty() and self.current_path == None:
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

                    if child_tile.location == self.destination:
                        self.current_path = deque(child_path)

        # print(self.current_path)



