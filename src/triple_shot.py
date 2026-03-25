# Triple shot module — fires three red bullets from the player's position:
#   center  : 90°  (straight up)
#   right   : 65°  (upper-right diagonal)
#   left    : 115° (upper-left diagonal)

import math
import pygame
import os

from classes import Bullet, player, game, enemies, bullet, base_dir
from power_up import spawn_power_up

_SPEED = 18
_VX = _SPEED * math.cos(math.radians(65))   # ≈  7.61
_VY = _SPEED * math.sin(math.radians(65))   # ≈ 16.31  (negated when applied)

_img = pygame.image.load(os.path.join(base_dir, '../images/triple_bala.png'))

bullet_center = Bullet(1, 0, 518, 0, 0, False, _img)
bullet_right  = Bullet(1, 0, 518, 0, 0, False, _img)
bullet_left   = Bullet(1, 0, 518, 0, 0, False, _img)

# Normalise visible to a scalar (same convention used in the rest of the codebase)
bullet_center.visible = False
bullet_right.visible  = False
bullet_left.visible   = False


def _hitbox(x1, y1, x2, y2, threshold):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < threshold


def triple_ready():
    """Return True only when all three bullets are inactive."""
    return not (bullet_center.visible or bullet_right.visible or bullet_left.visible)


def triple_fire():
    """Spawn all three bullets at the player's current position."""
    px = player.position_x[0] + 15   # align with ship centre
    py = player.position_y[0]

    bullet_center.position_x[0]        = px
    bullet_center.position_y[0]        = py
    bullet_center.position_x_change[0] = 0
    bullet_center.position_y_change[0] = -_SPEED
    bullet_center.visible               = True

    bullet_right.position_x[0]        = px
    bullet_right.position_y[0]        = py
    bullet_right.position_x_change[0] = _VX
    bullet_right.position_y_change[0] = -_VY
    bullet_right.visible               = True

    bullet_left.position_x[0]        = px
    bullet_left.position_y[0]        = py
    bullet_left.position_x_change[0] = -_VX
    bullet_left.position_y_change[0] = -_VY
    bullet_left.visible               = True

    bullet.sound.play()


def _reset(b):
    b.visible               = False
    b.position_x_change[0] = 0
    b.position_y_change[0] = 0


def update_triple_shot():
    """Move bullets, check enemy collisions, and reset when off-screen."""
    for b in (bullet_center, bullet_right, bullet_left):
        if not b.visible:
            continue

        b.update_position(0, b.image_path)

        # Reset when the bullet leaves the visible area
        if b.position_y[0] <= -64 or b.position_x[0] < -64 or b.position_x[0] > 864:
            _reset(b)
            continue

        # Collision detection against every active enemy
        for enemy in range(enemies.quantity):
            if _hitbox(b.position_x[0], b.position_y[0],
                       enemies.position_x[enemy], enemies.position_y[enemy], 28):
                game.destruction_sound.stop()
                game.destruction_sound.play()
                game.update_score()

                # Chance to drop a power-up at the enemy's position.
                spawn_power_up(enemies.position_x[enemy], enemies.position_y[enemy])

                # Same difficulty curve as the normal bullet
                enemies.respawn(enemy, 0, 200, 2500, False, 0)
                enemies.respawn(enemy, 0, 225, 3000, False, 2500)
                enemies.respawn(enemy, 0, 250, 3500, False, 3000)
                enemies.respawn(enemy, 0, 275, 4000, False, 3500)
                enemies.respawn(enemy, 0, 300, 4500, True)

                _reset(b)
                break
