import pygame
import os
import sys
from pygame.locals import *
import characters
import constants as const
import random
vec = pygame.math.Vector2
pygame.init()




class Game_State:
    """
    The state of the game
    """
    def __init__(self):
        self.view = Viewer(self)
        self.inputs = Controler(self)

        self.running = True
        self._start_screen = True

        self.level = 0
        self.score = 0
        self.walls = []
        self.coins = []
        self.coffees = []
        self.olinsprite = characters.OlinMan(self, 3)
        self.olinman = pygame.sprite.GroupSingle(self.olinsprite)
        self.red_ghost = characters.Ghost(self, [13.5,14], 2)
        self.ghosts = pygame.sprite.Group(self.red_ghost)
        self.setup()
        self.is_paused = False

    def is_intro(self):
        return self.level == 0

    def isrunning(self):
        return self.running

    def pause(self):
        self.is_paused = not self.is_paused

    def setup(self):
        self.olinsprite = characters.OlinMan(self, self.olinsprite.lives)
        self.olinman = pygame.sprite.GroupSingle(self.olinsprite)
        self.red_ghost = characters.Ghost(self, [13.5,14], 2)
        self.ghosts = pygame.sprite.Group(self.red_ghost)
        self.make_walls()
        self.make_coins()
        self.make_coffee()

    def make_walls(self):
        for row in range(len(const.MAP)):
            for col in range(len(const.MAP[row])):
                if const.MAP[row][col] == 1 or const.MAP[row][col] == 2:
                    self.walls.append(vec(col,(row + 3)))

    def make_coins(self):
        for row in range(len(const.MAP)):
            for col in range(len(const.MAP[row])):
                if const.MAP[row][col] == 4:
                    self.coins.append(vec(col,(row + 3)))

    def make_coffee(self):
        for row in range(len(const.MAP)):
            for col in range(len(const.MAP[row])):
                if const.MAP[row][col] == 3:
                    self.coffees.append(vec(col,(row + 3)))

    def player_is_dead(self):
        return self.olinsprite.dead

    def check_colide(self):
        ghost = pygame.sprite.spritecollide(self.olinsprite, self.ghosts, False)
        if ghost != []:
            print("****colision****")
            self.olinsprite.collision(ghost[0])


class Controler:
    """
    Controls the game
    """
    # uses pygame.event to check key presses
    # runs the menu selection
    def __init__(self, game):
        self.state = game

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False
                print("Exiting..")
                pygame.quit()
                print("Done")
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state.level += 1
                print("level:",self.state.level)
    
    def pause_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False
                print("Exiting..")
                pygame.quit()
                print("Done")
                sys.exit()
            if (event.type == pygame.KEYDOWN and
                (event.key == pygame.K_p or event.key == pygame.K_ESCAPE)):
                self.state.pause()
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.running = False
                print("Exiting..")
                pygame.quit()
                print("Done")
                sys.exit()
            elif (event.type == pygame.KEYDOWN and
                (event.key == pygame.K_p or event.key == pygame.K_ESCAPE)):
                self.state.pause()
                print("paused")
                print(state.is_paused)
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
            


class Viewer:
    """
    Displays the game
    """

    def __init__(self, game_state):
        # some pygame stuff
        # sets up a pygame display
        
        self.state = game_state

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

        self.background = self.object_image("Maze.jpeg", x=28, y=31)
        self.wall = self.object_image("Wall.png")
        self.coin = self.object_image("Coin.png")
        self.post_it = self.object_image("Post_Its.png")
        self.coffee = self.object_image("Coffee.png",1.25,1.25)

    def update_sprites(self):
        # Moves on screen sprite based on kep presses, or move methods
        self.window_screen.blit(
            self.state.olinsprite.image,
            (self.state.olinsprite.rect.x - 4, self.state.olinsprite.rect.y -4))
        self.window_screen.blit(
            self.state.red_ghost.image,
            (self.state.red_ghost.rect.x - 4, self.state.red_ghost.rect.y - 4))
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

    def draw_coins(self):
        for coin in self.state.coins:
            self.window_screen.blit(
                     self.post_it,
                     (const.WINDOW_SCALE * coin[0],
                     const.WINDOW_SCALE * coin[1])
                    )

    def draw_object(self, image, spaces):
        for nonmovable_object in spaces:
            #print("print coffee")
            self.window_screen.blit(
                     image,
                     (const.WINDOW_SCALE * nonmovable_object[0],
                     const.WINDOW_SCALE * nonmovable_object[1])
                    )

    def draw_play(self):
        self.clear_Screen()
        #self.draw_wall()
        #self.draw_background()
        # self.draw_grid()
        #self.draw_coins()
        self.draw_object(self.wall, self.state.walls)
        self.draw_object(self.coin, self.state.coins)
        self.draw_object(self.coffee, self.state.coffees)
        self.draw_txt(f"Score:{state.score}", const.WHITE, [0,9])
        # self.draw_txt(f"Level:{state.level}", const.WHITE, [64,9], False)g
        self.update_sprites()
    
    def pause(self):
        self.draw_txt(
            "Paused",
            const.START_ORANGE,
            [0, const.WINDOW_HEIGHT/2],
            title=True)
        pygame.display.update()

    def game_over(self):
        self.draw_txt(
            "GAME OVER",
            const.RED,
            [0, const.WINDOW_HEIGHT/2],
            title=True)

    def object_image(self, name, x=1, y=1):
        obj_image = self.load_image(name)[0]
        if x != const.WINDOW_SCALE and y != const.WINDOW_SCALE:
            print(name)
            obj_image = pygame.transform.scale(
                obj_image,
                (int(x*const.WINDOW_SCALE), int(y*const.WINDOW_SCALE))
                )
        return obj_image

    @staticmethod
    def load_image(name):
        """ Load image and return image object"""
        fullname = os.path.join("images", name)
        
        image = pygame.image.load(fullname)

        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        
        return image, image.get_rect()


if __name__ == "__main__":

    state = Game_State()
    view = Viewer(state)
    control = Controler(state)

    while state.isrunning():
        if state.is_intro():
            control.start_events()
            view.start()
        else:
            if state.coins == []:
                state.setup()
                state.level += 1
            elif state.player_is_dead():
                state.setup()
            elif state.is_paused:
                view.pause()
                while state.is_paused:
                    control.pause_events()
            state.check_colide()
            view.draw_play()
            control.events()
            #self.view.clear_Screen()
            state.olinsprite.update()
            state.ghosts.update()
            #self.olinman.draw(self.view.window_screen)
            pygame.display.update()
            
        view.clock.tick(const.FPS)
    print("Exiting..")
    pygame.quit()
    print("Done")
    sys.exit()