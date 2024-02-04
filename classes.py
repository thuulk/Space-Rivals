# Module created to define and store classes of Space_Heroic source code

from pygame import mixer
from pathlib import Path
import pygame
import random
import json


pygame.mixer.init()
pygame.init()


class MovableObject:

    # Function that initializes the attributes of this class.
    def __init__(self, quantity, position_x_parameter, position_y_parameter,
                 position_x_change_parameter, position_y_change_parameter, image_path_parameter):

        # Quantity of objects.
        self.quantity = quantity

        # Image.
        self.image_path = []

        # Initial X position.
        self.position_x = []

        # Initial Y position.
        self.position_y = []

        # Attribute that will indicate the change in the X position.
        self.position_x_change = []

        # This attribute determines how many pixels the position will change in the Y axis.
        self.position_y_change = []

        # Loop that will convert every parameter given into the instance in a class attribute.
        for iteration in range(self.quantity):

            self.image_path.append(image_path_parameter)
            self.position_x_change.append(position_x_change_parameter)
            self.position_y_change.append(position_y_change_parameter)

            """
            As "enemies" instance have 9 enemies in different X and Y coordinates.
            We need to iterate in a loop the X and Y coordinates of each enemy, while giving the attributes; 
            therefore, that would make position X and Y parameters lists, and we can't append lists into lists.
            So, both logic blocks below check if the coordinate parameter given is a list;
            if it is, the random coordinates generated in one iteration are the ones 
            that will be added in the correspondent enemy initialization iteration for assigning attributes.
            """

            if isinstance(position_x_parameter, list):
                self.position_x.append(position_x_parameter[iteration])

            else:
                self.position_x.append(position_x_parameter)

            if isinstance(position_x_parameter, list):
                self.position_y.append(position_y_parameter[iteration])

            else:
                self.position_y.append(position_y_parameter)

    # Function that updates the coordinates of the object in the X axis.
    def update_position(self, iteration, path):

        if isinstance(path, list):
            self.position_x[iteration] += self.position_x_change[iteration]
            self.position_y[iteration] += self.position_y_change[iteration]
            game.screen.blit(path[iteration], (self.position_x[iteration], self.position_y[iteration]))

        else:
            self.position_x[iteration] += self.position_x_change[iteration]
            self.position_y[iteration] += self.position_y_change[iteration]
            game.screen.blit(path, (self.position_x[iteration], self.position_y[iteration]))

    # Function that moves the ship to the right by 1.8 pixels.
    def move_to_right(self, iteration, change):

        # Updating the attribute used to change the X position for the value of the parameter given.
        self.position_x_change[iteration] = change

    # Function that moves the ship to the left by 2 pixels.
    def move_to_left(self, iteration, change):

        # Updating the attribute used to change the X position for the value of the parameter given.
        self.position_x_change[iteration] = change

    '''def regenerate_object(self, iteration, position_x, position_y):
        self.position_x[iteration] = position_x
        self.position_y[iteration] = position_y
        '''
    # Function that give a new random coordinates to the enemy within the given parameters below.
    def regenerate_object(self, iteration, first_y_coordinate_range, second_y_coordinate_range, random, position_x=0,
                          position_y=0, maximum_score=0, infinite=False, minimum_score=0):

        if infinite:

            if game.score > maximum_score:
                self.position_x[iteration] = random.randint(0, 736)
                self.position_y[iteration] = random.randint(first_y_coordinate_range, second_y_coordinate_range)

        elif random and minimum_score == 0 and maximum_score == 0:
            self.position_x[iteration] = random.randint(0, 736)
            self.position_y[iteration] = random.randint(first_y_coordinate_range, second_y_coordinate_range)

        elif not random and minimum_score == 0 and maximum_score == 0:
            self.position_x[iteration] = position_x
            self.position_y[iteration] = position_y

        else:
            if minimum_score <= game.score <= maximum_score:
                self.position_x[iteration] = random.randint(0, 736)
                self.position_y[iteration] = random.randint(first_y_coordinate_range, second_y_coordinate_range)


class Timer:

    # Function that initializes the attributes of this class.
    def __init__(self):

        pygame.font.init()

        # Storing the values the ticks of the cronometer.
        self.clock = pygame.time.Clock()

        # Variable that will be used for the count the seconds in the self.clock attribute.
        self.seconds = 0

        pygame.time.set_timer(pygame.USEREVENT, 1)

    # Function that resets the timer.
    def reset(self):

        self.seconds = 0

    # function that updates the timer by .001 second.
    def update_time(self):

        self.seconds += 0.001


