import datetime
import random
import time

length = 25  # length of LED ribbons
width = 12   # count of LED ribbons
widths = range(width)
cyan = '\033[96;1m'
red = '\033[91;1m'
redorange = red
orange = cyan
orangeyellow = orange
yellow = '\033[93;1m'
yellowgreen = yellow
green = '\033[92;1m'
greenblue = green
blue = '\033[94;1m'
blueviolet = blue
magenta = '\033[95;1m'
violet = magenta
violetblack = violet
reset = '\033[0m'

colors = [red, redorange, orange, orangeyellow, yellow, yellowgreen, green, greenblue, blue, blueviolet, violet, violetblack]

sunset = datetime.datetime(2016, 5, 28, 19, 53, 00, 00)
twilight = datetime.datetime(2016, 5, 28, 21, 35, 00, 00)
moonrise = datetime.datetime(2016, 5, 29, 00, 34, 00, 00)
sunrise = datetime.datetime(2016, 5, 29, 05, 39, 00, 00)

# def gettimes(o):
#     return 'time in stage: %s, seconds in stage: %s' % (o, o.total_seconds())
# 
# print 'sunset to twilight:   ', gettimes(twilight-sunset)
# print 'sunset to moonrise:   ', gettimes(moonrise-sunset)
# print 'twilight to moonrise: ', gettimes(moonrise-twilight)
# print 'twilight to sunrise:  ', gettimes(sunrise-twilight)
# print 'moonrise to sunrise:  ', gettimes(sunrise-moonrise)
# print 'sunset to sunrise:    ', gettimes(sunrise-sunset)
# 
# sunset to twilight:    time in stage: 1:42:00, seconds in stage: 6120.0 (*)
# sunset to moonrise:    time in stage: 4:41:00, seconds in stage: 16860.0
# twilight to moonrise:  time in stage: 2:59:00, seconds in stage: 10740.0 (*)
# twilight to sunrise:   time in stage: 8:04:00, seconds in stage: 29040.0
# moonrise to sunrise:   time in stage: 5:05:00, seconds in stage: 18300.0 (*)
# sunset to sunrise:     time in stage: 9:46:00, seconds in stage: 35160.0 (*)

sunset_to_twilight = twilight - sunset
twilight_to_moonrise = moonrise - twilight
moonrise_to_sunrise = sunrise - moonrise
sunset_to_sunrise = sunrise - sunset
totaltime = sunset_to_sunrise.total_seconds()


def main():
    for duration in [sunset_to_twilight, twilight_to_moonrise,
                     moonrise_to_sunrise]:
        seconds = duration.total_seconds()
        interval = seconds / (length * width * len(colors)) / 100
        for color in colors:
            print color
            for l in range(length):
                random.shuffle(widths)
                #for w in widths:
                #    print w,
                #    time.sleep(interval)
                print widths
                time.sleep(interval)
    print reset

if __name__ == '__main__':
    try:
        main()
    except:
        print reset
