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

        self.num_leds = num_leds

        # Open the file
        self._spi = open(dev_file, 'wb')

        # Make the underlying byte array
        self.bytes = bytearray(3 * self.num_leds)

        # Initialize LED objects (could be better)
        self.leds = []
        for n in range(num_leds):
            self.leds.append(self.LED(self, 3 * n))

        # Write out bytes to turn off LEDs
        self.refresh()

    class LED:
        def __init__(self, chain, pos):
            self._red = 0
            self._green = 0
            self._blue = 0
            self._chain = chain  # Reference to the parent object (not great)
            self.pos = pos

        @property
        def red(self):
            return self._red

        @red.setter
        def red(self, value):
            if 0 <= value <= 255:
                self._red = value
            self._chain.bytes[self.pos] = int(value)
            self._chain.refresh()

        @property
        def green(self):
            return self._green

        @green.setter
        def green(self, value):
            if 0 <= value <= 255:
                self._green = value
            self._chain.bytes[self.pos + 1] = int(value)
            self._chain.refresh()

        @property
        def blue(self):
            return self._blue

        @blue.setter
        def blue(self, value):
            if 0 <= value <= 255:
                self._blue = value
            self._chain.bytes[self.pos + 2] = int(value)
            self._chain.refresh()

    def refresh(self):
        """Send signal out to LEDs from byte array"""
        self._spi.write(self.bytes)
        self._spi.flush()

    def off(self):
        """Reset all bytes to zero and turn off LEDs"""
        self.bytes = bytearray(3 * self.num_leds)
        self.refresh()


def demo():
    """Simple demo to test and show off"""
    leds = WS2801LED()
    for n in range(60000):
        if n % 3 == 0:
            leds.leds[n % leds.num_leds].red = \
                (leds.leds[n % leds.num_leds].red + n) % 17
            leds.leds[n % leds.num_leds].green /= 2
            leds.leds[n % leds.num_leds].blue /= 2
        elif n % 3 == 1:
            leds.leds[n % leds.num_leds].green = \
                (leds.leds[n % leds.num_leds].green + n) % 17
            leds.leds[n % leds.num_leds].red /= 2
            leds.leds[n % leds.num_leds].blue /= 2
        else:
            leds.leds[n % leds.num_leds].blue = \
                (leds.leds[n % leds.num_leds].blue + n) % 17
            leds.leds[n % leds.num_leds].green /= 2
            leds.leds[n % leds.num_leds].red /= 2
        sleep(0.001)
    leds.off()


if __name__ == '__main__':
    demo()
