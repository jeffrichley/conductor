from prisoner_game import *
from utils import *


def test_random_state():
    for i in range(100):
        rand_state = random_state()

        # make sure we have only two elements
        assert (len(rand_state) == 2)

        # valid places for player A is 1-3 and player B is 5-7
        assert (1 <= rand_state[0] <= 3)
        assert (5 <= rand_state[1] <= 7)


def test_semi_random_state():
    start_state_count = 0
    other_state_count = 0
    for i in range(100):
        rand_state = semi_random_state(0.5)

        if rand_state == start_state:
            start_state_count += 1
        else:
            other_state_count += 1

    # make sure we got both types of results
    # each should be ~50 so test for only 20
    assert (start_state_count > 20)
    assert (other_state_count > 20)


def test_get_next_location():
    # position 1 and move left is 0
    assert (get_next_location(1, 1) == 0)

    # position 1 and move right is 2
    assert (get_next_location(1, 0) == 2)

    # position 1 and stick is 1
    assert (get_next_location(1, 2) == 1)


def test_game_step_bump():

    state = (3, 5)

    # both are next to the goal trying to get in
    # only one should actually get there
    new_state = game_step(state, 0, 1)

    assert(new_state == (4, 5) or new_state == (3, 4))


def test_game_step_non_goal():

    state = (2, 6)
    new_state = game_step(state, 0, 1)

    assert(new_state == (3, 5))


def test_game_step_outer_goals():

    state = (1, 7)
    new_state = game_step(state, 1, 0)

    assert(new_state == (0, 8))


def test_game_step_out_of_bounds():

    state = (0, 8)
    new_state = game_step(state, 1, 0)

    # make sure they can't go outside the game
    assert(state == new_state)


def test_game_step_crossing():

    state = (1, 2)
    new_state = game_step(state, 0, 1)

    assert(new_state == state)


def test_get_rewards():

    # non-goals get no rewards
    assert(get_rewards((1, 7)) == (0, 0))

    # only one makes it to the center goal
    assert(get_rewards((2, 4)) == (0, 100))
    assert (get_rewards((4, 5)) == (100, 0))

    # both get to the outer goal
    assert(get_rewards((0, 8)) == (100, 100))

    # one gets outer goal one gets inner
    assert(get_rewards((0, 4)) == (100, 100))
    assert (get_rewards((4, 8)) == (100, 100))


def test_one_five_rewards():

    p1, p2 = get_rewards_for_state_joint_action((1, 5), 1, 1)

    assert(p1 == 100)
    assert(p2 == 100)
