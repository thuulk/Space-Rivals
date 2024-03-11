# Module created to define and store functions of Space_Heroic source code
import random

from classes import game, bullet, enemies, player, timer, meteors
from pygame import mixer
import pygame
import math


# Function that initialize everything required for the game to run.
def initialize():

    # Initialize pygame.
    pygame.init()

    # Setting the title and icon screen.
    pygame.display.set_caption('Space Rivals')
    pygame.display.set_icon(game.icon)

    # Initialize music
    pygame.mixer.init()
    mixer.music.load('corneria.mp3')
    mixer.music.set_volume(1)
    mixer.music.play(-1)

    # Setting the frame rate in which the screen updates.
    timer.clock.tick(60)

    # Respawning enemies.
    for enemy in range(enemies.quantity):
        enemies.respawn(enemy, 0, 200, True)

    # Respawning player.
    for iteration in range(player.quantity):
        player.regenerate_object(iteration, 0, 0, False, 368, 518)
        bullet.visible = False

    # Respawning asteroids
    for meteor in range(meteors.quantity):
        meteors.regenerate_object(meteor, 0, 0, False, random.randint(0, 736), random.randint(-256, -128))

    # Resetting score
    game.score = 0


# Function that resets the music to the beginning.
def reinitialize_music():

    mixer.music.stop()
    mixer.music.play()


# Hitbox function.
def hitbox(position_x_1, position_y_1, position_x_2, position_y_2, distance_pixels):

    collision = math.sqrt(math.pow(position_x_1 - position_x_2, 2) +
                                        math.pow(position_y_1 - position_y_2, 2))

    # If collision is lower than distance_pixels, return True
    if collision < distance_pixels:
        return True

    # If collision ain't lower than distance_pixels, Return False
    else:
        return False


# Function that contains the block code that conforms the main menu.
def game_menu():

    # Displaying the background, game title, and options (Play and exit) texts.
    game.screen.blit(game.background, (0, 0))
    game.menu.display_text(game.menu.title_font, "Space Rivals", 145, 200, game.menu.default_color)
    game.menu.display_text(game.menu.option_font, "Play", 145, 350, game.menu.play_color)
    game.menu.display_text(game.menu.option_font, "Exit", 145, 400, game.menu.exit_color)

    # for each event in the game, execute the next block.
    for event in pygame.event.get():

        # If a key is pressed down, execute the next block
        if event.type == pygame.KEYDOWN:

            # If you click the quit button on the screen, exit the game.
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # If the player press the up or w key, the "play" text color will change to purple.
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                game.menu.play_color = (87, 35, 100)
                game.menu.exit_color = (255, 255, 255)

            # If the player press the up or w key, the "exit" text color will change to purple.
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                game.menu.play_color = (255, 255, 255)
                game.menu.exit_color = (87, 35, 100)

            # if the player press enter key and play text is color purple, the game will start.
            if event.key == pygame.K_RETURN and game.menu.play_color == (87, 35, 100):
                game.menu.execute = False

            # if the player press enter key and play text is color purple, he will exit the game.
            if event.key == pygame.K_RETURN and game.menu.exit_color == (87, 35, 100):
                pygame.quit()
                exit()

    # Updating the screen.
    pygame.display.flip()


def in_game_inputs():

    # for each tick in game execute the next block.
    for event in pygame.event.get():

        # If you click the quit button on the screen, exit the game.
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # If a key is pressed, the next block will be executed.
        if event.type == pygame.KEYDOWN:

            # If the key pressed is "right arrow" or "d", the player will move to the right by 1.8 pixels.
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                for iteration in range(player.quantity):
                    player.move_to_right(iteration, 1.8)

            # If the key pressed is "left arrow" or "a", the player will move to the left by 1.8 pixels.
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                for iteration in range(player.quantity):
                    player.move_to_left(iteration, -1.8)

            # If the key pressed is space, the next block will be executed.
            if event.key == pygame.K_SPACE:

                for iteration in range(bullet.quantity):

                    # Setting to true the attribute that triggers the bullet being shot.
                    bullet.visible = True

                    # Playing the shoot sound.
                    bullet.sound.play()

                    # calling the function that updates position_y_change attribute from 0 to -12.
                    bullet.shoot(iteration, -12)

        # This is an event I set to be called every millisecond.
        if event.type == pygame.USEREVENT:
            timer.update_time()


