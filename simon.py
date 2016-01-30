from __future__ import print_function 
import RPi.GPIO as GPIO
from getch import getch
import random
import time
import sys

# color = [red,green,blue]
# hoping that we can vary the luminosity of each diode so that I
# can create more than just these seven colors.
red =    [1, 0, 0]
yellow = [1, 1, 0]
white =  [1, 1, 1]
purple = [1, 0, 1]
blue =   [0, 0, 1]
cyan =   [0, 1, 1]
green =  [0, 1, 0]

# where will this live?
config = {}
config['standard'] = { 'board': [red, yellow, blue, green],
                       'difficulty': 0 }
config['brian'] = { 'board': [blue, white, cyan, purple],
                    'difficulty': 1 }
config['bryan'] = { 'board': [red, white, purple, white],
                    'difficulty': 2 }
config['rob'] = { 'board': [purple, red, purple, blue],
                  'difficulty': 3 }

# GPIO config details
LEDS = []
# LEDS.append([red,green,blue])
LEDS.append([4, 17, 27])
LEDS.append([22, 5, 6])
LEDS.append([13, 19, 26])
LEDS.append([16, 20, 21])
LED_SETUP = [pin for led_pins in LEDS for pin in led_pins]

SENSORS = [18, 23, 24, 25]

RFID = 12


def gpio_setup():
    # will I get useful returncodes out of the GPIO if things are
    # misconfigured or nonoperational, or do I need to trust that
    # I have done the right things and that everything will always
    # work perfectly? :)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_SETUP, GPIO.OUT)
    GPIO.setup(SENSORS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RFID, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def playsound(sound):
    """play sound file to audio port"""
    print('you could try using subprocess, but that may be expensive.')
    print('')
    print('here are some links to help integrate audio directly into the')
    print('script via python libraries for when you are ready!')
    print('')
    print('http://stackoverflow.com/questions/17657103/how-to-play-wav-file-in-python')
    print('http://stackoverflow.com/questions/260738/play-audio-with-python')
    print('https://wiki.python.org/moin/Audio/')
    print('')


def playcolor(color, sound):
    GPIO.output(color, True)
    playsound(sound)  # ensure sound file is sufficient length for LED to light
    GPIO.output(color, False)


def read_rfid_port():
    # poll RFID port for presence of tag;
    # if it exists, return its ID, else:
    return 'standard'


def read_sensor_ports():
    for s in SENSORS:
        if GPIO.input(s) == True:
            return SENSORS.index(s)
    return False


def play(color_sequence, count, user):
    # define sound file names
    # for when the color is being shown to you
    show_sound = '%s_%s_%s.wav' % (count, user, 'show')
    # for when you select the correct color
    play_sound = '%s_%s_%s.wav' % (count, user, 'play')
    # for when you select the wrong color
    fail_sound = '%s_%s_%s.wav' % (count, user, 'fail')
    # for when your game ends
    over_sound = '%s_%s_%s.wav' % (count, user, 'over')
    # for when you pass the round
    pass_sound = '%s_%s_%s.wav' % (count, user, 'pass')

    # pick a new color
    board = config[user]['board']
    select = random.randint(0, len(board) - 1)
    append_color = board[select]
    color_sequence.append(append_color)

    # display the colors for the user
    for color in color_sequence:
        playcolor(color, show_sound)

    # set up a timer equal to 1 second plus a half second for every
    # color after the first
    expired = time.time() + ( 1 + (count * 0.5) )

    # wait for the user to enter the correct sequence
    for color in color_sequence:
        while time.time() < expired:
            sensor_port_response = read_sensor_ports()
            if sensor_port_response:
                if sensor_port_response != board.index(color):
                    playcolor(color, fail_sound)
                    return False, color_sequence
                else:
                    playcolor(color, play_sound)
        else:
            playsound(over_sound)
            return False, color_sequence
    playsound(pass_sound)
    return True, color_sequence


def rungame(user):
    winning = True
    count = 0
    color_sequence = []
    while winning is True:
        count += 1
        (winning, color_sequence) = play(color_sequence, count, user)
    else:
        print('wah wah! you made it %s rounds!' % count - 1)
        print()


if __name__ == '__main__':
    gpio_setup()
    while True:
        # if RFID receiver registers USER nearby, set and send user as arg
        user = read_rfid_port()
        rungame(user)
