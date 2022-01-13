from burgle_env.envs.game.Board import Board
from burgle_env.envs.game.Tiles import *

class Game:

    def __init__(self, num_floors=1, num_players=1):

        self._board = Board()
        self.num_floors = num_floors

        self.num_players = num_players
        self.players = [(-1, -1) for _ in range(num_players)]

    def set_player_location(self, player_num, location):
        self.players[player_num] = location

    def __repr__(self):

        answer = ''

        for floor in range(self.num_floors):
            for y in range(4):
                in_between_line = ''
                for x in range(4):
                    tile = self._board.get_tile(floor, y, x)

                    if (floor, y, x) in self.players:
                        # draw where the player is
                        answer += str(self.players.index((floor, y, x)))
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


# first floor of the office job
class EasyGame(Game):

    def __init__(self, num_players=1):
        super().__init__(1, num_players)

        # create the walls
        for x in range(4):
            for y in range(4):
                if y == 0 and x == 3:
                    tile = Vault()
                elif y == 3 and x == 0:
                    tile = Stairs()
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

        # randomly place the players
        for player_num in range(self.num_players):
            player_location = (0, random.randint(0, 3), random.randint(0, 3))
            self.set_player_location(player_num, player_location)