# # Function that makes every specified object to move.
def movable_objects():

    # Displaying the background image on the screen.
    game.screen.blit(game.background, (0, 0))

    # Player -------------------------------------------------------------------------------------------------
    for iteration in range(player.quantity):

        # Updating the player's position.
        player.update_position(iteration, player.image_path)

        # If the position in the X axis of the player is 0 or below, the next block will be executed.
        if player.position_x[iteration] <= 0:
            player.stop_player_left(iteration)

        # If the position in the X axis of the player is 734 or greater, the next block will be executed.
        if player.position_x[iteration] >= 734:
            player.stop_player_right(iteration)

    # Enemies ------------------------------------------------------------------------------------------------
    for enemy in range(enemies.quantity):

        # Updating enemies' position.
        enemies.update_position(enemy, enemies.image_path)

        # Updating the position of the enemy whenever they hit the screen limits.
        if enemies.position_x[enemy] >= 736:
            enemies.move_to_left(enemy, -1)
            enemies.move_down(enemy)

        # Updating the position of the enemy whenever they hit the screen limits.
        if enemies.position_x[enemy] <= 0:
            enemies.move_to_right(enemy, 1)
            enemies.move_down(enemy)

        # Ending the game because an enemy ship passing through the player.
        if enemies.position_y[enemy] >= 550:
            game.over = True
            game.execute = False

        # Collisions ---------------------------------------------------------------------------------------------------
        for iteration in range(bullet.quantity):

            # Storing the collision between the bullet and the enemy.
            collision_bullet_n_enemy = hitbox(enemies.position_x[enemy], enemies.position_y[enemy],
                                              bullet.position_x[iteration], bullet.position_y[iteration],
                                              28)

            # Storing the collision between the player and the enemy.
            collision_player_n_enemy = hitbox(enemies.position_x[enemy], enemies.position_y[enemy],
                                              player.position_x[iteration], player.position_y[iteration],
                                              60)

            # Storing the collision between the player and the meteor.
            collision_player_n_meteor = hitbox(player.position_x[iteration], player.position_y[iteration],
                                               meteors.position_x[iteration], meteors.position_y[iteration],
                                               100)

            # If there is a collision between the bullet and an enemy, the next block will be executed.
            if collision_bullet_n_enemy:

                # Resetting the destruction sound.
                game.destruction_sound.stop()

                # Playing the destruction sound.
                game.destruction_sound.play()

                # Updating the player's
                game.update_score()

                # Difficulty curve
                enemies.respawn(enemy, 0, 200, 2500, False, 0 )
                enemies.respawn(enemy, 0, 225, 3000, False, 2500)
                enemies.respawn(enemy, 0, 250, 3500, False, 3000)
                enemies.respawn(enemy, 0, 275, 4000, False, 3500)
                enemies.respawn(enemy, 0, 300, 4500, True)

                # Bullet won't be longer visible until space key is pressed again.
                bullet.visible = False

            # If there is a collision between the player and an enemy, the next block will be executed.
            if collision_player_n_enemy:

                # Ending the game and activating the game over screen.
                game.execute = False
                game.over = True

            # If there is a collision between the player and a meteor, the next block will be executed.
            if collision_player_n_meteor:

                # Ending the game and activating the game over screen.
                game.execute = False
                game.over = True

    # Bullet -------------------------------------------------------------------------------------------------
    for iteration in range(bullet.quantity):

        # If the bullet attribute "visible" is not true, the next block will be executed.
        if not bullet.visible:

            ''' Calling the function that force the bullet to follow the ship in the X axis and sets
            the position_y_change parameter to 0 '''
            bullet.follow_ship(iteration, 15, 0)

        # If the bullet attribute "visible" is true, the next block will be executed.
        if bullet.visible:

            # Calling the function that shoots the bullet by updating its position by -12 pixels in the Y axis.
            bullet.update_position(iteration, bullet.image_path)

        # If bullet position in the Y axis is below -64 pixels, the next block will be executed.
        if bullet.position_y[iteration] <= -64:

            ''' As the attribute that shoots the bullet isn't true anymore, the bullet will stop updating its position
            and the block that calls the bullet.follow_ship(iteration, position_x_change, position_y_change)
            will be triggered '''
            bullet.visible = False

            # Resetting the bullet coordinate in Y axis by 518.
            bullet.position_y[iteration] = 518

    # Meteors ----------------------------------------------------------------------------------------------------------
    # if score is greater than 750 points, but lower than 1500 points, the next block will be executed.
    if 750 < game.score <= 1500:

        # for each meteor in one iteration, execute:
        for iteration in range(1):

            # If meteors.visible attribute isn't true, the next block will be executed.
            if not meteors.visible:

                # Generating the meteor
                meteors.regenerate_object(iteration, -256, -128, True)

                # Setting to true the value that triggers the meteor to move.
                meteors.visible = True

            # If meteors.visible attribute is true, the next block will be executed.
            if meteors.visible:
                meteors.shoot(iteration, 2)
                meteors.update_position(iteration, meteors.image_path)

            # If the meteor Y coordinate is greater or equal to 826, execute the following block.
            if meteors.position_y[iteration] >= 826:

                ''' Setting meteors.visible to false. As the attribute that triggers the meteor movement is not true 
                anymore, the meteor will generate again above screen limits, then setting the meteors.visible attribute
                to true again, making the meteor fall again, until it reaches pixel 826 in Y coordinate, making the 
                meteors.visible to false again '''
                meteors.visible = False

    # If score is greater than 1500 points, execute the following block.
    if 1500 < game.score:

        ''' This block does the same as the one above, with the slight difference that this one generates two meteors 
        instead of one. '''
        for iteration in range(2):

            if not meteors.visible:
                meteors.regenerate_object(iteration, 0, 0, False, random.randint(0, 736),
                                          random.randint(-256, -128))
                meteors.visible = True

            if meteors.visible:
                meteors.shoot(iteration, 2)
                meteors.update_position(iteration, meteors.image_path)

            if meteors.position_y[0] and meteors.position_y[1] >= 826:
                meteors.visible = False

