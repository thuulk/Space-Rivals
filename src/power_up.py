# Module created to define and store the power-up mechanic of Space Rivals

from classes import MovableObject, game, player, base_dir
import pygame
import random
import math
import os


# Chance to spawn a power-up when an enemy is destroyed (5%).
_SPAWN_CHANCE = 0.05

# Duration of the triple shot effect in milliseconds (10 seconds).
_DURATION_MS = 10_000


class PowerUp(MovableObject):

    # Function that initializes the attributes of this class.
    def __init__(self, quantity, initial_position_x, initial_position_y,
                 position_x_change, position_y_change, image):

        super().__init__(quantity, initial_position_x, initial_position_y,
                         position_x_change, position_y_change, image)

        # Attribute that determines if the power-up is visible on screen.
        self.visible = False

        # Attribute that determines if the triple shot effect is currently active.
        self.active = False

        # Storing the tick when the power-up was collected to track duration.
        self.activation_ticks = 0

        # Radius in pixels for detecting collision between the player and the power-up.
        self.hit_radius = 35

    # Function that attempts to spawn the power-up at the given coordinates with a random chance.
    def spawn(self, position_x, position_y):

        """Only one power-up can be on screen at a time, and not while the buff is active."""
        if not self.visible and not self.active:
            if random.random() < _SPAWN_CHANCE:
                self.position_x[0] = position_x
                self.position_y[0] = position_y
                self.visible = True

    # Function that checks if the triple shot effect is currently active.
    def is_active(self):

        if not self.active:
            return False

        return pygame.time.get_ticks() - self.activation_ticks < _DURATION_MS

    # Function that returns the milliseconds left on the active buff (0 if inactive).
    def remaining_ms(self):

        if not self.active:
            return 0

        return max(0, _DURATION_MS - (pygame.time.get_ticks() - self.activation_ticks))

    # Function that updates the power-up each frame: moves, draws, checks collection, and manages timer.
    def update(self):

        # If the effect is active but the timer has expired, deactivate the effect.
        if self.active and not self.is_active():
            self.active = False

        # If the power-up is not visible, there is nothing to update.
        if not self.visible:
            return

        # Updating the power-up's position on screen (moves it down and draws it).
        self.update_position(0, self.image_path)

        # If the power-up goes off the bottom of the screen, remove it.
        if self.position_y[0] > 640:
            self.visible = False
            return

        # Calculating the distance between the player and the power-up.
        collision = math.sqrt(
            math.pow(self.position_x[0] - player.position_x[0], 2) +
            math.pow(self.position_y[0] - player.position_y[0], 2))

        # If the player collects the power-up, activate the triple shot effect.
        if collision < self.hit_radius:
            self.visible = False
            self.active = True
            self.activation_ticks = pygame.time.get_ticks()


# Creating the power-up instance.
power_up = PowerUp(1,
                   0, -64, 0, 3,
                   pygame.image.load(os.path.join(base_dir, '../images/power_up.png')))


# Module-level functions that delegate to the power_up instance.
# These are imported by functions.py.

def spawn_power_up(position_x, position_y):
    power_up.spawn(position_x, position_y)

def update_power_up():
    power_up.update()

def triple_shot_active():
    return power_up.is_active()
