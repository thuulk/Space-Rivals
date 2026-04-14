# Module created to define and store the triple shot mechanic of Space Rivals
#   left    : 115° (upper-left diagonal)
#   center  : 90°  (straight up)
#   right   : 65°  (upper-right diagonal)

from classes import Bullet, game, player, enemies, bullet, base_dir
from power_up import spawn_power_up
from speed_power_up import spawn_speed_power_up
import pygame
import math
import os


# Speed of the triple shot bullets.
_SPEED = 18

# Horizontal speed component based on a 65-degree firing angle.
_VX = _SPEED * math.cos(math.radians(65))

# Vertical speed component based on a 65-degree firing angle.
_VY = _SPEED * math.sin(math.radians(65))


class TripleShot(Bullet):

    # Function that initializes the attributes of this class.
    def __init__(self, quantity, initial_position_x, initial_position_y,
                 position_x_change, position_y_change, visible, image):

        super().__init__(quantity, initial_position_x, initial_position_y,
                         position_x_change, position_y_change, visible, image)

    # Function that checks if all three bullets are available to fire.
    def ready(self):

        return not (self.visible[0] or self.visible[1] or self.visible[2])

    # Function that fires all three bullets from the player's current position.
    def fire(self):

        # Aligning the bullets to the center of the ship.
        px = player.position_x[0] + 15
        py = player.position_y[0]

        # Setting the position and velocity for the left bullet (115-degree angle).
        self.position_x[0] = px
        self.position_y[0] = py
        self.position_x_change[0] = -_VX
        self.position_y_change[0] = -_VY
        self.visible[0] = True

        # Setting the position and velocity for the center bullet (straight up).
        self.position_x[1] = px
        self.position_y[1] = py
        self.position_x_change[1] = 0
        self.position_y_change[1] = -_SPEED
        self.visible[1] = True

        # Setting the position and velocity for the right bullet (65-degree angle).
        self.position_x[2] = px
        self.position_y[2] = py
        self.position_x_change[2] = _VX
        self.position_y_change[2] = -_VY
        self.visible[2] = True

        # Playing the shoot sound.
        bullet.sound.play()

    # Function that resets a bullet to its inactive state.
    def reset_bullet(self, iteration):

        self.visible[iteration] = False
        self.position_x_change[iteration] = 0
        self.position_y_change[iteration] = 0

    # Function that updates the triple shot bullets each frame: moves, draws, checks collisions, and resets.
    def update(self):

        for iteration in range(self.quantity):

            # If the bullet is not visible, skip to the next one.
            if not self.visible[iteration]:
                continue

            # Updating the bullet's position on screen.
            self.update_position(iteration, self.image_path)

            # If the bullet goes off screen (top, left, or right), reset it.
            if self.position_y[iteration] <= -64 or self.position_x[iteration] < -64 or self.position_x[iteration] > 864:
                self.reset_bullet(iteration)
                continue

            # Checking collisions between this bullet and every enemy.
            for enemy in range(enemies.quantity):

                # Calculating the distance between the bullet and the enemy.
                collision = math.sqrt(
                    math.pow(self.position_x[iteration] - enemies.position_x[enemy], 2) +
                    math.pow(self.position_y[iteration] - enemies.position_y[enemy], 2))

                # If there is a collision, the next block will be executed.
                if collision < 28:

                    # Resetting the destruction sound.
                    game.destruction_sound.stop()

                    # Playing the destruction sound.
                    game.destruction_sound.play()

                    # Updating the player's score.
                    game.update_score()

                    # Chance to drop a power-up at the enemy's position.
                    spawn_power_up(enemies.position_x[enemy], enemies.position_y[enemy])

                    # Chance to drop a speed power-up at the enemy's position.
                    spawn_speed_power_up(enemies.position_x[enemy], enemies.position_y[enemy])

                    # Difficulty curve (same as regular bullet).
                    enemies.respawn(enemy, 0, 200, 2500, False, 0)
                    enemies.respawn(enemy, 0, 225, 3000, False, 2500)
                    enemies.respawn(enemy, 0, 250, 3500, False, 3000)
                    enemies.respawn(enemy, 0, 275, 4000, False, 3500)
                    enemies.respawn(enemy, 0, 300, 4500, True)

                    # Resetting the bullet.
                    self.reset_bullet(iteration)
                    break


    # Function that resets all triple shot bullets to their inactive state (used when restarting the game).
    def reset(self):
        for iteration in range(self.quantity):
            self.reset_bullet(iteration)


# Creating the triple shot instance with 3 bullets: left (index 0), center (index 1), and right (index 2).
triple_shot = TripleShot(3,
                         0, 518, 0, 0,
                         [False, False, False],
                         pygame.image.load(os.path.join(base_dir, '../images/triple_bala.png')))


# Module-level functions that delegate to the triple_shot instance.
# These are imported by functions.py.

def triple_ready():
    return triple_shot.ready()

def triple_fire():
    triple_shot.fire()

def update_triple_shot():
    triple_shot.update()

def reset_triple_shot():
    triple_shot.reset()