class Menu:

    def __init__(self, execute, title_font, color, option_color):

        # Bool that will determine if the game will keep running
        self.screen = pygame.display.set_mode((800, 600))

        # Screen background.
        self.background = pygame.image.load('fondo.png')

        # Bool that will determine if the menu will keep running
        self.execute = execute

        # Font
        self.title_font = title_font
        self.option_font = pygame.font.Font('advanced_pixel_lcd-7.ttf', 20)

        # Font color
        self.default_color = color
        self.play_color = option_color
        self.exit_color = color
        self.try_again = color

    def display_text(self, font, message, position_x, position_y, color):
        text = font.render(message, True, color)
        game.screen.blit(text, (position_x, position_y))


class Player(MovableObject):

    # Function that initializes the attributes of this class.
    def __init__(self, quantity, initial_position_x, initial_position_y, position_x_change, position_y_change, image):

        """
        super(). calls a function from the parent class, in this case "__init__". So, what function __init__
        from player class does, is call the function __init__ from its parent class. Summarizing, __init__
        function from player class is the same as the parent __init__ function.
        """
        super().__init__(quantity, initial_position_x, initial_position_y, position_x_change, position_y_change, image)

        self.frame02 = pygame.image.load('sprites_player1.png')
        self.death_sound = mixer.Sound('death_sound_effect.mp3')
        self.death_sound.set_volume(0.7)

    def stand_by(self, iteration):

        # Updating the attribute to NOT change the X position of the player.
        self.position_x_change[iteration] = 0

    # Function that limits player movement within the screen limitations
    def stop_player_right(self, iteration):

        # Setting the limit for the player in the screen on the right side.
        self.position_x[iteration] = 734

    # Function that limits player movement within the screen limitations
    def stop_player_left(self, iteration):

        # Setting the limit for the player in the screen on the left side.
        self.position_x[iteration] = 0


class Enemy(MovableObject):

    # Function that initializes the attributes of this class.
    def __init__(self, quantity, initial_position_x, initial_position_y, position_x_change, position_y_change, image):
        super().__init__(quantity, initial_position_x, initial_position_y, position_x_change, position_y_change, image)

    ''' "enemy" is a parameter you'll see often when I'm dealing with enemies functions, it is just
    the parameter I assign when working with an instance of Enemy class'''
    # Function that updates the current Y axis coordinates by 0.3 pixels every time it is called.
    def move_down(self, enemy):
        self.position_y[enemy] += self.position_y_change[enemy]

    # Function that give a new random coordinates to the enemy within the given parameters below.
    def regenerate_object(self, iteration, first_y_coordinate_range, second_y_coordinate_range, maximum_score=0,
                          infinite=False, minimum_score=0):

        if infinite:

            if game.score > maximum_score:
                self.position_x[iteration] = random.randint(0, 736)
                self.position_y[iteration] = random.randint(first_y_coordinate_range, second_y_coordinate_range)

        elif minimum_score == 0 and maximum_score == 0:
            self.position_x[iteration] = random.randint(0, 736)
            self.position_y[iteration] = random.randint(first_y_coordinate_range, second_y_coordinate_range)

        else:
            if minimum_score <= game.score <= maximum_score:
                self.position_x[iteration] = random.randint(0, 736)
                self.position_y[iteration] = random.randint(first_y_coordinate_range, second_y_coordinate_range)


class Bullet(MovableObject):

    # Function that initializes the attributes of this class.
    def __init__(self, quantity, initial_position_x, initial_position_y,
                 position_x_change, position_y_change, visible, image):
        super().__init__(quantity, initial_position_x, initial_position_y, position_x_change, position_y_change, image)

        # This attribute determines if the bullet is visible or not.
        self.visible = []

        # Attribute that stores shooting sound.
        self.sound = mixer.Sound('blaster.mp3')

        for iteration in range(self.quantity):

            if isinstance(visible, list):
                self.visible.append(visible[iteration])

            else:
                self.visible.append(visible)

    # Function that force the object to follow the player in the X axis.
    def follow_ship(self, iteration, position_x_change, position_y_change):

        # This line update the value of the bullet at the same position of the ship in the X axis.
        """Remember that the index [-1], calls the last element in the list"""
        self.position_x[iteration] = player.position_x[-1] + position_x_change

        # This line update the value of the bullet at the same position of the ship in the Y axis.
        self.position_y[iteration] = 518
        self.position_y_change[iteration] = position_y_change

    # Function that updates the change in the Y axis of the bullet by -30 pixels
    def shoot(self, iteration, new_change_in_y):

        self.position_y_change[iteration] = new_change_in_y


