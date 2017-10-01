#!/usr/bin/python

from parse_tweets import *
import sys
from time import sleep

DELAY_DEFAULT = 180

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Missing operand: twitter URL.'
        print 'Usage: python notify_rtt.py <twitter URL> [<delay in seconds>]'
        print 'Default value for delay is %d seconds.' %(DELAY_DEFAULT)
        exit()

    feed = sys.argv[1]

    # Check if the user has set delay. 
    if len(sys.argv) == 3:
        delay = int(sys.argv[2])
    else:
        # Default delay is 120 seconds. 
        delay = DELAY_DEFAULT

    # Loop till eternity. 
    while True:
        parse_feed(feed)
        sleep(delay)
