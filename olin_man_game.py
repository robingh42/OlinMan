import pygame
import os
import sys
from pygame.locals import *
import objects, characters
import constants as const
vec = pygame.math.Vector2

pygame.init()




class Game_State:
    """
    The state of the game
    """
    def __init__(self):
        self.view = Viewer(self)
        self.inputs = Controler(self)

        self._running = True
        self._start_screen = True

        self.level = 0
        self.score = 0
        self.walls = []
        self.coins = []
        self.coffees = []
        self.olinsprite = charaters.OlinMan(self, 3)
        self.olinman = pygame.sprite.GroupSingle(self.olinsprite)
        self.setup()
        # some pygame stuff
        #self._board = pygame.sprite.Group() # create a group of walls
        # create Olin man
        # create ghosts

    def is_intro(self):
        return self.level == 0

    def is_running(self):
        return self._running

    def setup(self):
        self.olinsprite = charaters.OlinMan(self, self.olinsprite.lives)
        self.olinman = pygame.sprite.GroupSingle(self.olinsprite)
        self.make_walls()
        self.make_coins()
        self.make_coffee()

    def make_walls(self):
        for row in range(len(const.MAP)):
            for col in range(len(const.MAP[row])):
                if const.MAP[row][col] == 1 or const.MAP[row][col] == 2:
                    #self.window_screen.blit(
                    #    self.wall, 
                    #    (const.WINDOW_SCALE * col,
                    #     const.WINDOW_SCALE * (row + 3))
                    #)

                    self.walls.append(vec(col,(row + 3)))

    def make_coins(self):
        for row in range(len(const.MAP)):
            for col in range(len(const.MAP[row])):
                if const.MAP[row][col] == 4:
                    #self.window_screen.blit(
                    #    self.wall, 
                    #    (const.WINDOW_SCALE * col,
                    #     const.WINDOW_SCALE * (row + 3))
                    #)

                    self.coins.append(vec(col,(row + 3)))

    def make_coffee(self):
        for row in range(len(const.MAP)):
            for col in range(len(const.MAP[row])):
                if const.MAP[row][col] == 3:
                    #self.window_screen.blit(
                    #    self.wall, 
                    #    (const.WINDOW_SCALE * col,
                    #     const.WINDOW_SCALE * (row + 3))
                    #)
                    print("added coffee")
                    self.coffees.append(vec(col,(row + 3)))
                

    

    
    
          


class Controler:
    """
    Controls the game
    """
    # uses pygame.event to check key presses
    # runs the menu selection
    def __init__(self, state):
        self.state = state
        pass

    def pause(self):
        # if p or Esc is pressed, loop untill they are pressed a second time
        pass

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state._running = False
                print("Exiting..")
                pygame.quit()
                print("Done")
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state.level += 1
                print("level:",self.state.level)
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state._running = False
                print("Exiting..")
                pygame.quit()
                print("Done")
                sys.exit()
            elif event.type == KEYDOWN or event.type == KEYUP:
                if event.key == K_w or event.key == K_UP:
                    self.state.olinsprite.move("up")
                    print("keyup")
                elif event.key == K_s or event.key == K_DOWN:
                    self.state.olinsprite.move("down")
                    print("keydwn")
                elif event.key == K_a or event.key == K_LEFT:
                    self.state.olinsprite.move("left")
                    print("keyL")
                elif event.key == K_d or event.key == K_RIGHT:
                    self.state.olinsprite.move("right")
                    print("keyR")
                self.state.olinman.update()
                #self.state.olinman.draw(self.state.view.window_screen)
    
    

    

    
    
            