class Meteor(Bullet):

    def __init__(self, quantity, initial_position_x, initial_position_y, position_x_change, position_y_change, visible,
                 image, visible01):

        super().__init__(quantity, initial_position_x, initial_position_y, position_x_change, position_y_change,
                         visible, image)

        self.visible01 = visible01


class DestructionSprites(Bullet):

    # Function that initializes the attributes of this class.
    def __init__(self, quantity, initial_position_x, initial_position_y, position_x_change,
                 position_y_change, visible, frame01, frame02, frame03, frame04):

        super().__init__(quantity, initial_position_x, initial_position_y, position_x_change, position_y_change,
                         visible, frame01)

        self.frame02 = frame02
        self.frame03 = frame03
        self.frame04 = frame04


class Game(Menu):

    # Function that initializes the attributes of this class.
    def __init__(self, execute, font, color, option_color):

        super().__init__(execute, font,  color, option_color)

        # Game icon.
        self.icon = pygame.image.load('missile.png')

        # Attribute that will determine if what section of the game will run.
        self.over = False
        self.reset = True

        # Destruction sound of enemy ships.
        self.destruction_sound = mixer.Sound('destruccion.mp3.mp3')
        self.destruction_sound.set_volume(0.8)

        # Storing the size and font of different texts displayed.
        self.score_font = pygame.font.Font('advanced_pixel_lcd-7.ttf', 20)

        # Destruction sprite.
        self.destruction_sprite = DestructionSprites(1, 0, 514, 0,
                                                     0, False,
                                                     pygame.image.load('destruction_sprites01.png'),
                                                     pygame.image.load('destruction_sprites02.png'),
                                                     pygame.image.load('destruction_sprites03.png'),
                                                     pygame.image.load('destruction_sprites04.png'))

        self.menu = Menu(True, pygame.font.Font('advanced_pixel_lcd-7.ttf', 40),
                         (255, 255, 255), (87, 35, 100))

        # Score attributes.
        self.score_path = Path('best_score.json')
        self.best_score = 0
        self.score = 0

    # Function that displays the current player's score.
    def show_score(self):

        text = self.score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        if self.score_path.exists():

            game.screen.blit(text, (10, 50))

        else:

            game.screen.blit(text, (10, 10))

    # Function that displays the player best score in any game.
    def show_best_score(self):

        if self.score_path.exists():
            contents = self.score_path.read_text()
            self.best_score = json.loads(contents)
            text = self.score_font.render(f"Best score: {self.best_score}", True, (255, 255, 255))
            game.screen.blit(text, (10, 10))

    # Function that updates the new player's best score.
    def new_best_score(self):

        if self.score > self.best_score:
            contents = json.dumps(self.score)
            self.score_path.write_text(contents)

    # Function that updates the current player's score every time he kills an enemy.
    def update_score(self):

        self.score += 10

    # Function that displays the game over text.
    def game_over_text(self, font, message, position_x, position_y, color):
        super().display_text(font, message, position_x, position_y, color)


game = Game(True, pygame.font.Font('advanced_pixel_lcd-7.ttf', 40), (255, 255, 255),
            (87, 35, 100))

player = Player(1, 368, 518, 0, 0,
                pygame.image.load('sprites_player0.png'))


enemies = Enemy(7, [random.randint(0, 736) for enemy in range(7)],
                [random.randint(0, 200) for enemy in range(7)], 0.26, 0.048,
                pygame.image.load('space-ship.png'))

meteors = Meteor(2, [random.randint(0, 736) for asteroid in range(2)],
                 [random.randint(-256, -128) for asteroid in range(2)], 0, 0, False,
                 pygame.image.load('asteroide_128_X_128.png'), False)

bullet = Bullet(1,
                0, 518, 0,
                0, False, pygame.image.load('laser_player.png'))

timer = Timer()
