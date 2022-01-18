from burgle_env.envs.game.Board import Board
from burgle_env.envs.game.Player import *
from burgle_env.envs.game.Guard import *
from game_tests.Factory import *

class Game:

    def __init__(self, num_floors=1, num_players=1):

        self.action_space = ['north', 'east', 'south', 'west', 'stick', 'crack safe', 'use stairs', 'drop dice']

        self._board = Board()
        self.num_floors = num_floors

        # player information
        self.num_players = num_players
        self.players = [Player(player_num=num) for num in range(num_players)]

        self.current_player = 0
        self.num_current_player_turns = 0

        # valut information
        self.vault_tile = None
        self.vault_opened = False
        self.vault_combination = []
        self.vault_combination_cracked = []
        self.num_vault_dice = 0

    def set_player_location(self, player_num, location):
        self.players[player_num].move_to(location)

    def take_action(self, player_num, action):

        if self.num_current_player_turns < 4:
            # move the player
            if action <= 4:
                self.move_player(player_num, action)

            # crack the safe
            elif action == 5:
                self.crack_safe(player_num)

            # use the stairs
            elif action == 6:
                # TODO: we need to extend this to check if the tile above or below are stairs going in the correct direction
                player_next_location = list(self.players[player_num].location)
                tile = self._board.get_tile(player_next_location[0], player_next_location[1], player_next_location[2])

                # if we are on the actual stairs, we always go up
                if isinstance(tile, Stairs):
                    self.num_current_player_turns += 1
                    player_next_location[0] += 1

                # TODO: need to add the going down feature

                self.players[player_num].move_to(tuple(player_next_location))

            # drop a die on the safe
            elif action == 7:
                self.drop_dice(player_num)

            # we don't know this action
            else:
                raise Exception(f'Unknown action {action} for player {player_num}')

    def drop_dice(self, player_num):

        if self.num_current_player_turns < 3 and self.num_vault_dice < 6 and self.vault_tile.location == self.players[player_num].location:
            self.num_vault_dice += 1
            self.num_current_player_turns += 2

    def crack_safe(self, player_num):

        # roll the dice if we have any
        if self.num_vault_dice > 0:
            self.num_current_player_turns += 1

            for _ in range(self.num_vault_dice):
                roll = random.randint(1, 6)

                # mark the roll as cracked
                self.vault_combination_cracked[roll] = True

            if all(self.vault_combination_cracked):
                self.vault_opened = True

    def move_player(self, player_num, action):

        next_location = list(self.players[player_num].location)
        current_tile = self._board.get_tile(next_location[0], next_location[1], next_location[2])

        if current_tile.can_take_action(action):
            self.num_current_player_turns += 1

            # moving north
            if action == 0:
                next_location[1] -= 1

            # moving east
            elif action == 1:
                next_location[2] += 1

            # moving south
            elif action == 2:
                next_location[1] += 1

            # moving west
            elif action == 3:
                next_location[2] -= 1

        self.players[player_num].move_to(tuple(next_location))

    def set_vault_information(self):

        self.vault_combination_cracked = [True if x > 0 else True for x in range(7)]

        for direction in ['north_tile', 'south_tile', 'east_tile', 'west_tile']:
            current_tile = getattr(self.vault_tile, direction)
            while current_tile is not None:
                if current_tile.vault_number not in self.vault_combination:
                    self.vault_combination.append(current_tile.vault_number)
                    self.vault_combination_cracked[current_tile.vault_number] = False


                current_tile = getattr(current_tile, direction)

        self.vault_combination.sort()

    def players_won(self):
        return self.vault_opened

    def next_players_turn(self):
        self.num_current_player_turns = 0
        self.current_player += 1

        if self.current_player + 1 > self.num_players:
            self.current_player = 0

    def __repr__(self):

        answer = ''

        player_list = [player.location for player in self.players]

        for floor in range(self.num_floors):
            for y in range(4):
                in_between_line = ''
                for x in range(4):
                    tile = self._board.get_tile(floor, y, x)

                    if (floor, y, x) in player_list:
                        # (floor, y, x) = player.location
                        # draw where the player is
                        guard_location = self.get_guard_print_info()
                        if guard_location is not None and (floor, y, x) == guard_location:
                            answer += '\u2639'
                        else:
                            # answer += str(player.player_num)
                            answer += str(player_list.index((floor, y, x)))
                    if self.get_guard_print_info() is not None and self.get_guard_print_info() == (floor, y, x):
                        # guard_location = self.get_guard_print_info()
                        # if guard_location == (floor, y, x):
                        answer += 'G'
                    else:
                        # draw what type of tile it is
                        answer += tile.get_tile_short_hand()

                    # draw walls
                    if tile.east_wall:
                        answer += '|'
                    else:
                        answer += ' '

                    if tile.south_wall:
                        in_between_line += '- '
                    else:
                        in_between_line += '  '

                if in_between_line != '        ':
                    answer += '\n' + in_between_line + '\n'
                else:
                    answer += '\n'


        return answer

    def get_guard_print_info(self):
        return None

# first floor of the office job
class EasyGame(Game):

    def __init__(self, num_players=1, use_guard=False):
        super().__init__(1, num_players)

        self.use_guard = use_guard

        # create the walls
        for x in range(4):
            for y in range(4):
                if y == 0 and x == 3:
                    tile = Vault()
                    self.vault_tile = tile
                elif y == 3 and x == 0:
                    tile = Stairs('up')
                else:
                    tile = BaseTile()

                tile.showing = True
                self._board.add_tile(0, y, x, tile)

        # verticle walls
        self._board.add_wall(0, 0, 0, 0, 1)
        self._board.add_wall(0, 0, 1, 0, 2)
        self._board.add_wall(0, 1, 0, 1, 1)
        self._board.add_wall(0, 1, 2, 1, 3)
        self._board.add_wall(0, 2, 1, 2, 2)

        # horizontal walls
        self._board.add_wall(0, 0, 3, 1, 3)
        self._board.add_wall(0, 2, 1, 3, 1)
        self._board.add_wall(0, 2, 3, 3, 3)

        # guard information
        if self.use_guard:
            self.guard = Guard(floor=0, num_players=num_players, game=self)

        # randomly place the players
        start_y = random.randint(0, 3)
        start_x = random.randint(0, 3)
        for player_num in range(self.num_players):
            player_location = (0, start_y, start_x)
            self.set_player_location(player_num, player_location)

        self.set_vault_information()

    def move_player(self, player_num, action):
        super().move_player(player_num, action)

        self.move_guard()

    def move_guard(self):
        if self.use_guard:
            self.guard.move()
            # self.guard.location == self.players[0].location

    def get_board(self):
        return self._board

    def players_won(self):
        won = False

        if super().players_won():
            won = True
            for player in self.players:
                if player.location[0] != 1:
                    won = False

        return won

    def get_guard_print_info(self):

        if self.use_guard:
            return self.guard.location
        else:
            return None
