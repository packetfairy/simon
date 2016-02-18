from __future__ import print_function
import RPi.GPIO as GPIO
import subprocess
import random
import time
import sys
import os

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
config['standard'] = {'board': ['red', 'green', 'blue', 'yellow'],
                      'difficulty': 1}
# config['standard'] = {'board': [red, yellow, blue, green],
#                       'difficulty': 1}
# config['brian'] = {'board': [blue, white, cyan, lightblue],
#                    'difficulty': 2}
# config['bryan'] = {'board': [red, white, pink, white],
#                    'difficulty': 3}
# config['erik'] = {'board': [yellow, white, orange, blue],
#                   'difficulty': 3}
# config['nate'] = {'board': [pink, magenta, cyan, white],
#                   'difficulty': 3}
# config['rob'] = {'board': [purple, red, purple, blue],
#                  'difficulty': 4}

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
LEDS = [4, 17, 27, 22]
SENSORS = [18, 23, 24, 25]
RESETLED = 26
RESETSENSOR = 21
# RFID = 12  # for the future


def gpio_setup():
    # will I get useful returncodes out of the GPIO if things are
    # misconfigured or nonoperational, or do I need to trust that
    # I have done the right things and that everything will always
    # work perfectly? :)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEDS, GPIO.OUT)
    GPIO.setup(RESETLED, GPIO.OUT)
    GPIO.setup(SENSORS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RESETSENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(RFID, GPIO.IN)  # for the future


def block_playsound(sound_path):
    """play sound file to audio port, pausing progress"""
    return subprocess.call(['play', '-q', sound_path])

def noblock_playsound(sound_path):
    """play sound file to audio port"""
    return subprocess.Popen(['play', '-q', sound_path])


def playcolor(duration, color, led_position, sound_path):
    # send color to led_position via serial pulse; does this block?
    # if so, maybe play sound first via something which detaches?
    # for v1.0, we're using simple positional arguments
    GPIO.output(LEDS[led_position], True)
    if 'fail' in sound_path:
        soundplay = block_playsound(sound_path)
    else:
        soundplay = noblock_playsound(sound_path)
    time.sleep(duration)
    GPIO.output(LEDS[led_position], False)


def read_rfid_port():
    # once we can do so, poll RFID port for presence of tag;
    # if it exists, return its ID, else return standard
    # for now, we will do this by simply randomly selecting a
    # directory of audio files to use
    dirs = subprocess.Popen(['ls', '-1', './audio'],
                            stdout=subprocess.PIPE).stdout.read()
    options = dirs[:-1].split('\n')
    return random.choice(options)


def read_sensor_ports():
    return [GPIO.input(sensor) for sensor in SENSORS]


def celebrate(high_sound, score):
    """i imagine running a full rainbow down the chain while playing
       some fun celebratory music. this would get used for that point
       where our player has reached the point where we thought they
       would never possibly reach"""
    print('congratulations! new high score: ', end='')
    soundplay = noblock_playsound(high_sound)
    while soundplay.poll() is None:
        GPIO.output(LEDS, True)
        time.sleep(0.1)
        GPIO.output(LEDS, False)
        time.sleep(0.1)
    else:
        GPIO.output(LEDS, False)
        highscore = int(score)
        print('%s' % highscore)
    return


def play(color_sequence, count, board, difficulty, sounds):
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
    #num = count
    #if num == 10:   # we'll assume we have only 10 sets of sound files,
    #    celebrate()   # and that this game will be challenging enough that
    #elif num > 10:  # reaching level 10 will be unlikely.
    #    num = 10

    # when we are using this, we need to include a user argument to play
    #
    # define sound file names
    # for when the color is being shown to you
    # show_sound = '%s/%02d_%s.wav' % (user, num, 'show')
    # for when you select the correct color
    # play_sound = '%s/%02d_%s.wav' % (user, num, 'play')
    # for when you pass the round
    # pass_sound = '%s/%02d_%s.wav' % (user, num, 'pass')
    # for when you select the wrong color
    # fail_sound = '%s/%s.wav' % (user, 'fail')
    # for when your game ends
    # over_sound = '%s/%s.wav' % (user, 'over')
    # for when you the player takes the high score
    # high_sound = '%s/%s.wav' % (user, 'high')

    # pick a new color
    select = random.choice(board)
    color_sequence.append(select)

    # set our difficulty level and length of time to light the LEDs
    led_duration = 0.1 + (0.25 / difficulty) - (difficulty/100.0)

    # display the color set for the user
    print('color sequence: %s' % color_sequence)
    for color in color_sequence:
        # our LED position corresponds to the color index on the board
        playcolor(led_duration, color, board.index(color), sounds['show'])
        # without this sleep, if we get two of the same color in a row,
        # the LED does not toggle off between plays
        time.sleep(0.1)

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
    color_count = 0
    evaluate_sequence = list(color_sequence)
    while time.time() < expired:
        click = 0
        sensor_port_response = read_sensor_ports()
        if click == 0:  # NO CLICK RECEIVED
            if 0 in sensor_port_response:  # CLICK-ON
                click = 1  # SET CLICK TO BE READ

        if click == 1:  # CLICK SET TO BE READ
            # print('evaluating click %s' % sensor_port_response)
            # print('spr: %s, b: %s' % (sensor_port_response.index(0), board.index(color)))
            print('l: %s, s: %s, e: %s, c: %s' % (len(color_sequence), color_sequence, evaluate_sequence, color_count))
            color = evaluate_sequence.pop(0)
            color_count += 1
            if sensor_port_response.index(0) != board.index(color):
                print('you picked %s, should have picked %s' % (board[sensor_port_response.index(0)], color))
                playcolor(led_duration, color, board.index(color), sounds['fail'])
                return False, color_sequence
            else:
                print('you picked %s' % board[sensor_port_response.index(0)])
                playcolor(led_duration, color, board.index(color), sounds['play'])
                print('l: %s, s: %s, e: %s, c: %s' % (len(color_sequence), color_sequence, evaluate_sequence, color_count))
                if len(color_sequence) == color_count:
                    soundplay = noblock_playsound(sounds['pass'])
                    for x in range(count + 3):
                        GPIO.output(LEDS, True)
                        time.sleep(0.1)
                        GPIO.output(LEDS, False)
                        time.sleep(0.1)
                    time.sleep(0.5)
                    return True, color_sequence
            click = 2  # SET CLICK AS READ

        if click == 2:  # CLICK SET AS READ
            if 0 not in sensor_port_response:
                click = 0  # CLICK-OFF
    else:
        time.sleep(0.1)
        soundplay = block_playsound(sounds['over'])
        return False, color_sequence


def rungame(user, highscore, sounds):
    winning = True
    count = 0
    color_sequence = []
    board = config[user]['board']
    difficulty = config[user]['difficulty']
    while winning is True:
        count += 1
        print('count %s ENTER color sequence is %s' % (count,color_sequence))
        GPIO.output(LEDS, False)
        (winning, color_sequence) = play(color_sequence, count, board,
                                         difficulty, sounds)
        print('status %s EXIT color sequence is %s' % (winning, color_sequence))
    else:
        score = count - 1
        print('wah wah! you made it %s rounds!' % score)
        print('final color sequence: %s' % color_sequence)
        if score > highscore:
            print('previous high score: %s' % highscore)
            celebrate(sounds['high'], score)
    return score


if __name__ == '__main__':
    gpio_setup()
    highscore = 0
    try:
        if sys.argv[1] == 'test':
            GPIO.output(LEDS, True)
            GPIO.output(RESETLED, True)
            time.sleep(1)
            GPIO.output(LEDS, False)
            GPIO.output(RESETLED, False)
            time.sleep(1)
            GPIO.output(LEDS, True)
            GPIO.output(RESETLED, True)
            time.sleep(1)
            GPIO.output(LEDS, False)
            GPIO.output(RESETLED, False)
            sys.exit(0)
    except:
        pass

    try:
        while True:
            GPIO.output(26, True)
            # if RFID receiver registers USER nearby, set and send user as arg
            # v1.0 won't be using that, so we are just getting 'standard' back
            if GPIO.input(21) == 0:
                GPIO.output(26, False)
                user = read_rfid_port()
                sound_types = ['start', 'show', 'play', 'fail', 'over', 'pass', 'high']
                sounds = {sound_type: 'audio/%s/%s_sound.wav' % (user, sound_type) for sound_type in sound_types}
                soundplay = block_playsound(sounds['start'])
                highscore = rungame('standard', highscore, sounds)
    except KeyboardInterrupt:  # this would be taking a prompt from the reset button
        GPIO.cleanup()         #
        exit                   # how can i capture a button press, and convert
                               # into an exception?
