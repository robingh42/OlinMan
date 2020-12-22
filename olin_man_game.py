import pygame
import os
import sys
from pygame.locals import *
import characters
import constants as const
import random
from pathlib import Path
vec = pygame.math.Vector2
pygame.init()


class Game_State:
    """
    The state of the game. Contains all of the sprites and interactable objects

    Attributes:
        view: A (Viewer) allowing the game to display onto the screen
        _running: A (bool) depicting whether the game is running or not
        _ghost_speed: an (int) depicting the number of pixels to move
            the ghosts per frame
        _level: an (int) depicting the current level
        score: an (int) depicting the score the player has earned
        walls: a (list) of all the positions walls exist
        coins: a (list) of all the positions coins exist
        coffees: a (list) of all the positions coffees exist
        olin_man: (OlinMan) a type of Movable player that the user controls
        red_ghost: (OlinMan) a type of Movable player that moves on its own
            and can kill the player
        blue_ghost: (OlinMan) a type of Movable player that moves on its own
            and can kill the player, moves faster than red_ghost
        ghosts:  (pygame.sprite.Group) a group of sprites containing
            all the ghosts
        is_paused: A (bool) depicting whether the game is paused
        clock: a (pygame.Clock) to control the timing of the game
    """
    def __init__(self):
        self.view = Viewer(self)

        self._running = True
        self._ghost_speed = 2
        self._level = 0
        self.score = 0

        # create interactable objects
        self.walls = []
        self.coins = []
        self.coffees = []

        # sprites
        self.olin_man = characters.OlinMan(self, 3)
        self.red_ghost = characters.Ghost(self, vec(14, 14), self._ghost_speed)
        self.blue_ghost = characters.Ghost(
                self,
                vec(13, 14),
                self._ghost_speed + 1,
                vec(-1, 0),
                image="Fright_Ghost.png")
        self.ghosts = pygame.sprite.Group(self.red_ghost, self.blue_ghost)

        # build all the walls, coins, and coffees
        self.setup()

        self.is_paused = False
        self.clock = pygame.time.Clock()

    def setup(self):
        """
        Set up all the walls, coins, coffees and reset the player and ghosts
        """

        # if the game is playing and setup() is called to reset the board
        # start a countdown
        if not self.is_intro():
            view.countdown()
        # if the player is alive, reset the game board and sprites
        if not self.player_is_dead():
            self.make_walls()
            self.make_coins()
            self.make_coffee()
        self.olin_man = characters.OlinMan(self, self.olin_man.lives)
        self.red_ghost.reset((14, 14))
        self.blue_ghost.reset((13, 14), vec(-1, 0))

    def is_intro(self):
        """
        Return whether the player is in the start screen (True)
        """
        return self._level == 0

    def is_running(self):
        """
        Return whether the game is running (True) or is over (False)
        """
        return self._running

    def end_game(self):
        """
        End the game by setting the running state to (False)
        """
        self._running = False

    def is_gameover(self):
        """
        Return whether the player has enough lives to continue (False)
            or has no lives left (True)
        """
        if self.olin_man.lives < 1:
            return True
        else:
            return False

    def player_is_dead(self):
        """
        Return whether the player is dead (True) or alive (False)
        """
        return self.olin_man.dead

    def player_is_vertical(self):
        """
        Return whether the player is moving verticaly (True)
            or horizontaly (False)
        """
        return self.olin_man.direction in [vec(0, 1), vec(0, -1)]

    def get_level(self):
        """
        return the current level (int) of the game
        """
        return self._level

    def pause(self):
        """
        Changes the game state to be paused, or unpauses the game
        """
        # change the pause game state
        self.is_paused = not self.is_paused

    def check_quarter_second(self):
        """
        Check if a quarter second has passed.

        Return (True) if a quarter second has passed,
            (False) if a half second has passed
        """
        if pygame.time.get_ticks() % 500 > 250:
            return True
        else:
            return False

    def make_walls(self):
        """
        Adds the position of walls from the map to self.walls
        """
        for row in range(len(const.MAP)):
            for col in range(len(const.MAP[row])):
                # check if the position is a wall or ghost wall
                if const.MAP[row][col] == 1 or const.MAP[row][col] == 2:
                    self.walls.append(vec(col, (row + 3)))

    def make_coins(self):
        """
        Adds the position of coins from the map to self.coins
        """
        for row in range(len(const.MAP)):
            for col in range(len(const.MAP[row])):
                if const.MAP[row][col] == 4:
                    self.coins.append(vec(col, (row + 3)))

    def make_coffee(self):
        """
        Adds the position of coffees from the map to self.coffees
        """
        for row in range(len(const.MAP)):
            for col in range(len(const.MAP[row])):
                if const.MAP[row][col] == 3:
                    self.coffees.append(vec(col, (row + 3)))

    def check_colide(self):
        """
        Check if OlinMan has ran into a ghost and calls OlinMan's collision()

        Return (True) if there is a colision
        """

        # finds all the ghosts coliding with Olin man
        ghost = pygame.sprite.spritecollide(self.olin_man, self.ghosts, False)
        # If a ghost did colide, call OlinMan's collision()
        if ghost != []:
            print("***You hit a Ghost***")
            self.olin_man.collision()
            return True
        else:
            return False

    def update_highscore(self):
        """
        Check if the highscore was beat and saves the highscore to a file

        Return (True) if the highscore was beat
        """
        if self.get_highscore() < self.score:
            self.save_highscore(self.score)
            print("You beat the highscore!")
            return True
        return False

    @staticmethod
    def save_highscore(score):
        """
        Saves the highscore to a file

        Args:
            score: (int) the highest score achieved

        Return (True) if the file is created/updated
        """
        # Open a file in the directory linkdata with the file name "title"
        # and save all the links in the file
        with open("highscore.txt", "w") as file:
            file.write(f"{score}")
            return True
        return False

    @staticmethod
    def get_highscore():
        """
        Check if the file exists and return the highscore
        Return a highscore (int)
        """
        if not Path("highscore.txt").is_file():
            return 0
        with open("highscore.txt", "r") as file:
            read_data = file.read()
        return int(read_data)


