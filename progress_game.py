#!/usr/bin/env python3

# Created by: Ben Lapuhapo
# Created on: OCT 2019
# This program is the "Space Alien" game
#   for CircuitPython

import ugame
import stage
import constants
import board
import neopixel
import time

DELAY = 0.25
# get sound ready
pew_sound = open("jump.wav", 'rb')
start_sound = open("pew.wav", 'rb')

sound = ugame.audio
sound.stop()
sound.mute(False)

def menu_scene():
    # this function is the splash game loop

    # new pallet for black filled text
    NEW_PALETTE = (b'\xff\xff\x00\x22\xcey\x22\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                    b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')

    # An image bank for CicuitPython
    image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")

     # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_1, constants.SCREEN_X, constants.SCREEN_Y)

    # a list of sprites that will be updated every frame
    sprites = []

    # add text objects
    text = []
    text1 = stage.Text(width=29, height=12, font=None, palette=NEW_PALETTE, buffer=None)
    text1.move(20, 10)
    text1.text("Dylan & Ben\n Game Studios")
    text.append(text1)

    text2 =stage.Text(width=29, height=12, font=None, palette=NEW_PALETTE, buffer=None)
    text2.move(40, 110)
    text2.text("Press Start")
    text.append(text2)


    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers, items show up in order
    game.layers = text + sprites + [background]
    # render the background and initial location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()
        # print(keys)
        # A button to fire
        if keys & ugame.K_START != 0:
            sound.play(start_sound)
            game_scene()

        # update game logic

        game.tick()  # wait until refresh rate finishes

def game_scene():
    # this function keeps the information of the buttons
    a_button_pressed = constants.button_state["button_up"]
    b_button_pressed = constants.button_state["button_up"]
    start_button_pressed = constants.button_state["button_up"]
    select_button_pressed = constants.button_state["button_up"]
    # LED
    PIXEL_PIN = board.NEOPIXEL  # pin that the NeoPixel is connected to
    ORDER = neopixel.RGB   # pixel color channel order
    COLOR_one= (0, 255, 0) # color to blink
    COLOR_two = (255, 0, 0)
    CLEAR = (0, 0, 0)      # clear (or second color)
    pixel = neopixel.NeoPixel(PIXEL_PIN, 5, pixel_order=ORDER)

    # an image bank for CircuitPython
    image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_1, constants.SCREEN_X, constants.SCREEN_Y)

    # a list of sprites that will be updated every frame
    sprites = []

    ship = stage.Sprite(image_bank_1, 5, int(constants.SCREEN_X / 2 - constants.SPRITE_SIZE / 2),
                        int(constants.SCREEN_Y - constants.SPRITE_SIZE + constants.SPRITE_SIZE / 2))
    sprites.append(ship) # Insert at the top of the sprite list

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers, items show up in order
    game.layers = sprites + [background]
    # render the background and initial location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()
        # print(keys)
        # A button to fire
        if keys & ugame.K_X != 0:
            if a_button_pressed == constants.button_state["button_up"]:
                a_button_pressed = constants.button_state["button_just_pressed"]
            elif a_button_pressed == constants.button_state["button_just_pressed"]:
                a_button_pressed = constants.button_state["button_still_pressed"]
        else:
            a_button_pressed = constants.button_state["button_up"]

        # update game logic

        # move ship right
        if keys & ugame.K_RIGHT != 0:
            if ship.x > constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)
            else:
                ship.move(ship.x + 1, ship.y)

        # move ship left
        if keys & ugame.K_LEFT != 0:
            if ship.x < 0:
                ship.move(0, ship.y)
            else:
                ship.move(ship.x - 1, ship.y)

        # play sound if A is pressed
        if a_button_pressed == constants.button_state["button_just_pressed"]:
            sound.play(pew_sound)
            pixel[2] = COLOR_two
            time.sleep(DELAY)
            pixel[2] = CLEAR

        if keys & ugame.K_SELECT != 0:
            if select_button_pressed == constants.button_state["button_up"]:
                select_button_pressed = constants.button_state["button_just_pressed"]
            elif select_button_pressed == constants.button_state["button_just_pressed"]:
                select_button_pressed = constants.button_state["button_still_pressed"]
        else:
            select_button_pressed = constants.button_state["button_up"]

        if select_button_pressed == constants.button_state["button_just_pressed"]:
            pixel[2] = COLOR_two
            time.sleep(DELAY)
            pixel[2] = CLEAR
            menu_scene()
        # redraw sprite list
        game.render_sprites(sprites)
        game.tick()  # wait until refresh rate finishes

if __name__ == "__main__":
    menu_scene()
