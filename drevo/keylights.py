""" Class to control the lights """
from platform import system
from colour import Color
import usbadapter
import random
if system() == 'Windows':
    import usbwindows
else:
    import usblinux

class Keylights:
    """
    Primary (maybe only) class of the fdclct project.
    This tries to find an attached Drevo Calibur keyboard and
    opens a connection to the device.

    Throws ValueError if something is wrong, description in message.

    see: Keylights.setall() and Keylights.setkey() for practical uses
    """
    adapter: usbadapter.Usbadapter = None

    def __init__(self):
        if system() == 'Windows':
            self.adapter = usbwindows.Usbwindows()
        else:
            self.adapter = usblinux.Usblinux()

    def setall(self, color):
        """
        Sets the color of all keys.

        The color parameter is a colour.Color object
        or alternatively a string interpretable by the colour.Color constructor
        """
        if not isinstance(color, Color):
            color = Color(color)
        colstr = color.hex_l[1:]
        fullcolorstr = colstr * 72
        # TODO: construct this string from some kind of list.
        # said list should have a corresponding map solving keynames to ids.
        self.adapter.sendhex(fullcolorstr)

    def setrandom(self):
        """
        Sets the color of a single key. Massive TODO.
        """
        fullcolorstr = ''
        for i in range(0,72):
            color = Color(rgb=(random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)))
            fullcolorstr += color.hex_l[1:]
        self.adapter.sendhex(fullcolorstr)
        pass

    def setkey(self, keycode, _color):
        """
        Sets the color of a single key. Massive TODO.
        """

        fullcolorstr = ''
        for i in range(0,72):
            if i == keycode:
                color = Color(rgb=[c / 255 for c in _color])
            else:
                color = Color(rgb=(0,0,0))
            fullcolorstr += color.hex_l[1:]

        self.adapter.sendhex(fullcolorstr)
        pass