class Controler:
    """
    Controls the game by checking user inputs and modifying the game state

    Attributes:
        state: a (GameState) to access the conditions of the board
    """
    def __init__(self, game):
        """
        Creates a Controler instance

        args:
            state: a (GameState) to access the conditions of the board
        """
        self.state = game

    def start_events(self):
        """
        Check keypresses during the start of the game
        """
        for event in pygame.event.get():
            # if the window was closed, end the game
            if event.type == pygame.QUIT:
                self.state.end_game()
                print("Exiting..")
                pygame.quit()
                print("Done")
                sys.exit()
            # if the user pressed space increase the level and start the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state._level += 1
                print("Level:", self.state.get_level())

    def pause_events(self):
        """
        Check keypresses during the pause menu
        """
        for event in pygame.event.get():
            # if the window was closed, end the game
            if event.type == pygame.QUIT:
                self.state.end_game()
                print("Checking highscore")
                state.update_highscore()
                print("Exiting..")
                pygame.quit()
                print("Done")
                sys.exit()
            # if the user pressed [space], [p], or [esc] resume the game
            if (
                event.type == pygame.KEYDOWN and
                (event.key == pygame.K_p or event.key == pygame.K_ESCAPE or
                 event.key == pygame.K_SPACE)
                    ):
                self.state.pause()
                print("Resuming game...")

    def events(self):
        """
        Check keypresses during the main game
        """
        for event in pygame.event.get():
            # if the window was closed, end the game
            if event.type == pygame.QUIT:
                self.state._running = False
            # if the user pressed [space], [p], or [esc] pause the game
            elif (
                  event.type == pygame.KEYDOWN and
                  (event.key == pygame.K_p or
                   event.key == pygame.K_ESCAPE or
                   event.key == pygame.K_SPACE)
                    ):
                self.state.pause()
                print("Paused")
            # if the user pressed up, down, left, or right
            # change OlinMan's direction
            elif event.type == KEYDOWN or event.type == KEYUP:
                if event.key == K_w or event.key == K_UP:
                    self.state.olin_man.move("up")
                elif event.key == K_s or event.key == K_DOWN:
                    self.state.olin_man.move("down")
                elif event.key == K_a or event.key == K_LEFT:
                    self.state.olin_man.move("left")
                elif event.key == K_d or event.key == K_RIGHT:
                    self.state.olin_man.move("right")
                self.state.olin_man.update()


