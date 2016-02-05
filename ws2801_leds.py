#!/usr/bin/env python3
"""This class interfaces with a chain of WS2801 LED drivers connected to the
BeagleBone Black's SPI bus."""

__author__ = 'Kristian Sims'

from time import sleep


class WS2801LED:
    def __init__(self, num_leds=25, dev_file='/dev/spidev1.0'):
        """
        Opens the file object to connect to the LEDs and initializes objects
        """

        # Open the file
        self.leds = open(dev_file, 'wb')
        self.num_leds = num_leds
        self.bytes = bytearray(3 * self.num_leds)

        # Write out bytes to turn off LEDs
        self.refresh()

    def refresh(self):
        """Send signal out to LEDs from byte array"""
        self.leds.write(self.bytes)
        self.flush()

    def all_leds_off(self):
        """Reset all bytes to zero and turn off LEDs"""
        self.bytes = bytearray(3 * self.num_leds)
        self.refresh()


def demo():
    """Simple demo to test and show off"""
    leds = WS2801LED()
    for n in range(60000):
        leds.bytes[3 * n % leds.num_leds] += n % 7
        leds.bytes[3 * n % leds.num_leds] %= 17
        leds.refresh()
        sleep(0.001)


if __name__ == '__main__':
    demo()
