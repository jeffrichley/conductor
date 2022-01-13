from burgle_env.envs.game.Tiles import *

def test_tile_inits_vault_number():

    tile = BaseTile()

    # make sure the vault number was assigned
    assert(0 < tile.vault_number <= 6)


