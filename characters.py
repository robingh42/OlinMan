import pygame
from pygame.locals import *
import constants as const
import random
# Import pygames vector function to simplify movement and positions as vec
vec = pygame.math.Vector2

# Initiate pygame
pygame.init()


class MoveablePlayer(pygame.sprite.Sprite):
    """
    Movable sprites used for all levels.

    Inherits all attributes from pygame.Sprites

    Attributes:
        state: a (GameState) for checking conditions of the board
        _area: a (pygame.Rect) depicting the size of the window screen
        image: a (pygame.image) for a basic sprite state
        rect: a (pygame.Rect) for postioning and colision detection
        image2: a (pygame.image) for a second sprite state
        direction: a (pygame.Vector2) the direction the sprite will move
            depicted in change in postion
        _last_direct: a (pygame.Vector2) the last direction the sprite
            was moving in
        _grid_pos: a (pygame.Vector2) the current position of the sprite
            on the grid
        _last_grid: a (pygame.Vector2) the last position of the sprite
            on the grid
        _speed: an (int) depicting the number of pixels to move per frame
        dead: a (bool) depicting if the sprite is dead (True) or alive (False)
    """

    def __init__(self, state, pos, speed, image, image2):
        """
        Creates the MovablePlayer

        args:
            state: a (GameState) for checking conditions of the board
            pos: the position (pygame.Vector2) on the grid to place the sprite
            speed: an (int) depicting the number of pixels to move per frame
            image: a file name (string) to find the image to load
            image2: a file name (string) to find the image to load
        """
        # init super and get the game state
        pygame.sprite.Sprite.__init__(self)
        self.state = state
        self._area = state.view.window_screen.get_rect()

        # load image, and base rect
        self.image, self.rect = state.view.load_image(image)
        self.image = pygame.transform.scale(
            self.image,
            (24, 24)
            )

        # create a second scaled image for a second state
        self.image2 = state.view.object_image(image2, 1.5, 1.5)

        # resize rect to the size of each grid block, and place the sprite
        self.rect = pygame.rect.Rect(
            const.WINDOW_SCALE * pos[0],
            const.WINDOW_SCALE * pos[1],
            const.WINDOW_SCALE,
            const.WINDOW_SCALE)

        # setup directions, and positions
        self._last_direct = vec(0, 0)
        self.direction = vec(0, 0)
        self._grid_pos = vec(
            int((self.rect.x+8)//const.WINDOW_SCALE),
            int((self.rect.y+8)//const.WINDOW_SCALE)
            )
        self._last_grid = self._grid_pos
        self._speed = speed
        self.dead = False

    def collision(self):
        """
        A method to update the charater if there is a colision
        """
        pass

    def revive(self):
        """
        Revives the sprite if it is dead
        """
        self.dead = False

    def update(self):
        """
        Updates the charater's position each frame
        Checks if the position can be updated.
        """
        # create a copy of rect in the new position
        movement = self._speed * self.direction
        newpos = self.rect.move(movement[0], movement[1])

        # if the character can move, move the player
        if self._area.contains(newpos) and self.can_move():
            self.rect = newpos
            # update memory arguments
            self._last_direct = self.direction
            self._last_grid = self._grid_pos

        # update the current grid position
        self._grid_pos = vec(
            int((self.rect.x+8)//const.WINDOW_SCALE),
            int((self.rect.y+8)//const.WINDOW_SCALE)
            )

        # if the direction has changed, center the sprite in the grid
        if self._last_direct == self.direction:

            # if the sprite is moving vertialy center them horizontaly
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                self.rect.y = const.WINDOW_SCALE * self._grid_pos[1]
            # if the sprite is moving horizontaly center them vertialy
            elif self.direction == vec(0, 1) or self.direction == vec(0, -1):
                self.rect.x = const.WINDOW_SCALE * self._grid_pos[0]
            # if the sprite hits a wall center them in their grid
            if not self.can_move():
                self.rect.x = const.WINDOW_SCALE * self._grid_pos[0]
                self.rect.y = const.WINDOW_SCALE * self._grid_pos[1]

    def move(self, direction):
        """
        Takes a given direction as a (string) and sets the charater's direction
        as a (pygame.Vector2)

        args:
            direction: a (string) depicting the direction to move the player
        """

        # change the sprites direction based on input
        if direction == "up":
            self.direction = vec(0, -1)
        elif direction == "down":
            self.direction = vec(0, 1)
        elif direction == "left":
            self.direction = vec(-1, 0)
        elif direction == "right":
            self.direction = vec(1, 0)
        else:
            # otherwise set the player to stop moving
            self.direction = vec(0, 0)

        # if the new direction would cause the player to go into a wall
        # revert to last direction
        if self.can_move():
            self._last_direct = self.direction
        else:
            self.direction = self._last_direct

    def teleport(self, pos):
        """
        Takes a given grid position as a (pygame.Vector2) and sets the
        charater's direction as a (pygame.Vector2)

        args:
            pos: a (pygame.Vector2) the new grid position for the player
        """

        # create a rect in the new position
        newpos = pygame.rect.Rect(
            const.WINDOW_SCALE * pos[0],
            const.WINDOW_SCALE * pos[1],
            const.WINDOW_SCALE,
            const.WINDOW_SCALE)

        # if the position is on screen and not a wall move the sprite
        if self._area.contains(newpos) and pos not in self.state.walls:
            self.rect = newpos
            self._grid_pos = vec(
                int((self.rect.x+8)//const.WINDOW_SCALE),
                int((self.rect.y+8)//const.WINDOW_SCALE)
                )

    def can_move(self):
        """
        Returns a (bool) if there is a wall in the sprites next position
        """
        if vec(self._grid_pos + self.direction) in self.state.walls:
            return False
        return True


class OlinMan(MoveablePlayer):
    """
    A Movable player controled by the user.

    Inherits all attributes from MoveablePlayer

    Attributes:
        image3: a (pygame.image) for a third player state
        lives: an (int) depicting the number of lives the player has left
    """

    def __init__(self, state, lives):
        """
        Initiate Olin man from MovablePlayers init method

        args:
            state: a (GameState) for checking conditions of the board
            lives: an (int) depicting the number of lives the player has left
        """

        MoveablePlayer.__init__(
            self,
            state,
            vec(13.5, 26),
            2,
            "Olinman.png",
            "Olinman_bounce.png")

        # Create a third player image and scale it
        self.image3 = state.view.object_image("Olinman_squeeze.png", 1.5, 1.5)
        self.lives = lives

    def update(self):
        """
        Updates the charater's position each frame
        Checks if the position can be updated.
        Check is the player has interacted with an object and update the object
        Checks for tunnel usage
        """
        super().update()
        if self.on_coin():
            self.eat_coin()
        elif self.on_coffee():
            self.drink_coffee()
        # if the player has moved to the end of a tunnel
        # teleport it to the other tunnel
        elif self._grid_pos == vec(1, 17):
            self.teleport(vec(24, 17))
        elif self._grid_pos == vec(26, 17):
            self.teleport(vec(3, 17))

    def collision(self):
        """
        Updates the player after a colision. Remove a life and kill the player.
        """
        self.lives -= 1
        self.dead = True

    def on_coin(self):
        """
        Checks if the player is on a coin. Returns a (bool).
        """
        if self._grid_pos in self.state.coins:
            return True
        else:
            return False

    def on_coffee(self):
        """
        Checks if the player is on a coffee. Returns a (bool).
        """
        if self._grid_pos in self.state.coffees:
            return True
        else:
            return False

    def eat_coin(self):
        """
        Remove a coin under the player and increase the score.
        """
        self.state.coins.remove(self._grid_pos)
        self.state.score += 10

    def drink_coffee(self):
        """
        Remove a coin under the player and increase the score.
        """
        self.state.coffees.remove(self._grid_pos)
        self.state.score += 50


class Ghost(MoveablePlayer):
    """
    A MovablePlayer to avoid, self selects movement.

    Inherits all attributes from MoveablePlayer
    """

    def __init__(self, state, pos, speed,
                 direction=vec(1, 0), image="Red_Ghost.png"):
        """
        Initiate ghosts from MovablePlayers init method

        args:
            state: a (GameState) for checking conditions of the board
            pos: the position (pygame.Vector2) on the grid to place the sprite
            speed: an (int) depicting the number of pixels to move per frame
        """
        MoveablePlayer.__init__(
            self,
            state,
            vec(pos[0], pos[1]),
            speed,
            image,
            "Fright_Ghost.png")

        self.direction = direction

    def update(self):
        """
        Updates the charater's position each frame
        Checks if the position can be updated.
        """
        self.move()
        super().update()

    def moves(self):
        """
        Returns a (list) of all directions (pygame.Vector2) the ghost can move
        """
        walls = [True, True, True, True]
        directions = [vec(0, -1), vec(0, 1), vec(-1, 0), vec(1, 0)]
        for i in range(4):
            if (self._grid_pos + directions[i] not in self.state.walls):
                walls[i] = False
        # only return directions without a wall
        return [directions[i] for i in range(len(walls)) if walls[i] is False]

    def can_move(self):
        """
        Returns a (bool) if there is a wall in the sprites next position
            or if the position would put the ghost in a tunnel (False)
            Otherwise return (True)
        """
        if (
            self._grid_pos + self.direction in self.state.walls or
            self._grid_pos + self.direction in [vec(5, 17), vec(22, 17)]
                ):
            return False
        return True

    def move(self):
        """
        Choses a direction to move each frame.
        """
        # if the grid position hasn't changed and the ghost can move, break
        if self._last_grid == self._grid_pos and self.can_move():
            return

        # get all the directions the ghost can move
        directions = self.moves()

        # if the ghost can move backwards, remove that option
        if self.direction * -1 in directions:
            directions.remove(self.direction * -1)

        # if there is more than one option, make the option a 1/4 chance
        # that the ghost will change direction
        # otherwise move in that direction
        if len(directions) > 1:
            for _ in range(3):
                directions.append(self.direction)
            self.direction = random.choice(directions)
        else:
            self.direction = directions[0]

    def reset(self, pos=vec(13, 14), direction=vec(1, 0)):
        """
        Resets the ghost by placing them in a new position
            and setting a new direction

        args:
            direction: the direction (pygame.Vector2) the sprite will move
            depicted in change in postion
            pos: a (pygame.Vector2) the new position of the sprite
            on the grid
        """
        self.teleport(pos)
        self.direction = direction
