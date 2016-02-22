#!/usr/bin/env python3
"""
This class uses the ws2801_leds library to display traffic signals for a
biker when they're arranged in a 3-diamond pattern from left to right.

Arrangement of LEDs:
     2      10      18
   1   3   9  11  17  19
 0   4   8  12  16  20  24
   5   7  13  15  21  23
     6      14      22

Kristian Sims, BYU Physical Computing 2016
"""

from ws2801_leds import *
from time import sleep

__author__ = 'Kristian Sims'


class BikeLEDs:
    turn_interval = 0.6
    night_light_interval = 0.1
    left_arrow_dex = [0, 1, 2, 4, 5, 6]
    right_arrow_dex = [18, 19, 20, 22, 23, 24]
    brake_light_dex = [0, 1, 3, 4, 5, 7, 8, 16, 17, 19, 20, 21, 23, 24]
    night_light_dex = [9, 10, 11, 12]

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

        self.leds.off()

        self.left_turn_off_func = None
        self.right_turn_off_func = None
        self.night_light_off_func = None

    def left_turn_on(self, duration=0):
        self.left_turn_off_func = self.leds.flash(self.left_arrow_dex, orange,
                                                  self.turn_interval, duration)
        return self.left_turn_off_func

    def left_turn_off(self):
        if self.left_turn_off_func is not None:
            self.left_turn_off_func()
            self.left_turn_off_func = None

    def right_turn_on(self, duration=0):
        self.right_turn_off_func = self.leds.flash(self.right_arrow_dex, orange,
                                                   self.turn_interval, duration)
        return self.right_turn_off_func

    def right_turn_off(self):
        if self.right_turn_off_func is not None:
            self.right_turn_off_func()
            self.right_turn_off_func = None

    def brake_light_on(self, duration):
        self.leds[self.brake_light_dex] = red


    def brake_light_off(self):
        self.leds[self.brake_light_dex] = 0

    def night_light_on(self):
        """
        Flash safety lights at 5 Hz
        :return: A function that, when called, will stop the flashing
        """
        self.night_light_off_func = self.leds.flash(self.night_light_dex,
                                                    bright_white,
                                                    self.night_light_interval)
        return self.night_light_off_func

    def night_light_off(self):
        """
        Turn of the safety lights, if on
        :return: None
        """
        if self.night_light_off_func is not None:
            self.night_light_off_func()
        self.night_light_off_func = None


# Self-test
if __name__ == '__main__':
    me = BikeLEDs()
    while True:
        me.left_turn_on(5)
        sleep(6)
        me.right_turn_on(5)
        sleep(6)
        me.brake_light_on(3)
        sleep(5)
        me.night_light_on(10)
        sleep(1)
        me.left_turn_on(5)
        sleep(6)
        me.right_turn_on(5)
        sleep(6)
        me.brake_light_on()
        sleep(3)
        me.brake_light_off()
        me.night_light_off()
        sleep(10)
