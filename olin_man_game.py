import pygame
import os
import sys
from pygame.locals import *

pygame.init()




class App:

    def __init__(self):
        self._state = Game_State()
        self._draw = Viewer(self._state)
        self._inputs = Controler()
        self._running = True
        self._start_screen = True

    def run(self):
        while self._running:
            if self._state.is_intro():
                self.start_events()
                self._state.start()
                self._draw.start()
            else :
                self.events()
                #self._draw.clear_Screen()
                self._draw.draw_background()
                self._draw.draw_grid()
                
            self._draw.clock.tick(self._draw._FPS)
        pygame.quit()
        sys.exit()
    
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._state.level += 1
                print(self._state.level)
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                

          


class Game_State:
    """
    The state of the game
    """
    def __init__(self):
        self.level = 0
        
        # some pygame stuff
        #self._board = pygame.sprite.Group() # create a group of walls
        # create Olin man
        # create ghosts

    def is_intro(self):
        return self.level == 0

    def events(self):
        pass

    def start(self):
        pass
    
    
          


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

    BLACK = (0,0,0)
    WHITE = (255, 255, 255)
    START_ORANGE = (170, 130, 60)
    OLIN_BLUE = (0,155,223)
    GREY = (100,100,100)

    def __init__(self, state):
        # some pygame stuff
        # sets up a pygame display
        self._WINDOW_SCALE = 16
        self._WINDOW_WIDTH = 28 * self._WINDOW_SCALE
        self._WINDOW_HEIGHT = 36 * self._WINDOW_SCALE
        self._FPS = 60


        self._text_size = 16

        self._font = pygame.font.Font(
            "PressStart2P-Regular.ttf",
            self._text_size
            )

        self._sprite_len = 32
        self.window_screen = pygame.display.set_mode(
            (self._WINDOW_WIDTH, self._WINDOW_HEIGHT)
            )
        self.window_screen.fill(Viewer.BLACK)
        self.clock = pygame.time.Clock()
        

    def update_sprites(self):
        # Moves on screen sprite based on kep presses, or move methods
        pass

    def clear_Screen(self):
        self.window_screen.fill(Viewer.BLACK)
        pygame.display.update()

    def start(self):
        
        self.draw_txt(
            "HIGH SCORE",
            Viewer.WHITE,
            [0, 0 +9]
            )
        self.draw_txt(
            "Olin Man:",
            Viewer.OLIN_BLUE,
            [0, self._WINDOW_HEIGHT / 4],
            title=True
            )
        self.draw_txt(
            "The Video Game",
            Viewer.WHITE,
            [0, self._WINDOW_HEIGHT / 4 + 32]
            )
        self.draw_txt(
            "Press [Space] to Play",
            Viewer.START_ORANGE,
            [0, self._WINDOW_HEIGHT / 2]
            )

        pygame.display.update()
        self.clock.tick(self._FPS)

    def draw_txt(self, text, RGB_color, pos, center=True, title=False):
        text_to_print = self._font.render(text, False, RGB_color)
        if title:
            font = pygame.font.Font(
                "PressStart2P-Regular.ttf",
                self._text_size * 2
                )
            text_to_print = font.render(text, False, RGB_color)
        if center:
            pos[0] = self._WINDOW_WIDTH / 2
        textpos = text_to_print.get_rect(centerx=pos[0], centery=pos[1])
        self.window_screen.blit(text_to_print, textpos)
    
    def draw_grid(self):
        for x in range(28):
            pygame.draw.line(
                self.window_screen,
                Viewer.GREY,
                (x * self._WINDOW_SCALE, 0),
                (x * self._WINDOW_SCALE, self._WINDOW_HEIGHT)
                )
        for y in range(36):
            pygame.draw.line(
                self.window_screen,
                Viewer.GREY,
                (0, y * self._WINDOW_SCALE),
                (self._WINDOW_WIDTH, y * self._WINDOW_SCALE)
                )
        pygame.display.update()


    def draw_background(self):
        fullname = os.path.join("images", "Maze.jpeg")
        self.background = pygame.image.load(fullname)
        self.background = pygame.transform.scale(
            self.background, 
            (self._WINDOW_WIDTH, 31 * self._WINDOW_SCALE)
            )
        self.window_screen.blit(self.background, (0, self._WINDOW_SCALE * 3))
        pygame.display.update()

    @staticmethod
    def load_image(name):
        """ Load image and return image object"""
        fullname = os.path.join("images", name)
        try:
            image = pygame.image.load(fullname)

            if image.get_alpha is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pygame.error as message:
            print("Cannot load image:", fullname)
            raise SystemExit
        return image, image.get_rect()

if __name__ == "__main__":
    app = App()
    app.run()