import pytest
import pygame
from pygame.locals import *
import olin_man_game
import characters
import constants as const
vec = pygame.math.Vector2

directions = [
    # directions to test if the sprites can detect walls
    # direction, has_wall
    (vec(0, -1), False),  # up
    (vec(0, 1), False),   # down
    (vec(-1, 0), True),   # left
    (vec(1, 0), True)    # right
]

updates = [
    # for checking whether the update function will work
    # grid_pos, direction, can_move
    (vec(1, 4), vec(0, -1), False),
    (vec(1, 4), vec(0, 1), True),
    (vec(1, 4), vec(-1, 0), False),
    (vec(1, 4), vec(1, 0), True),

    (vec(21, 8), vec(0, -1), True),
    (vec(21, 8), vec(0, 1), True),
    (vec(21, 8), vec(-1, 0), True),
    (vec(21, 8), vec(1, 0), True),
]

collide = [
    # for testing if the collision detection works
    # grid_pos, ghost_grid_pos, direction, collided
    (vec(1, 4), vec(1, 6), vec(0, -1), False),
    (vec(1, 4), vec(1, 6), vec(0, 1), True),
    (vec(1, 4), vec(3, 4), vec(1, 0), True),

    (vec(21, 8), vec(21, 6), vec(0, -1), True),
    (vec(21, 8), vec(21, 10), vec(0, 1), True),
    (vec(21, 8), vec(19, 8), vec(-1, 0), True),
    (vec(21, 8), vec(23, 8), vec(1, 0), True),
]

teleports = [
    # for testing if the teleport and reset functions work
    # grid_pos, direction,
    (vec(1, 4), vec(0, -1)),
    (vec(1, 4), vec(0, 1)),
    (vec(1, 4), vec(-1, 0)),
    (vec(1, 4), vec(1, 0)),

    (vec(21, 8), vec(0, -1)),
    (vec(21, 8), vec(0, 1)),
    (vec(21, 8), vec(-1, 0)),
    (vec(21, 8), vec(1, 0)),

    (vec(23, 23), vec(0, -1)),
    (vec(23, 23), vec(0, 1)),
    (vec(23, 23), vec(-1, 0)),
    (vec(23, 23), vec(1, 0)),
]


@pytest.mark.parametrize("direction, bool_check", directions)
def test_can_move(direction, bool_check):
    """
    Test if OlinMan can detect walls properly

    args:
        direction: a (pygame.Vector2) the direction the sprite will move
        bool_check: a (bool) that is (True) if the test should work
    """
    state = olin_man_game.Game_State()
    player = state.olin_man
    player.direction = direction
    assert player.can_move() == bool_check


@pytest.mark.parametrize("pos, direction, bool_check", updates)
def test_player_update(pos, direction, bool_check):
    """
    Test if the update function moves the sprites properly

    args:
        pos: a (pygame.Vector2) the new grid position for the player
        direction: a (pygame.Vector2) the direction the sprite will move
        bool_check: a (bool) that is (True) if the test should work
    """
    state = olin_man_game.Game_State()
    player = state.olin_man
    player.set_speed(const.WINDOW_SCALE)
    player.teleport(pos)
    player.direction = direction
    player.update()
    assert (player.get_last_pos() != player.get_pos()) is bool_check


@pytest.mark.parametrize("pos, direction, bool_check", updates)
def test_get_moves(pos, direction, bool_check):
    """
    Test if the get moves functions can find all the potential movements

    args:
        pos: a (pygame.Vector2) the new grid position for the player
        direction: a (pygame.Vector2) the direction the sprite will move
        bool_check: a (bool) that is (True) if the test should work
    """
    state = olin_man_game.Game_State()
    player = state.olin_man
    player.set_speed(const.WINDOW_SCALE)
    player.teleport(pos)
    moves = player.get_moves()
    assert (direction in moves) is bool_check


@pytest.mark.parametrize("direction, bool_check", directions)
def test_ghost_can_move(direction, bool_check):
    """
    Test if ghosts can detect walls properly

    args:
        direction: a (pygame.Vector2) the direction the sprite will move
        bool_check: a (bool) that is (True) if the test should work
    """
    state = olin_man_game.Game_State()
    player = characters.Ghost(state, vec(3, 4), 2, direction)
    assert player.can_move() == bool_check


@pytest.mark.parametrize("execution_number", range(40))
def test_ghost_corner(execution_number):
    """
    Test if a ghost will not move backwards, and can turn a corner easily

    Movement is randomized somewhat so we run the test many many times

    args:
        execution_number: a (int) to allow the test to run many times
    """
    backwards = False
    state = olin_man_game.Game_State()
    player = characters.Ghost(state, [3, 4], 2)
    player.direction = vec(-1, 0)
    for _ in range(20):
        player.update()
        if player.direction == vec(1, 0):
            backwards = True
            print(f"Direction: {player.direction}")
    assert not backwards


@pytest.mark.parametrize("pos, direction, bool_check", updates)
def test_coins(pos, direction, bool_check):
    """
    Test if OlinMan can eat coins
    Check that the update function does that correctly

    We don't test if this works with coffees, as they function in the same way

    args:
        pos: a (pygame.Vector2) the new grid position for the player
        direction: a (pygame.Vector2) the direction the sprite will move
        bool_check: a (bool) that is (True) if the test should work
    """

    state = olin_man_game.Game_State()
    coins0 = len(state.coins[:])
    player = state.olin_man
    player.direction = vec(0, 0)
    player.set_speed(const.WINDOW_SCALE)
    player.teleport(pos)
    player.update()
    coins1 = len(state.coins)
    player.direction = direction
    player.update()
    coins2 = len(state.coins)
    assert (
            (coins0 - 1 == coins1) and
            ((coins1 - 1 == coins2) is bool_check)
            )


@pytest.mark.parametrize("pos, ghost_pos, direction, collided", collide)
def test_collision(pos, ghost_pos, direction, collided):
    """
    Test if the game can detect collision between OlinMan and the ghost(s)

    args:
        pos: a (pygame.Vector2) the new grid position for the player
        ghost_pos: a (pygame.Vector2) the new grid position for the ghost
        direction: a (pygame.Vector2) the direction the sprite will move
        collided: a (bool) that is (True) if the ghost have collided
    """
    state = olin_man_game.Game_State()
    player = state.olin_man
    player.set_speed(const.WINDOW_SCALE)
    player.teleport(pos)
    player.direction = direction
    ghost = state.red_ghost
    ghost.set_speed(const.WINDOW_SCALE)
    ghost.teleport(ghost_pos)
    ghost.direction = direction * -1

    player.update()
    ghost.update()

    assert state.check_colide() == collided


@pytest.mark.parametrize("pos, direction", teleports)
def test_reset(pos, direction):
    """
    Test if reset function and with that the teleport function,
        will move the sprite and change the sprites direction

    args:
        pos: a (pygame.Vector2) the new grid position for the player
        direction: a (pygame.Vector2) the direction the sprite will move
    """
    state = olin_man_game.Game_State()
    player = state.olin_man
    player.set_speed(const.WINDOW_SCALE)
    first_direct = player.direction
    first_pos = player.get_pos()
    player.teleport(pos)
    player.direction = direction
    pos_changed = first_pos != player.get_pos()
    direction_changed = first_direct != player.direction
    values_correct = pos == player.get_pos() and direction == player.direction
    assert values_correct and pos_changed and direction_changed
