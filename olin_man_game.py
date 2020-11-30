import pygame


class Game_state:
    
    def __init__(self):
        # some pygame stuff

        self._board = pygame.sprite.Group() # create a group of walls


        # create Olin man
        # create ghosts
        pass


class Controler:
    # uses pygame.event to check key presses
    # runs the menu selection 
    def __init__(self):
        pass

    def pause(self):
        # if p or Esc is pressed, loop untill they are pressed a second time
        pass


class Viewer:
    
    def __init__(self):
        # some pygame stuff
        # sets up a pygame display
        pass

    def update_sprites(self):
        # Moves on screen sprite based on kep presses, or move methods
        pass