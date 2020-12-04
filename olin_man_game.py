import pygame
import os
from pygame.locals import *

pygame.init()


class Game_state:
    """
    The state of the game
    """
    def __init__(self):
        # some pygame stuff

        self._board = pygame.sprite.Group() # create a group of walls


        # create Olin man
        # create ghosts


class Controler:
    """
    Controls the game
    """
    # uses pygame.event to check key presses
    # runs the menu selection
    def __init__(self):
        pass

    def pause(self):
        # if p or Esc is pressed, loop untill they are pressed a second time
        pass


class Viewer:
    """
    Displays the game
    """
    def __init__(self):
        # some pygame stuff
        # sets up a pygame display
        _window_width = 448
        _window_height = 512
        _window_size = (_window_width,_window_height)
        _sprite_len = 16
        window_surface = pygame.display.set_mode(_window_size, pygame.RESIZABLE)
        window_surface.fill((0,0,0))

    def update_sprites(self):
        # Moves on screen sprite based on kep presses, or move methods
        pass

    @staticmethod
    def load_image(name):
        """ Load image and return image object"""
        fullname = os.path.join('images', name)
        try:
            image = pygame.image.load(fullname)

            if image.get_alpha is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pygame.error as message:
            print('Cannot load image:', fullname)
            raise SystemExit
        return image, image.get_rect()