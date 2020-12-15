import pygame
from pygame.locals import *
import constants as const
import random
vec = pygame.math.Vector2

pygame.init()


class MoveablePlayer(pygame.sprite.Sprite):
    def __init__(self, state, pos, speed, image):
        pygame.sprite.Sprite.__init__(self)
        self.state = state
        self.area = state.view.window_screen.get_rect()
        self.image, self.rect = state.view.load_image(image)
        self.image = pygame.transform.scale(
            self.image,
            (24, 24)
            )
        print(pos[0], pos[1])
        self.rect = self.rect.move(pos[0], pos[1])
        self.past_direct = vec(0, 0)
        self.direction = vec(0, 0)
        self.grid_pos = vec(
            int((self.rect.x+8)//const.WINDOW_SCALE),
            int((self.rect.y+8)//const.WINDOW_SCALE)
            )
        self.last_grid = self.grid_pos
        self._speed = speed
        self.dead = False

    def collision(self):
        pass

    def revive(self):
        self.dead = False

    def update(self):
        # print(self.direction)
        movement = self._speed * self.direction
        # print(movement)
        newpos = self.rect.move(movement[0], movement[1])

        if self.area.contains(newpos) and self.can_move():
            self.rect = newpos
            self.past_direct = self.direction
            self.last_grid = self.grid_pos

        
        self.grid_pos = vec(
            int((self.rect.x+8)//const.WINDOW_SCALE),
            int((self.rect.y+8)//const.WINDOW_SCALE)
            )

        if self.past_direct == self.direction:

            if self.direction == vec(1,0) or self.direction == vec(-1,0):
                self.rect.y = const.WINDOW_SCALE * self.grid_pos[1]
                #print("updown")
            elif self.direction == vec(0,1) or self.direction == vec(0,-1):
                self.rect.x = const.WINDOW_SCALE * self.grid_pos[0]
                #print("leftright")
            if not self.can_move():
                #print("selfcorrect")
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

    def teleport(self, pos):
        newpos = pygame.rect.Rect(
            const.WINDOW_SCALE * pos[0],
            const.WINDOW_SCALE * pos[1],
            const.WINDOW_SCALE,
            const.WINDOW_SCALE)

        if self.area.contains(newpos):
            self.rect = newpos

            self.grid_pos = vec(
                int((self.rect.x+8)//const.WINDOW_SCALE),
                int((self.rect.y+8)//const.WINDOW_SCALE)
                )

    def can_move(self):
        # print("start")
            # print(self.grid_pos+self.direction, wall)
        if vec(self.grid_pos+self.direction) in self.state.walls:

            #print("can't move")

            return False
        # print("can move")
        return True



class OlinMan(MoveablePlayer):

    def __init__(self, state, lives):
        MoveablePlayer.__init__(
            self,
            state,
            [const.WINDOW_SCALE * 13.5, const.WINDOW_SCALE * 26],
            2,
            "Olinman.png")

        self.rect = pygame.rect.Rect(
            const.WINDOW_SCALE * 13.5,
            const.WINDOW_SCALE * 26,
            const.WINDOW_SCALE,
            const.WINDOW_SCALE)

        self.lives = lives
        # self.rect = self.rect.move()

    def update(self):
        super().update()
        if self.on_coin():
            self.eat_coin()
        elif self.on_coffee():
            self.drink_coffee()
        elif self.grid_pos == vec(1,17):
            self.teleport(vec(24,17))
        elif self.grid_pos == vec(26,17):
            self.teleport(vec(3,17))   

    def collision(self, ghost):
        self.lives -= 1
        self.dead = True
        if ghost.is_frightened:
            pass

    def on_coin(self):
        if self.grid_pos in self.state.coins:
            return True
        else:
            return False

    def on_coffee(self):
        if self.grid_pos in self.state.coffees:
            return True
        else:
            return False

    def eat_coin(self):
        self.state.coins.remove(self.grid_pos)
        self.state.score += 10

    def drink_coffee(self):
        self.state.coffees.remove(self.grid_pos)
        self.state.score += 50

# Enemies to avoid
class Ghost(MoveablePlayer):

    def __init__(self, state, pos, speed, direction=vec(1,0)):
        self.is_frightened = False
        MoveablePlayer.__init__(
            self,
            state,
            [const.WINDOW_SCALE * pos[0], const.WINDOW_SCALE * pos[1]],
            speed,
            "Red_Ghost.png")

        self.rect = pygame.rect.Rect(
            const.WINDOW_SCALE * pos[0],
            const.WINDOW_SCALE * pos[1],
            const.WINDOW_SCALE,
            const.WINDOW_SCALE)

        self.direction = direction
        

    def frightened(self):
        pass

    def update(self):
        self.move()
        super().update()

    def start(self):
        pass

    def moves(self):
        walls = [0,0,0,0]
        directions = [vec(0,-1), vec(0,1), vec(-1,0), vec(1,0)]
        for i in range(4):
                # print(self.grid_pos+self.direction, wall)
            if (self.grid_pos + directions[i] not in self.state.walls):

                #print("can't move")

                walls[i] += 1

        return walls

    def can_move(self):
        if (
            self.grid_pos+self.direction in self.state.walls or
            self.grid_pos+self.direction in [vec(5,17),vec(22,17)]
            ):
            return False
        return True

    def move(self):
        if self.last_grid == self.grid_pos and self.can_move():
            return
        paths = self.moves()
        directions = [vec(0,-1), vec(0,1), vec(-1,0), vec(1,0)]
        directions = [directions[i] for i in range(len(paths)) if paths[i] != 0]
        #print(directions, paths)

        if self.direction * -1 in directions:
            directions.remove(self.direction * -1)

        if len(directions) > 1:
            for _ in range(3):
                directions.append(self.direction)
            self.direction = random.choice(directions)
        else:
            self.direction = directions[0]
