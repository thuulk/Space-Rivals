# Power-up module — yellow orb that drops from destroyed enemies.
# When the player catches it, triple shot is activated for 10 seconds.

import math
import os
import random

import pygame

from classes import player, game, base_dir

_FALL_SPEED  = 3          # pixels per frame
_HIT_RADIUS  = 35         # player catch radius
_DURATION_MS = 10_000     # 10 seconds in milliseconds
_SPAWN_CHANCE = 0.05      # 5 % chance per enemy kill

_img = pygame.image.load(os.path.join(base_dir, '../images/power_up.png'))

# Internal state
_x              = 0
_y              = -64
_visible        = False
_active         = False
_activation_ticks = 0


def spawn_power_up(x, y):
    """Attempt to spawn the power-up at (x, y) with _SPAWN_CHANCE probability.
    Only one power-up can be on screen at a time, and not while the buff is active."""
    global _x, _y, _visible
    if not _visible and not _active and random.random() < _SPAWN_CHANCE:
        _x = x
        _y = y
        _visible = True


def triple_shot_active():
    """Return True while the power-up buff is running."""
    if not _active:
        return False
    return pygame.time.get_ticks() - _activation_ticks < _DURATION_MS


def remaining_ms():
    """Milliseconds left on the active buff (0 if inactive)."""
    if not _active:
        return 0
    return max(0, _DURATION_MS - (pygame.time.get_ticks() - _activation_ticks))


def update_power_up():
    """Call once per frame inside the main game loop."""
    global _x, _y, _visible, _active, _activation_ticks

    # Expire the buff when the timer runs out
    if _active and not triple_shot_active():
        _active = False

    if not _visible:
        return

    # Fall downward
    _y += _FALL_SPEED

    # Remove if it exits the screen
    if _y > 640:
        _visible = False
        return

    # Draw the orb
    game.screen.blit(_img, (_x, _y))

    # Check player collision
    dist = math.sqrt((_x - player.position_x[0]) ** 2 + (_y - player.position_y[0]) ** 2)
    if dist < _HIT_RADIUS:
        _visible         = False
        _active          = True
        _activation_ticks = pygame.time.get_ticks()
