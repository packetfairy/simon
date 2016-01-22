from __future__ import print_function 
import RPi.GPIO as GPIO
from getch import getch
import random
import time
import sys

red = 'r'
yellow = 'y'
blue = 'b'
green = 'g'
white = 'w'
lightblue = 'l'
brightblue = 'e'
pink = 'k'
brightred = 'd'
purple = 'p'

config = {}
config['standard'] = { 'board': [ red, yellow, blue, green ],
                       'difficulty': 0 }
config['brian'] = { 'board': [ blue, white, lightblue, brightblue ],
                    'difficulty': 1 }
config['bryan'] = { 'board': [ red, white, pink, brightred ] ,
                    'difficulty': 2 }
config['rob'] = { 'board': [ purple, red, purple, blue ] ,
                  'difficulty': 3 }

# GPIO config details
pin['red'] = 19
pin['yellow'] = 13
pin['blue'] = 6
pin['green'] = 5

switch['red'] = 12
switch['yellow'] = 16
switch['blue'] = 20
switch['green'] = 21


def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(switch.values(), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(pin.values(), GPIO.OUT)


def playcolor(color):
    GPIO.output(pin[color], True)
    time.sleep(0.5)
    GPIO.output(pin[color], False)


def monitorswitches(seconds):
    timeend = time.time() + seconds
    while time.time() < timeend:
        for s in switch:
            if GPIO.input(s) == True:
                return s
    return False


def play(colors, count, board):
    select = random.randint(0, len(board) - 1)
    color = board[select]
    colors.append(color)
    for color in colors:
        playcolor(color)
    c = 0
    print('enter the colors:')
    for color in colors:
        c += 1
        # need to implement timer function
        # hpoing that timer will be easy enough to "cheat" with
        # something like this:
        # expired = time.time() + some_growing_number_of_seconds
        # while time.time() < expired:
        #     gpio_port_response = check_gpio_ports()
        #     if gpio_port_response:
        #         if gpio_port_response != color:
        #             return incorrect error and exit
        #     time.sleep(0.01)
        # else:
        #     return timeout error and exit
        #
        # the alternative seems to be for the timer to live in a thread, but
        # i think i am not fancy enough to know how to make that work yet.
        user_input = getch()
        if user_input in ['', '!']:
            print('thanks for playing')
            sys.exit(0)
        if user_input != color:
            print('wrong selection (%s, you chose: %s)' % (color, user_input))
            return False, colors
    # trigger sound play
    #   - name files as USER_COUNT.mp3 for easy play
    # when no more files remain, play some other file?
    return True, colors


def rungame(user='standard'):
    board = config[user]['board']
    a = True
    count = 0
    colors = []
    while a is True:
        count += 1
        (a, colors) = play(colors, count, board)
    else:
        print('wah wah!')
        print()


if __name__ == '__main__':
    while True:
        # if RFID receiver registers USER nearby, set and send user as arg
        rungame()
