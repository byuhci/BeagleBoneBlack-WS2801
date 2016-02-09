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
        while True:
            self.leds.off()

            self.leds[22] = soft_yellow
            self.leds[21] = soft_yellow
            self.leds[16] = soft_yellow
            self.leds[17] = soft_yellow
            self.leds[18] = soft_yellow
            self.leds.refresh()

            sleep(turn_delay)

            self.leds[22] = 0
            self.leds[21] = 0
            self.leds[16] = 0
            self.leds[17] = 0
            self.leds[18] = 0

            self.leds[14] = soft_yellow
            self.leds[13] = soft_yellow
            self.leds[8] = soft_yellow
            self.leds[9] = soft_yellow
            self.leds[10] = soft_yellow
            self.leds.refresh()

            sleep(turn_delay)

            self.leds[14] = 0
            self.leds[13] = 0
            self.leds[8] = 0
            self.leds[9] = 0
            self.leds[10] = 0

            self.leds[6] = soft_yellow
            self.leds[5] = soft_yellow
            self.leds[0] = soft_yellow
            self.leds[1] = soft_yellow
            self.leds[2] = soft_yellow
            self.leds.refresh()

            sleep(1.5 *turn_delay)

if __name__ == '__main__':
    me = BikeLEDs()
    me.left_turn()
