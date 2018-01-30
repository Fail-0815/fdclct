""" Class to control the lights """
from platform import system
from colour import Color
from . import usbadapter
if system() == 'Windows':
    from . import usbwindows
else:
    from . import usblinux

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

    def setkey(self, keyname, color):
        """
        Sets the color of a single key. Massive TODO.
        """
        pass