class Viewer:
    """
    Creates the screen and displays the game to the screen.

    Attributes:
        state: a (GameState) for checking conditions of the board
        _text_size: An (int) depicting the size of text in pixels
        _font: a (pygame.font.Font) object controling the games font
        window_screen: a (pygame.display) window to display everything on
        background: a (pygame.image) of the original PacMan map
        wall: a (pygame.image) of the wall blocks
        coin: a (pygame.image) of a coin
        post_it: a (pygame.image) of stack of post-it notes
        coffee: a (pygame.image) of an Acronym Coffee
        heart: a (pygame.image) of the heart of OlinMan
    """

    def __init__(self, game):
        """
        Creates a Viewer instance

        args:
            state: a (GameState) to access the conditions of the board
        """
        self.state = game

        # set up the font
        self._text_size = 16
        self._font = pygame.font.Font(
            "PressStart2P-Regular.ttf",
            self._text_size
            )

        # setup the basic window
        self.window_screen = pygame.display.set_mode(
            (const.WINDOW_WIDTH, const.WINDOW_HEIGHT)
            )
        self.window_screen.fill(const.BLACK)

        # load all the images from local files
        self.background = self.object_image("Maze.jpeg", x=28, y=31)
        self.wall = self.object_image("Wall.png")
        self.coin = self.object_image("Coin.png")
        self.post_it = self.object_image("Post_Its2.png")
        self.coffee = self.object_image("Coffee.png", 1.25, 1.25)
        self.heart = self.object_image("Life.png", 2, 2)

    def draw_sprites(self):
        """
        Draws all the sprites to the window

        Causes OlinMan to "bounce" based on his movement
        """
        # every quarter second change whether Olin man is bouncing or not
        if state.check_quarter_second():
            self.window_screen.blit(
                self.state.olin_man.image,
                (self.state.olin_man.rect.x - 4,
                 self.state.olin_man.rect.y - 4))
        else:
            # if olinman is moving verticaly, make him squeeze horizontaly
            if self.state.player_is_vertical():
                self.window_screen.blit(
                    self.state.olin_man.image3,
                    (self.state.olin_man.rect.x - 4,
                     self.state.olin_man.rect.y - 4))
            # if olinman is moving horizontaly, make him bounce verticaly
            else:
                self.window_screen.blit(
                    self.state.olin_man.image2,
                    (self.state.olin_man.rect.x - 4,
                     self.state.olin_man.rect.y - 4))

        # draw all the ghosts
        for ghost in self.state.ghosts:
            self.window_screen.blit(
                ghost.image,
                (ghost.rect.x - 4, ghost.rect.y - 4))

    def clear_Screen(self):
        """
        Fills the screen with black, erasing all the pixels currently displayed
        """
        self.window_screen.fill(const.BLACK)

    def start(self):
        """
        Display the start screen
        """
        self.draw_txt(
            "HIGH SCORE",
            const.WHITE,
            [0, 0 + 9]
            )
        # Read the highscore from a file, and display it
        self.draw_txt(
            f"{self.state.get_highscore()}",
            const.WHITE,
            [0, 9 + 16]
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
        self.draw_txt(
            "Created by",
            const.WHITE,
            [0, const.WINDOW_HEIGHT - 40]
            )
        self.draw_txt(
            "Robin Graham-Hayes",
            const.WHITE,
            [0, const.WINDOW_HEIGHT - 16]
            )

        pygame.display.update()
        self.state.clock.tick(const.FPS)

    def draw_txt(self, text, RGB_color, pos, center=True, title=False):
        """
        Draws text to the screen using the games font

        args:
            text: A (string) to print to the screen
            RGB_color: a (tuple) of three numbers depicting the RGB color
            pos: a (list) of ints to place the text, counted in pixels
            center: a (bool) depicting whether or not to center
                the text horizontaly
            title: a (bool) depicting whether or not to double the text size
        """
        text_to_print = self._font.render(text, False, RGB_color)
        # if title is True, make the text twice the normal size
        if title:
            font = pygame.font.Font(
                "PressStart2P-Regular.ttf",
                self._text_size * 2
                )
            text_to_print = font.render(text, False, RGB_color)
        # center the text horizontaly
        if center:
            pos[0] = const.WINDOW_WIDTH / 2
        # print the text to the screen
        textpos = text_to_print.get_rect(centerx=pos[0], centery=pos[1])
        self.window_screen.blit(text_to_print, textpos)

    def draw_grid(self):
        """
        Draws the grid to the screen
        """
        # draw vertical lines
        for x in range(28):
            pygame.draw.line(
                self.window_screen,
                const.GREY,
                (x * const.WINDOW_SCALE, 0),
                (x * const.WINDOW_SCALE, const.WINDOW_HEIGHT)
                )
        # draw horizontal lines
        for y in range(36):
            pygame.draw.line(
                self.window_screen,
                const.GREY,
                (0, y * const.WINDOW_SCALE),
                (const.WINDOW_WIDTH, y * const.WINDOW_SCALE)
                )

    def draw_background(self):
        """
        Draws the PacMan maze to the screen
        """
        self.window_screen.blit(self.background, (0, const.WINDOW_SCALE * 3))
        pygame.event.pump()

    def draw_object(self, image, spaces):
        """
        Draws all instances of a interactable object to the screen

        args:
            image: a file name (string) to get the image from
            spaces: a (list) of all the grid positions to place the object
        """
        # draw each interactable object to the screen
        for nonmovable_object in spaces:
            self.window_screen.blit(
                image,
                (const.WINDOW_SCALE * nonmovable_object[0],
                 const.WINDOW_SCALE * nonmovable_object[1])
                )

    def draw_lives(self):
        """
        Draws all lives to the screen. Changes based on number of lives left.

        Allows for more than the basic three lives
        """
        for life in range(self.state.olin_man.lives):
            self.window_screen.blit(
                self.heart,
                (const.WINDOW_SCALE * (2 + 2.5 * life),
                 const.WINDOW_SCALE * 34)
                )

    def draw_play(self):
        """
        Update the screen. Clears the screen and then draws all
            the objects and sprites to the screen
        """
        self.clear_Screen()
        self.draw_object(self.wall, self.state.walls)
        # draw coins or post-its depending on the level
        if state.get_level() % 2 == 1:
            self.draw_object(self.post_it, self.state.coins)
        else:
            self.draw_object(self.coin, self.state.coins)
        self.draw_object(self.coffee, self.state.coffees)
        self.draw_txt(f"Score:{state.score}", const.WHITE, [0, 9])
        self.draw_lives()
        self.draw_sprites()

    def countdown(self):
        """
        Draws a count down, waiting the apropriate amount of time between
            numbers

        The game is esentialy paused during the countdown
        """
        for count in ["Three", "Two", "One"]:
            self.draw_play()
            self.draw_txt(
                count,
                const.WHITE,
                [0, const.WINDOW_HEIGHT/2],
                title=True)
            pygame.display.update()
            pygame.time.wait(1000)

    def pause(self):
        """
        Displays the pause screen
        """
        self.draw_txt(
            "Paused",
            const.START_ORANGE,
            [0, const.WINDOW_HEIGHT/2],
            title=True)
        pygame.display.update()

    def you_died(self):
        """
        Displays the player death screen
        """
        self.draw_txt(
            "You Died",
            const.RED,
            [0, const.WINDOW_HEIGHT/2],
            title=True)
        pygame.display.update()
        pygame.time.wait(1000)

    def game_over(self):
        """
        Displays the game over screen
        """
        self.draw_txt(
            "GAME OVER",
            const.RED,
            [0, const.WINDOW_HEIGHT/2],
            title=True)
        pygame.display.update()

    @staticmethod
    def object_image(name, x=1, y=1):
        """
        Return a (pygame.image) for the game objects

        args:
            name: a file name (string) to find the image to load
            x: a (float) to scale the image width by (based on the grid scale)
            y: a (float) to scale the image height by (based on the grid scale)
        """
        obj_image = Viewer.load_image(name)[0]
        obj_image = pygame.transform.scale(
            obj_image,
            (int(x*const.WINDOW_SCALE), int(y*const.WINDOW_SCALE))
            )
        return obj_image

    @staticmethod
    def load_image(name):
        """
        Loads an image and return:
            the image (pygame.image), the image's rect (pygame.rect)

        args:
            name: a file name (string) to find the image to load
        """
        fullname = os.path.join("images", name)

        image = pygame.image.load(fullname)

        # Check if the image has transparency and maintains it
        # Converts the image to maintain color format
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()

        return image, image.get_rect()


if __name__ == "__main__":
    """
    Runs the game
    """
    # Create the state, viewer, and controler
    state = Game_State()
    view = Viewer(state)
    control = Controler(state)

    # while the game is running
    while state.is_running():
        # if the game is in the intro state runn all the start screen functions
        if state.is_intro():
            control.start_events()
            view.start()
        else:
            # if the coins all all collected, reset the board and add a level
            if state.coins == []:
                state.setup()
                state._level += 1
            # if the game is over, display the end screen and close the game
            elif state.is_gameover():
                view.game_over()
                pygame.time.wait(3000)
                state.end_game()
            # If the player died, print the death screen and reset the screen
            elif state.player_is_dead():
                view.you_died()
                state.setup()
            # check if the game is paused and wait until it is unpaused
            elif state.is_paused:
                view.pause()
                while state.is_paused:
                    control.pause_events()
                view.countdown()
            # check if the player collided with ghosts
            state.check_colide()
            # draw the board
            view.draw_play()
            # check key presses
            control.events()
            # update OlinMan and the ghosts
            state.olin_man.update()
            state.ghosts.update()
            # update the display
            pygame.display.update()
            # make sure the FPS is capped
            state.clock.tick(const.FPS)
    # when the game is over check the highscore and update it
    print("Checking highscore")
    state.update_highscore()
    # completly close the game
    print("Exiting..")
    pygame.quit()
    print("Done")
    sys.exit()
