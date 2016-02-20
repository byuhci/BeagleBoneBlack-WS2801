#!/usr/bin/env python3
"""
This class interfaces with a chain of WS2801 LED drivers connected to the
BeagleBone Black's SPI bus.

Kristian Sims, BYU Physical Computing 2016
"""

from collections import namedtuple
from time import sleep
from threading import Event, Thread

__author__ = 'Kristian Sims'

# This defines a tuple 'LED' that can be indexed with .red, .green, etc. It's
#  not as useful as I hoped, though, because tuples are immutable, so I think
#  my goal of having a line like "leds[9].red = 50" won't work. This possibly
#  could be achieved by making a subclass with fixed __slots__.
LED = namedtuple('LED', 'red green blue')

# Some colors to use
soft_yellow = LED(16, 18, 0)
orange = LED(80, 15, 0)
red = LED(120, 0, 0)
bright_white = LED(200, 200, 200)


class WS2801LEDS:
    def __init__(self, num_leds=25, dev_file='/dev/spidev1.0'):
        """
        Opens the file object to connect to the LEDs and initializes objects
        """

        self.num_leds = num_leds
        self._frame_hold = False

        # Open the file
        self._spi = open(dev_file, 'wb')

        # Make the underlying byte array
        self._bytes = bytearray(3 * self.num_leds)

        # Write out bytes to turn off LEDs
        self.refresh()

    def __getitem__(self, key):
        """
        Return the current stored values of the indicated LED
        :param key: Index of the LED
        :return: A named tuple (red, green, blue) with the intensities for
        the LED
        """
        return LED(
            self._bytes[3 * key],
            self._bytes[3 * key + 1],
            self._bytes[3 * key + 2])

    def __setitem__(self, key, value):
        """
        Set the indicated LED to value, and refresh the display if needed.
        :param key: Index of the LED, or a list or set of indices
        :param value: New value for the LED, either a 3-tuple or single integer.
        :return: None
        """

        # Try to map for multiple assignments
        if type(key) in {list, set}:
            temp = self._frame_hold
            self.hold_frame()
            for k in key:
                self.__setitem__(k, value)
            if not temp:  # Don't release if it was already held
                self.release_frame()
        # Set LED as packed int (must be less than 2^24)
        elif type(value) is int:
            if not 0 <= value < 2 ** 24:
                raise ValueError('LED value must be a 24-bit positive number.')
            self._bytes[3 * key] = (value >> 16) & 0xFF
            self._bytes[3 * key + 1] = (value >> 8) & 0xFF
            self._bytes[3 * key + 2] = value & 0xFF
        # Set LED as tuple of ints (must be less than 2^8)
        elif type(value) in {tuple, LED} and len(value) is 3:
            if all([n < 256 and type(n) is int for n in value]):
                self._bytes[3 * key:3 * (key + 1)] = value
            else:
                raise ValueError('LED value must be a tuple of 3 integers '
                                 'less than 255.')
        else:
            raise ValueError('Unrecognized format for LED value')

        # Update the display if frame_lock is not set
        if not self._frame_hold:
            self.refresh()

    def hold_frame(self):
        self._frame_hold = True

    def release_frame(self):
        if self._frame_hold:
            self.refresh()
        self._frame_hold = False

    def refresh(self, wait_for_latch=True):
        """
        Send signal out to LEDs from byte array
        :param wait_for_latch: Wait until the frame latches. Set to false if
        there's no possibility that refresh() will be called again very soon.
        :return: None
        """
        self._spi.write(self._bytes)
        self._spi.flush()
        if wait_for_latch:
            sleep(0.001)

    def off(self):
        """Reset all bytes to zero and turn off LEDs"""
        self._bytes = bytearray(3 * self.num_leds)
        self.refresh()

    def flash(self, dex, color, interval):
        """
        Flash some LEDs in a separate thread
        :param dex: List containing the indices of the LEDs to flash
        :param color: Color to light the LEDs
        :param interval: Time for LEDs to be on/off (half-period)
        :return: A function that, when called, will stop the flashing thread
        """
        stopped = Event()

        def loop():
            while True:
                if stopped.wait(interval):
                    break
                else:
                    self[dex] = color
                if stopped.wait(interval):
                    break
                else:
                    self[dex] = 0
            self[dex] = 0

        Thread(target=loop, daemon=True).start()

        return stopped.set


def demo():
    """Simple demo to test and show off"""
    from math import sin, pi
    leds = WS2801LEDS()
    t = 0
    while True:
        t += 0.01
        leds.hold_frame()
        for n in range(25):
            leds[n] = (int(25 * (1 + sin(t - 2 * pi * n / 25))),
                       int(25 * (1 + sin(t - 2 * pi * (n / 25 + 1 / 3)))),
                       int(25 * (1 + sin(t - 2 * pi * (n / 25 + 2 / 3)))))
        leds.release_frame()

if __name__ == '__main__':
    demo()