class Viewer:
    """
    Displays the game
    """

    

    def __init__(self, state):
        # some pygame stuff
        # sets up a pygame display
        
        self.state = state

        self._text_size = 16
        self._font = pygame.font.Font(
            "PressStart2P-Regular.ttf",
            self._text_size
            )

        self._sprite_len = 32
        self.window_screen = pygame.display.set_mode(
            (const.WINDOW_WIDTH, const.WINDOW_HEIGHT)
            )
        self.window_screen.fill(const.BLACK)

        self.clock = pygame.time.Clock()

        self.background = self.object_image("Maze.jpeg",1,31)
        self.wall = self.object_image("Wall.png")
        self.coin = self.object_image("Coin.png")
        self.coffee = self.object_image("Coffee.png",)
        
        print("view init")



    def update_sprites(self):
        # Moves on screen sprite based on kep presses, or move methods
        pass

    

    def clear_Screen(self):
        self.window_screen.fill(const.BLACK)

    def start(self):
        self.draw_txt(
            "HIGH SCORE",
            const.WHITE,
            [0, 0 + 9]
            )
        self.draw_txt(
            "Olin Man:",
            const.OLIN_BLUE,
            [0, const.WINDOW_HEIGHT / 4],
            title=True
            )
        self.draw_txt(
            "The Video Game",
            const.WHITE,
            [0, const.WINDOW_HEIGHT / 4 + 32]
            )
        self.draw_txt(
            "Press [Space] to Play",
            const.START_ORANGE,
            [0, const.WINDOW_HEIGHT / 2]
            )

        pygame.display.update()
        self.clock.tick(const.FPS)

    def draw_txt(self, text, RGB_color, pos, center=True, title=False):
        text_to_print = self._font.render(text, False, RGB_color)
        if title:
            font = pygame.font.Font(
                "PressStart2P-Regular.ttf",
                self._text_size * 2
                )
            text_to_print = font.render(text, False, RGB_color)
        if center:
            pos[0] = const.WINDOW_WIDTH / 2
        textpos = text_to_print.get_rect(centerx=pos[0], centery=pos[1])
        self.window_screen.blit(text_to_print, textpos)
    
    def draw_grid(self):
        for x in range(28):
            pygame.draw.line(
                self.window_screen,
                const.GREY,
                (x * const.WINDOW_SCALE, 0),
                (x * const.WINDOW_SCALE, const.WINDOW_HEIGHT)
                )
        for y in range(36):
            pygame.draw.line(
                self.window_screen,
                const.GREY,
                (0, y * const.WINDOW_SCALE),
                (const.WINDOW_WIDTH, y * const.WINDOW_SCALE)
                )


    def draw_background(self):
        self.window_screen.blit(self.background, (0, const.WINDOW_SCALE * 3))
        pygame.event.pump()

    def draw_wall(self):
        for wall in self.state.walls:
            self.window_screen.blit(
                     self.wall, 
                     (const.WINDOW_SCALE * wall[0],
                     const.WINDOW_SCALE * wall[1])
                    )
        #self.state.olinman.draw(self.window_screen)

    def draw_coins(self):
        for coin in self.state.coins:
            self.window_screen.blit(
                     self.coin,
                     (const.WINDOW_SCALE * coin[0],
                     const.WINDOW_SCALE * coin[1])
                    )

    def draw_object(self, image, spaces):
        for nonmovable_object in spaces:
            print("print coffee")
            self.window_screen.blit(
                     image,
                     (const.WINDOW_SCALE * nonmovable_object[0],
                     const.WINDOW_SCALE * nonmovable_object[1])
                    )

    def draw_play(self):
        self.clear_Screen()
        self.draw_wall()
        self.draw_grid()
        self.draw_coins()
        self.draw_object(self.coffee,self.state.coffees)
        self.draw_txt(f"Score:{state.score}", const.WHITE, [0,9])
        # self.draw_txt(f"Level:{state.level}", const.WHITE, [64,9], False)g
        self.window_screen.blit(self.state.olinsprite.image, ((self.state.olinsprite.rect.x) -4,(self.state.olinsprite.rect.y)-4))
        pygame.draw.rect(
            self.window_screen,
            const.OLIN_BLUE,
            (
                self.state.olinsprite.grid_pos[0] * const.WINDOW_SCALE,
                self.state.olinsprite.grid_pos[1] * const.WINDOW_SCALE,
                const.WINDOW_SCALE,
                const.WINDOW_SCALE,
            ), 2
            )

    def object_image(self, name, x=1, y=1):
        full = os.path.join("images", name)
        obj_image, rect = self.load_image(name)
        if rect.height != const.WINDOW_SCALE and rect.width == rect.height:
            obj_image = pygame.transform.scale(
                obj_image,
                (x*const.WINDOW_SCALE, y*const.WINDOW_SCALE)
                )
        return obj_image

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
        except pygame.error:
            print("Cannot load image:", fullname)
            raise SystemExit
        return image, image.get_rect()


if __name__ == "__main__":

    state = Game_State()
    view = Viewer(state)
    control = Controler(state)

    while state.is_running():
        if state.is_intro():
            control.start_events()
            view.start()
        else:
            if state.coins == []:
                state.setup()
                state.level += 1
            view.draw_play()
            control.events()
            #self.view.clear_Screen()
            state.olinsprite.update()
            #self.olinman.draw(self.view.window_screen)
            pygame.display.update()
            
        view.clock.tick(const.FPS)
    print("Exiting..")
    pygame.quit()
    print("Done")
    sys.exit()