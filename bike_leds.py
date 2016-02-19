#!/usr/bin/env python3
"""
This class uses the ws2801_leds library to display traffic signals for a
biker when they're arranged in a 3-diamond pattern from left to right.

Arrangement of LEDs:
     6      14      22
   5   7  13  15  21  23
 0   4   8  12  16  20  24
   1   3   9  11  17  19
     2      10      18

Kristian Sims, BYU Physical Computing 2016
"""

from ws2801_leds import *
from time import sleep

__author__ = 'Kristian Sims'

turn_delay = 0.6


class BikeLEDs:
    def __init__(self, leds=None):
        """
        Initialize the BikeLEDs class
        :param leds: WS2801LEDS object to display on
        :return: A new BikeLEDs instance
        """
        if leds is not None:
            self.leds = leds
        else:
            self.leds = WS2801LEDS()

        self.leds.hold_frame()  # refresh() must be called manually
        self.leds.off()

    def left_turn(self):
        """
        Turn left (forever)
        :return: None
        """
        self.leds.off()

        sleep(turn_delay)

        self.leds[6] = orange
        self.leds[5] = orange
        self.leds[0] = orange
        self.leds[1] = orange
        self.leds[2] = orange
        self.leds[4] = orange
        self.leds.refresh()

        sleep(turn_delay)

    def right_turn(self):
        """
        Turn left (forever)
        :return: None
        """
        self.leds.off()

        sleep(turn_delay)

        self.leds[22] = orange
        self.leds[23] = orange
        self.leds[20] = orange
        self.leds[24] = orange
        self.leds[19] = orange
        self.leds[18] = orange
        self.leds.refresh()

        sleep(turn_delay)

    def brake(self):
        """
        Brake lights pattern
        :return: None
        """
        self.leds.off()

        self.leds[0] = red
        self.leds[5] = red
        self.leds[7] = red
        self.leds[4] = red
        self.leds[8] = red
        self.leds[1] = red
        self.leds[3] = red

        self.leds[16] = red
        self.leds[21] = red
        self.leds[23] = red
        self.leds[20] = red
        self.leds[24] = red
        self.leds[17] = red
        self.leds[19] = red


if __name__ == '__main__':
    me = BikeLEDs()
    while True:
        for n in range(10):
            me.left_turn()
        for n in range(10):
            me.right_turn()

        me.brake()
        sleep(5)
