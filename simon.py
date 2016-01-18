from __future__ import print_function 
from getch import getch
import random

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

boards = {}
boards['standard'] = [ red, yellow, blue, green ]
boards['brian'] = [ blue, white, lightblue, brightblue ]
boards['bryan'] = [ red, white, pink, brightred ]
boards['rob'] = [ purple, red, purple, blue ]


def play(colors, count, board):
    select = random.randint(0, len(board) - 1)
    color = board[select]
    colors.append(color)
    for color in colors:
        print(color)
    c = 0
    print('enter the colors:')
    for color in colors:
        c += 1
        user_input = getch()
        if user_input != color:
            return False, colors
    # trigger sound play, name files as USER_COUNT.mp3 for easy play
    # when no more files remain, play some other file?
    return True, colors


def rungame(user):
    board = boards[user]
    a = True
    count = 0
    colors = []
    while a is True:
        count += 1
        (a, colors) = play(colors, count, board)
    else:
        print('wah wah!')


if __name__ == '__main__':
    # if RFID receiver registers USER nearby, select a different board
    user = 'standard'
    try:
        rungame(user)
    except KeyboardInterrupt:
        print('thanks for playing')


