from burgle_env.envs.game.Game import *


def test_set_player_locations():

    game = Game()

    # make sure they start off the board
    assert(game.players[0] == (-1, -1))

    game.set_player_location(0, (1, 1))

    # make sure the player was moved
    assert (game.players[0] == (1, 1))


def test_player_can_move():

    game = EasyGame()

    # move north
    game.set_player_location(0, (0, 2, 1))
    game.move_player(0, 0)
    assert(game.players[0] == (0, 1, 1))

    # move east
    game.set_player_location(0, (0, 2, 0))
    game.move_player(0, 1)
    assert (game.players[0] == (0, 2, 1))

    # move south
    game.set_player_location(0, (0, 0, 0))
    game.move_player(0, 2)
    assert (game.players[0] == (0, 1, 0))

    # move west
    game.set_player_location(0, (0, 2, 1))
    game.move_player(0, 3)
    assert (game.players[0] == (0, 2, 0))


def test_player_cant_move_through_walls():

    game = EasyGame()

    # move north
    game.set_player_location(0, (0, 3, 1))
    game.move_player(0, 0)
    assert(game.players[0] == (0, 3, 1))

    # move east
    game.set_player_location(0, (0, 0, 0))
    game.move_player(0, 1)
    assert (game.players[0] == (0, 0, 0))

    # move south
    game.set_player_location(0, (0, 2, 1))
    game.move_player(0, 2)
    assert (game.players[0] == (0, 2, 1))

    # move west
    game.set_player_location(0, (0, 0, 1))
    game.move_player(0, 3)
    assert (game.players[0] == (0, 0, 1))


def test_vault_information():

    game = EasyGame()
    vault = game.vault_tile

    # make sure the vault tile is set and in the correct location
    assert(vault.location == (0, 0, 3))

    # make sure some of the safe combinations have been set
    # the first true is because we never roll a 0
    assert(not all(game.vault_combination_cracked))

    # check to make sure the numbers for the vault combination are calculated correctly
    game._board.get_tile(0, 0, 0).vault_number = 1
    game._board.get_tile(0, 0, 1).vault_number = 2
    game._board.get_tile(0, 0, 2).vault_number = 3
    game._board.get_tile(0, 1, 3).vault_number = 4
    game._board.get_tile(0, 2, 3).vault_number = 5
    game._board.get_tile(0, 3, 3).vault_number = 6

    # force an update
    game.set_vault_information()

    assert(game.vault_combination == [1, 2, 3, 4, 5, 6])


def test_crack_safe():
    game = EasyGame()

    original_cracking = game.vault_combination_cracked.copy()

    # we don't have any vault dice, so nothing should change
    # lets try cracking a bunch of times
    for _ in range(100):
        game.take_action(0, 5)

    # make sure something changed
    assert (game.vault_combination_cracked == original_cracking)

    # add the dice
    game.num_vault_dice = 6

    # lets try cracking a bunch of times
    for _ in range(100):
        game.take_action(0, 5)

    # make sure something changed
    assert(game.vault_combination_cracked != original_cracking)


def test_going_up_stairs():

    game = EasyGame()
    game.set_player_location(0, (0, 3, 0))

    # go up the stairs
    game.take_action(0, 6)

    assert(game.players[0] == (1, 3, 0))

    game.set_player_location(0, (0, 0, 0))

    # try going up the stairs even though we aren't on stairs
    game.take_action(0, 6)

    assert (game.players[0] == (0, 0, 0))


def test_drop_dice():

    game = EasyGame()

    assert(game.num_current_player_turns == 0)
    assert(game.num_vault_dice == 0)

    game.take_action(0, 7)
    assert (game.num_current_player_turns == 2)
    assert (game.num_vault_dice == 1)

    game.num_vault_dice = 0
    game.num_current_player_turns = 3
    assert (game.num_current_player_turns == 3)
    assert (game.num_vault_dice == 0)

    game.num_vault_dice = 0
    game.num_current_player_turns = 4
    assert (game.num_current_player_turns == 4)
    assert (game.num_vault_dice == 0)
