from __future__ import print_function
import RPi.GPIO as GPIO
import random
import time

# color = [red,green,blue]
# hoping that we can vary the luminosity of each diode so that I
# can create more than just these seven colors.
pink = [255, 36, 120]
red = [255, 36, 36]
orange = [255, 120, 36]
yellow = [255, 255, 36]
limegreen = [120, 255, 36]
green = [36, 255, 36]
lightgreen = [36, 255, 120]
cyan = [36, 255, 255]
lightblue = [36, 120, 255]
blue = [36, 36, 255]
purple = [120, 36, 255]
magenta = [255, 36, 255]
white = [255, 255, 255]

# where will this live?
config = {}
config['standard'] = {'board': [red, yellow, blue, green],
                      'difficulty': 1}
config['brian'] = {'board': [blue, white, cyan, lightblue],
                   'difficulty': 2}
config['bryan'] = {'board': [red, white, pink, white],
                   'difficulty': 3}
config['erik'] = {'board': [yellow, white, orange, blue],
                  'difficulty': 3}
config['nate'] = {'board': [pink, magenta, cyan, white],
                  'difficulty': 3}
config['rob'] = {'board': [purple, red, purple, blue],
                 'difficulty': 4}

# GPIO config details
#LEDS = []
# LEDS.append([red,green,blue])
#LEDS.append([4, 17, 27])
#LEDS.append([22, 5, 6])
#LEDS.append([13, 19, 26])
#LEDS.append([16, 20, 21])
#LED_SETUP = [pin for led_pins in LEDS for pin in led_pins]
# we are going to deal with LEDs via serial, rather than GPIO port toggle

# actually, for our v0.1, we will use four standard color 100mm arcade buttons
# assembled in some way so they are playable.
LEDS = [4. 17, 27, 22]
SENSORS = [18, 23, 24, 25]
RESET = 21
# RFID = 12  # for the future


def gpio_setup():
    # will I get useful returncodes out of the GPIO if things are
    # misconfigured or nonoperational, or do I need to trust that
    # I have done the right things and that everything will always
    # work perfectly? :)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEDS, GPIO.OUT)
    GPIO.setup(SENSORS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RESET, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(RFID, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # for the future


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


def light_led(led_position, duration):
    GPIO.output(led_position, True)
    time.sleep(duration)
    GPIO.output(led_position, False)


def playcolor(duration, color, led_position, sound):
    # send color to led_position via serial pulse; does this block?
    # if so, maybe play sound first via something which detaches?
    playsound(sound)  # ensure sound file is sufficient length for LED to light
    light_led(led_position, duration)


def read_rfid_port():
    # poll RFID port for presence of tag;
    # if it exists, return its ID, else:
    return 'standard'


def read_sensor_ports():
    for s in SENSORS:
        if GPIO.input(s) is True:
            return SENSORS.index(s)
    return False


def celebrate():
    """i imagine running a full rainbow down the chain while playing
       some fun celebratory music. this would get used for that point
       where our player has reached the point where we thought they
       would never possibly reach"""
    return


def play(color_sequence, count, user):
    # ok, so, we want to do a thing where we play different sounds
    # during each round. but, at a certain point, if we have a
    # crazy badass player, we will eventually exhaust our available
    # set of sounds. so, we'll do a check here.
    #
    # if need be, we can do the check by os.path.isfile(), like in
    # the case where we have more files in the set for one user than
    # we have for another one.
    #
    # for now, we'll do it with a basic check.
    num = count
    if count == 10:   # we'll assume we have only 10 sets of sound files,
        celebrate()   # and that this game will be challenging enough that
    elif count > 10:  # reaching level 10 will be unlikely.
        num = 10

    # define sound file names
    # for when the color is being shown to you
    show_sound = '%s/%02d_%s.wav' % (user, num, 'show')
    # for when you select the correct color
    play_sound = '%s/%02d_%s.wav' % (user, num, 'play')
    # for when you select the wrong color
    fail_sound = '%s/%02d_%s.wav' % (user, num, 'fail')
    # for when your game ends
    over_sound = '%s/%02d_%s.wav' % (user, num, 'over')
    # for when you pass the round
    pass_sound = '%s/%02d_%s.wav' % (user, num, 'pass')

    # pick a new color
    board = config[user]['board']
    select = random.choice(board)
    color_sequence.append(select)

    # set our difficulty level and length of time to light the LEDs
    difficulty = config[user]['difficulty']
    led_duration = 0.1 + (0.25 / difficulty) - (difficulty/100.0)

    # display the colors for the user
    for color in color_sequence:
        # our LED position corresponds to the color index on the board
        playcolor(led_duration, color, board.index(color), show_sound)

    # set up a timer which increases incrementally, and variably
    # depending upon difficulty level
    playtime = 1 + (count * 0.5) + ((count * 0.25) / difficulty)
    expired = time.time() + playtime

    # example values:                 -----------------play time-----------------
    # | difficulty level | light time | c=1 | c=2 | c=3 | c=4 | c=5 | c=6 | c=7 |
    # |        1         |   0.34     | 1.75| 2.5 |3.25 | 4.0 | 4.75| 5.5 | 6.25|
    # |        2         |   0.205    |1.625| 2.25|2.875| 3.5 |4.125| 4.75|5.375|
    # |        3         |   0.153    |1.583|2.167| 2.75|3.333|3.917| 4.5 |5.083|
    # |        4         |   0.123    |1.563|2.123|2.688| 3.25|3.813|4.375|4.938|
    # on its face, 1.75 seconds for a single depression sounds like a lot to me.
    # but i guess i want the game to be playable. so that's not so bad. and it
    # does get increasingly difficult. it should be pretty hard after 4, even for
    # standard difficulty. in actuality, this might not be enough time, given the
    # mechanism of interaction with the devices. but we'll see.

    # wait for the user to enter the correct sequence
    for color in color_sequence:
        while time.time() < expired:
            sensor_port_response = read_sensor_ports()
            if sensor_port_response:
                if sensor_port_response != board.index(color):
                    playcolor(led_duration, color, board.index(color), fail_sound)
                    return False, color_sequence
                else:
                    playcolor(led_duration, color, board.index(color), play_sound)
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
        print('wah wah! you made it %s rounds!' % (count - 1))
        print()


if __name__ == '__main__':
    gpio_setup()
    while True:
        # if RFID receiver registers USER nearby, set and send user as arg
        user = read_rfid_port()
        try:
            rungame(user)
        except KeyboardInterrupt:  # this would be taking a prompt from the "power" button
            exit                   # how can i capture a button press and convert it into an exception?
