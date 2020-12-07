import pygame
from pygame.locals import *
#from olin_man_game import Viewer
import constants as const

pygame.init()

class Nonmovable(pygame.sprite.Sprite):
    def __init__(self, state, image, points=0):
        pygame.sprite.Sprite.__init__(self)
        self._points = points
        self.image, self.rect = state.view.load_image(image)
        self.state = state


class snack(Nonmovable):
    def __init__(self, state):
        #super().__init__(10)
        pass


class coffee(Nonmovable):
    def __init__(self, state):
        super().__init__(state, "Coffee_32.gif", 50)


class wall(Nonmovable):
    def __init__(self, state):
        super().__init__(state, "Wall.png", 0)

    def draw(self, pos):
        self.state.view.window_screen.blit(
                     self.image, 
                     (const.WINDOW_SCALE * pos[0],
                     const.WINDOW_SCALE * (pos[1]))
                    )
        


class cherry(Nonmovable):
    def __init__(self):
        #super().__init__(1000)
        pass
