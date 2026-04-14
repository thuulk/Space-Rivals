# Module created to define and store the speed power-up mechanic of Space Rivals

from classes import base_dir
from power_up import PowerUp
import pygame
import os


# Speed multiplier applied to the bullet when this power-up is active.
SPEED_MULTIPLIER = 2.5


def _recolor_to_yellow(surface):
    """Shifts an orange-tinted surface toward yellow by boosting the green channel."""
    result = surface.copy()
    boost = pygame.Surface(result.get_size(), pygame.SRCALPHA)
    boost.fill((0, 90, 0))
    result.blit(boost, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    return result


def _tint_surface(surface, color):
    """Creates a tinted copy of a surface preserving only the original alpha."""
    result = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))
            if a > 0:
                result.set_at((x, y), (color[0], color[1], color[2], a))
    return result


# Yellow power-up sprite (orange orb from power_up.png recolored to yellow).
_yellow_power_up_sprite = _recolor_to_yellow(
    pygame.image.load(os.path.join(base_dir, '../images/power_up.png')).convert_alpha())

# Yellow bullet sprite (purple laser recolored to yellow, used while the effect is active).
yellow_bullet_sprite = _tint_surface(
    pygame.image.load(os.path.join(base_dir, '../images/laser_player.png')).convert_alpha(),
    (255, 255, 50))


# Creating the speed power-up instance using the yellow orb sprite.
speed_power_up = PowerUp(1,
                         0, -64, 0, 3,
                         _yellow_power_up_sprite)


# Module-level functions that delegate to the speed_power_up instance.
# These are imported by functions.py.

def spawn_speed_power_up(position_x, position_y):
    speed_power_up.spawn(position_x, position_y)

def update_speed_power_up():
    speed_power_up.update()

def speed_shot_active():
    return speed_power_up.is_active()

def reset_speed_power_up():
    speed_power_up.reset()
