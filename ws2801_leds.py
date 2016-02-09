#!/usr/bin/env python3
"""This class interfaces with a chain of WS2801 LED drivers connected to the
BeagleBone Black's SPI bus."""

from collections import namedtuple
from time import sleep

__author__ = 'Kristian Sims'

# This defines a tuple 'LED' that can be indexed with .red, .green, etc. It's
#  not as useful as I hoped, though, because tuples are immutable, so I think
#  my goal of having a line like "leds[9].red = 50" won't work. This possibly
#  could be achieved by making a subclass with fixed __slots__.
LED = namedtuple('LED', 'red green blue')


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

        # Initialize LED objects
        self._leds = [LED(0, 0, 0)] * self.num_leds

        # Write out bytes to turn off LEDs
        self.refresh()

    def __getitem__(self, key):
        """
        Return the current stored values of the indicated LED
        :param key: Index of the LED
        :return: A named tuple (red, green, blue) with the intensities for
        the LED
        """

        return self._leds[key]

    def __setitem__(self, key, value):
        """
        Set the indicated LED to value, and refresh the display if needed.
        :param key: Index of the LED
        :param value: New value for the LED, either a 3-tuple or single integer.
        :return: None
        """

        # Set LED as packed int (must be less than 2^24)
        if type(value) is int:
            if not 0 <= value < 2 ** 24:
                raise ValueError("LED value must be a 24-bit positive number")
            self._leds[key] = (
                (value >> 16) & 0xFFFF,
                (value >> 8) & 0xFFFF,
                value & 0xFFFF)
        # Set LED as tuple of ints (must be less than 2^8)
        elif type(value) is tuple and len(value) is 3:
            if all([n < 256 for n in value]):
                self._leds[key] = value
            else:
                raise ValueError
        else:
            raise ValueError

        # Update the byte array
        self._bytes[(3 * key):(3 * (key + 1))] = self._leds[key]

        # Update the display if frame_lock is not set
        if not self._frame_hold:
            self.refresh()

    def hold_frame(self):
        self._frame_hold = True

    def release_frame(self):
        if self._frame_hold:
            self.refresh()
        self._frame_hold = False

    def refresh(self):
        """Send signal out to LEDs from byte array"""
        self._spi.write(self._bytes)
        self._spi.flush()

    def off(self):
        """Reset all bytes to zero and turn off LEDs"""
        self._leds = [LED(0, 0, 0)] * self.num_leds
        self._bytes = bytearray(3 * self.num_leds)
        self.refresh()


def demo():
    """Simple demo to test and show off"""
    leds = WS2801LEDS()
    for n in range(12000):
        r, g, b = leds[n % leds.num_leds]
        if n % 3 == 0:
            r = (r + n) % 17
        elif n % 3 == 1:
            g = (g + n) % 17
        else:
            b = (b + n) % 17
        leds[n % leds.num_leds] = (r, g, b)
        sleep(0.005)
    leds.off()


if __name__ == '__main__':
    demo()
