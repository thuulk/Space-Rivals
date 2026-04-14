# Module created to define and store the power-up mechanic of Space Rivals

from classes import MovableObject, game, player, base_dir
import pygame
import random
import math
import os


class PowerUp(MovableObject):

    # List that tracks all power-up instances for mutual exclusivity.
    _all_instances = []

    # Function that initializes the attributes of this class.
    def __init__(self, quantity, initial_position_x, initial_position_y,
                 position_x_change, position_y_change, image,
                 center_color=None, border_color=None,
                 spawn_chance=0.05, duration_ms=10_000):

        super().__init__(quantity, initial_position_x, initial_position_y,
                         position_x_change, position_y_change, image)

        # Register this instance for mutual exclusivity between power-ups.
        PowerUp._all_instances.append(self)

        # Color attributes for customizing the power-up appearance.
        self.center_color = center_color
        self.border_color = border_color

        # Spawn chance and effect duration configurable per instance.
        self.spawn_chance = spawn_chance
        self.duration_ms = duration_ms

        # Attribute that determines if the power-up is visible on screen.
        self.visible = False

        # Attribute that determines if the power-up effect is currently active.
        self.active = False

        # Storing the tick when the power-up was collected to track duration.
        self.activation_ticks = 0

        # Radius in pixels for detecting collision between the player and the power-up.
        self.hit_radius = 35

        # If colors are provided, build a colored surface for the power-up sprite.
        if center_color and border_color:
            self._build_colored_surface()

    # Function that builds a colored surface combining circles with the sprite on top.
    def _build_colored_surface(self):
        original = self.image_path[0]
        orig_w, orig_h = original.get_size()
        padding = 10
        size = max(orig_w, orig_h) + padding * 2
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)
        pygame.draw.circle(surface, self.border_color, center, size // 2)
        pygame.draw.circle(surface, self.center_color, center, size // 3)
        sprite_x = (size - orig_w) // 2
        sprite_y = (size - orig_h) // 2
        surface.blit(original, (sprite_x, sprite_y))
        self.image_path[0] = surface

    # Function that attempts to spawn the power-up at the given coordinates with a random chance.
    def spawn(self, position_x, position_y):

        """Only one power-up can be on screen at a time, and not while the buff is active."""
        if not self.visible and not self.active:
            if random.random() < self.spawn_chance:
                self.position_x[0] = position_x
                self.position_y[0] = position_y
                self.visible = True

    # Function that checks if the triple shot effect is currently active.
    def is_active(self):

        if not self.active:
            return False

        return pygame.time.get_ticks() - self.activation_ticks < self.duration_ms

    # Function that returns the milliseconds left on the active buff (0 if inactive).
    def remaining_ms(self):

        if not self.active:
            return 0

        return max(0, self.duration_ms - (pygame.time.get_ticks() - self.activation_ticks))

    # Function that resets the power-up to its initial state (used when restarting the game).
    def reset(self):
        self.visible = False
        self.active = False
        self.activation_ticks = 0
        self.position_x[0] = 0
        self.position_y[0] = -64

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

        # If the player collects the power-up, activate its effect and deactivate any other active power-up.
        if collision < self.hit_radius:
            for other in PowerUp._all_instances:
                if other is not self:
                    other.active = False
            self.visible = False
            self.active = True
            self.activation_ticks = pygame.time.get_ticks()


def _tint_surface(surface, color):
    """Creates a tinted copy of a surface preserving only the original alpha."""
    result = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))
            if a > 0:
                result.set_at((x, y), (color[0], color[1], color[2], a))
    return result


# Creating the triple shot power-up instance (red tint).
_red_sprite = _tint_surface(
    pygame.image.load(os.path.join(base_dir, '../images/power_up.png')).convert_alpha(),
    (255, 80, 80))

power_up = PowerUp(1,
                   0, -64, 0, 3,
                   _red_sprite)


# Module-level functions that delegate to the power_up instance.
# These are imported by functions.py.

def spawn_power_up(position_x, position_y):
    power_up.spawn(position_x, position_y)

def update_power_up():
    power_up.update()

def triple_shot_active():
    return power_up.is_active()

def reset_power_up():
    power_up.reset()
