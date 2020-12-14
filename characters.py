import pygame
from pygame.locals import *
import constants as const
vec = pygame.math.Vector2

pygame.init()


class MoveablePlayer(pygame.sprite.Sprite):
    def __init__(self, state, pos, speed, image):
        pygame.sprite.Sprite.__init__(self)
        self.state = state
        self.area = state.view.window_screen.get_rect()
        self.image, self.rect = state.view.load_image(image)

        print(pos[0], pos[1])
        self.rect = self.rect.move(pos[0], pos[1])
        self.past_direct = vec(0, 0)
        self.direction = vec(0, 0)
        self.grid_pos = vec(
            int((self.rect.x+8)//const.WINDOW_SCALE),
            int((self.rect.y+8)//const.WINDOW_SCALE)
            )
        self._speed = speed

    def collision(self):
        pass

    def update(self):
        # print(self.direction)
        movement = self._speed * self.direction
        # print(movement)
        newpos = self.rect.move(movement[0], movement[1])

        if self.area.contains(newpos) and self.can_move():
            self.rect = newpos
            self.past_direct = self.direction

        self.grid_pos = vec(
            int((self.rect.x+8)//const.WINDOW_SCALE),
            int((self.rect.y+8)//const.WINDOW_SCALE)
            )

        if self.past_direct == self.direction:

            if self.direction == vec(1,0) or self.direction == vec(-1,0):
                self.rect.y = const.WINDOW_SCALE * self.grid_pos[1]
                print("updown")
            elif self.direction == vec(0,1) or self.direction == vec(0,-1):
                self.rect.x = const.WINDOW_SCALE * self.grid_pos[0]
                print("leftright")
            if not self.can_move():
                print("selfcorrect")
                self.rect.x = const.WINDOW_SCALE * self.grid_pos[0]
                self.rect.y = const.WINDOW_SCALE * self.grid_pos[1]
            
    def move(self, direction):
        """

        """
        
        if direction == "up":
            self.direction = vec(0, -1)
        elif direction == "down":
            self.direction = vec(0, 1)
        elif direction == "left":
            self.direction = vec(-1, 0)
        elif direction == "right":
            self.direction = vec(1, 0)
        else:
            self.direction = vec(0, 0)

        if self.can_move():
            self.past_direct = self.direction
        else:
            self.direction = self.past_direct

    def can_move(self):
        # print("start")
        for wall in self.state.walls:
            # print(self.grid_pos+self.direction, wall)
            if vec(self.grid_pos+self.direction) == wall:

                print("can't move")

                return False
        # print("can move")
        return True



class OlinMan(MoveablePlayer):

    def __init__(self, state, lives):
        MoveablePlayer.__init__(
            self,
            state,
            [const.WINDOW_SCALE * 13.5, const.WINDOW_SCALE * 26],
            2.5,
            "Olinman.png")

        self.image = pygame.transform.scale(
            self.image,
            (24, 24)
            )

        self.rect = pygame.rect.Rect(
            const.WINDOW_SCALE * 13.5,
            const.WINDOW_SCALE * 26,
            const.WINDOW_SCALE,
            const.WINDOW_SCALE)

        self.lives = lives
        # self.rect = self.rect.move()

    def update(self):
        # print(self.direction)
        movement = self._speed * self.direction
        # print(movement)
        newpos = self.rect.move(movement[0], movement[1])

        if self.area.contains(newpos) and self.can_move():
            self.rect = newpos
            self.past_direct = self.direction

        self.grid_pos = vec(
            int((self.rect.x+8)//const.WINDOW_SCALE),
            int((self.rect.y+8)//const.WINDOW_SCALE)
            )
        
        if self.on_coin():
            self.eat_coin()

        if self.past_direct == self.direction:

            if self.direction == vec(1,0) or self.direction == vec(-1,0):
                self.rect.y = const.WINDOW_SCALE * self.grid_pos[1]
                print("updown")
            elif self.direction == vec(0,1) or self.direction == vec(0,-1):
                self.rect.x = const.WINDOW_SCALE * self.grid_pos[0]
                print("leftright")
            if not self.can_move():
                print("selfcorrect")
                self.rect.x = const.WINDOW_SCALE * self.grid_pos[0]
                self.rect.y = const.WINDOW_SCALE * self.grid_pos[1]

    def teleport(self, pos, direction):
        newpos = pygame.rect.Rect(
            const.WINDOW_SCALE * pos,
            const.WINDOW_SCALE * pos,
            const.WINDOW_SCALE,
            const.WINDOW_SCALE)

        if self.area.contains(newpos):
            self.rect = newpos

            self.grid_pos = vec(
                int((self.rect.x+8)//const.WINDOW_SCALE),
                int((self.rect.y+8)//const.WINDOW_SCALE)
                )
                
            self.move(direction)

    def on_coin(self):
        if self.grid_pos in self.state.coins:
            return True
        else:
            return False

    def on_coffee(self):
        if self.grid_pos in self.state.coffee:
            return True
        else:
            return False

    def eat_coin(self):
        self.state.coins.remove(self.grid_pos)
        self.state.score += 10

    def drink_coffee(self):
        self.state.coffee.remove(self.grid_pos)
        self.state.score += 50

# Enemies to avoid
class Ghost(MoveablePlayer):

    def __init__(self, state):
        self._is_chase
        pass

    def frightened(self):
        pass

    def find_target(self):
        pass

    def move(self):
        pass
