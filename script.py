#!/usr/bin/python

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(5, True) # powered on
GPIO.output(5, False) # powered off

GPIO.input(6) == 0 # depressed
GPIO.input(6) == 1 # not pressed

GPIO.input(21) == 0 # broken
GPIO.input(21) == 1 # unbroken


