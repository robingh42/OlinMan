import pygame
from pygame.locals import *
#from olin_man_game import Viewer
import constants as const

pygame.init()

class MoveablePlayer(pygame.sprite.Sprite):
    def __init__(self, state, pos, speed, image):
        pygame.sprite.Sprite.__init__(self)
        self.state = state
        self._surface = pygame.display.get_surface()
        self.area = state.view.window_screen.get_rect()
        self.image, self.rect = state.view.load_image(image)
        print(pos[0],pos[1])
        self.rect = self.rect.move(pos[0], pos[1])
        self.move_pos = [0, 0]
        self.direction = "none"
        self.grid_pos = [int((self.rect.x+.5)//const.WINDOW_SCALE), int((self.rect.y+.5)//const.WINDOW_SCALE)]
        #self._rect = self.image.get_rect()
        self._speed = speed
        self.pimpleUP = [self.grid_pos[0], self.grid_pos[1]-1]
        self.pimpleDown = [self.grid_pos[0], self.grid_pos[1]+1]
        self.pimpleLeft = [self.grid_pos[0]-1, self.grid_pos[1]]
        self.pimpleRight = [self.grid_pos[0]+1, self.grid_pos[1]]
        self.mapUP = self.grid_pos[0], self.grid_pos[1]-4
        self.mapDown = self.grid_pos[0], self.grid_pos[1]-2
        self.mapLeft = self.grid_pos[0]-1, self.grid_pos[1]-3
        self.mapRight = self.grid_pos[0]+1, self.grid_pos[1]-3
    def collision(self):
        pass

    def update(self):
        newpos = self.rect.move(self.move_pos)
        
        if self.direction == "up":
            newgrid = self.mapUP
        elif self.direction == "down":
            newgrid = self.mapDown
        elif self.direction == "left":
            newgrid = self.mapLeft
        elif self.direction == "right":
            newgrid = self.mapRight
        else:
            newgrid = self.grid_pos
        fake_sprite = pygame.sprite.Sprite()
        fake_sprite.rect = newpos
        if self.area.contains(newpos) and const.MAP[newgrid[1]][newgrid[0]] != 1:
            self.rect = newpos
        self.grid_pos = [int((self.rect.x+8)//const.WINDOW_SCALE), int((self.rect.y+8)//const.WINDOW_SCALE)]
        self.pimpleUP = [self.grid_pos[0], self.grid_pos[1]-1]
        self.pimpleDown = [self.grid_pos[0], self.grid_pos[1]+1]
        self.pimpleLeft = [self.grid_pos[0]-1, self.grid_pos[1]]
        self.pimpleRight = [self.grid_pos[0]+1, self.grid_pos[1]]
        self.mapUP = [self.grid_pos[0], self.grid_pos[1]-4]
        self.mapDown = [self.grid_pos[0], self.grid_pos[1]-2]
        self.mapLeft = [self.grid_pos[0]-1, self.grid_pos[1]-3]
        self.mapRight = [self.grid_pos[0]+1, self.grid_pos[1]-3]
        #self.draw(self.state.view.window_screen)
        #print(self.rect.x, self.rect.y)
        print(self.mapUP, self.mapDown, self.mapLeft, self.mapRight)
        self.state.view.draw_txt(
            str(const.MAP[self.mapUP[1]][self.mapUP[0]]),
            const.WHITE,
            [
            (self.pimpleUP[0])*const.WINDOW_SCALE,
            self.pimpleUP[1]*const.WINDOW_SCALE
            ],
            center=False
            )

        self.state.view.draw_txt(
            str(const.MAP[self.mapDown[1]][self.mapDown[0]]),
            const.RED,
            [
            (self.pimpleDown[0])*const.WINDOW_SCALE,
            self.pimpleDown[1]*const.WINDOW_SCALE
            ],
            center=False
            )

        self.state.view.draw_txt(
            str(const.MAP[self.mapLeft[1]][self.mapLeft[0]]),
            const.GREEN,
            [
            self.pimpleLeft[0]*const.WINDOW_SCALE,
            (self.pimpleLeft[1])*const.WINDOW_SCALE
            ],
            center=False
            )

        self.state.view.draw_txt(
            str(const.MAP[self.mapRight[1]][self.mapRight[0]]),
            const.START_ORANGE,
            [
            self.pimpleRight[0]*const.WINDOW_SCALE,
            (self.pimpleRight[1])*const.WINDOW_SCALE
            ],
            center=False
            )
        print(self.mapDown[0],self.mapDown[1])
        pygame.display.update()
        pygame.event.pump()

    def move(self):
        pass

    


class OlinMan(MoveablePlayer):

    def __init__(self, state, lives):
        MoveablePlayer.__init__(self, state, [const.WINDOW_SCALE * 13.5, const.WINDOW_SCALE * 26], 10, "Olinman.png")
        self.image = pygame.transform.scale(
            self.image, 
            (24, 24)
            )
        
        self.rect = pygame.rect.Rect(const.WINDOW_SCALE * 13.5, const.WINDOW_SCALE * 26, const.WINDOW_SCALE, const.WINDOW_SCALE)
        
        self._lives = lives
        #self.rect = self.rect.move()
    
    def move(self, direction):
        """
        fake_sprite = pygame.sprite.Sprite()
        if direction == "up": 
            newpos = self.rect.move([0,-self._speed/2])
        elif direction == "down": 
            newpos = self.rect.move([0,self._speed/2])
        elif direction == "right": 
            newpos = self.rect.move([self._speed/2,0])
        elif direction == "left": 
            newpos = self.rect.move([-self._speed/2,0])
        fake_sprite.rect = newpos
        has_wall = pygame.sprite.spritecollide(fake_sprite, self.state.walls, 0) != []
        """
        #print(pygame.sprite.spritecollide(self, self.state.walls, 0))
        #if not has_wall:
        moveable = {0,3,4}
        print(self.mapUP, self.mapDown, self.mapLeft, self.mapRight)
        print(
            self.grid_pos,
            const.MAP[self.mapUP[1]][self.mapUP[0]],
            const.MAP[self.mapDown[1]][self.mapDown[0]],
            const.MAP[self.mapLeft[1]][self.mapLeft[0]],
            const.MAP[self.mapRight[1]][self.mapRight[0]]
            )
        
        
        if direction == "up" and const.MAP[self.mapUP[1]][self.mapUP[0]] != 1: 
            self.move_pos = [0,-self._speed/2]
            self.direction = "up"
        elif direction == "down" and const.MAP[self.mapDown[1]][self.mapDown[0]] != 1: 
            self.move_pos = [0,self._speed/2]
            self.direction = "down"
        elif direction == "left" and const.MAP[self.mapLeft[1]][self.mapLeft[0]] != 1: 
            self.move_pos = [-self._speed/2,0]
            self.direction = "left"
        elif direction == "right" and const.MAP[self.mapRight[1]][self.mapRight[0]] != 1: 
            self.move_pos = [self._speed/2,0]
            self.direction = "right"


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

class blinky(Ghost):
    def __init__(self, state):
        pass

    def find_target(self):
        # on Olin Man
        pass


class pinky(Ghost):
    def __init__(self, state):
        pass

    def find_target(self):
        # 4 squares Olin Man
        pass

class inky(Ghost):
    def __init__(self, state):
        pass

    def find_target(self):
        # opposite blinky
        pass


class clyde(Ghost):
    def __init__(self, state):
        pass