# Game over function.
def game_over():

    # Stopping the music.
    mixer.music.stop()

    # Setting the background to a black image.
    game.screen.fill((0, 0, 0))

    for sprite in range(game.destruction_sprite.quantity):

        # Calling the function that stops the player from moving.
        player.stand_by(sprite)
        game.destruction_sprite.follow_ship(sprite, 0, 0)

        # If timer is lower than 0.39 seconds, execute the following block.
        if timer.seconds < 0.39:

            # Updating the position of the player.
            player.update_position(sprite, player.image_path)

        # If timer is lower or equal to 0.08 seconds, execute the following block.
        if timer.seconds <= 0.08:

            # Display the first sprite of the explosion.
            game.destruction_sprite.update_position(sprite, game.destruction_sprite.image_path)

        # If timer is greater than 0.08 seconds and lower or equal to 0.16 seconds, execute the following block.
        if 0.08 < timer.seconds <= 0.16:

            # Display the second sprite of the explosion.
            game.destruction_sprite.update_position(sprite, game.destruction_sprite.frame02)

        # If timer is greater than 0.16 seconds and lower or equal to 0.24 seconds, execute the following block.
        if 0.16 < timer.seconds <= 0.24:

            # Display the third sprite of the explosion.
            game.destruction_sprite.update_position(sprite, game.destruction_sprite.frame03)

        # If timer is greater than 0.24 seconds and lower or equal to 0.4 seconds, execute the following block.
        if 0.24 < timer.seconds <= 0.4:

            # Display the fourth sprite of the explosion.
            game.destruction_sprite.update_position(sprite, game.destruction_sprite.frame04)

    # If timer is lower than 1.5 seconds, execute the following block.
    if timer.seconds < 1.5:

        # Play death sound.
        player.death_sound.play()

    # If timer is greater than 2 seconds, execute the following block.
    if timer.seconds > 2:

        # Display the "Game Over" text.
        game.game_over_text(game.title_font, "Game Over", 200, 200, game.default_color)

    # if timer is greater than 3 seconds.
    if timer.seconds > 3:

        # Displaying the "Try Again" and "Exit" text.
        game.display_text(game.option_font, "Try Again", 160, 300, game.play_color)
        game.display_text(game.option_font, "Exit", 160, 340, game.exit_color)

    """ This block does the same as the one to choose options in game_menu function, if you have any doubts 
    about this block, please check the comments in the block from menu """
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.USEREVENT:
            timer.update_time()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP or event.key == pygame.K_w:
                game.play_color = (87, 35, 100)
                game.exit_color = (255, 255, 255)

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                game.play_color = (255, 255, 255)
                game.exit_color = (87, 35, 100)

            if event.key == pygame.K_RETURN and game.play_color == (87, 35, 100):
                game.reset = True
                game.execute = True
                game.menu.execute = False
                game.over = False

            if event.key == pygame.K_RETURN and game.exit_color == (87, 35, 100):
                pygame.quit()
                exit()

    pygame.display.flip()


