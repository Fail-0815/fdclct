""" Class to control the lights """
from platform import system
from colour import Color
import drevo.usbadapter as usbadapter
from drevo import keyboard as keymap
import random
if system() == 'Windows':
    import drevo.usbwindows as usbwindows
else:
    import drevo.usblinux as usblinux

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
        Sets random colors for each key.
        
        TODO: Change  random color calculation. 
        Maybe use hsl instead rgb and only use intensive colors.
        """
        fullcolorstr = ''
        for _ in range(0,72):
            color = Color(rgb=(random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)))
            fullcolorstr += color.hex_l[1:]
        self.adapter.sendhex(fullcolorstr)

    def setkey(self, keycode, color):
        """
        Sets the color of a single key.
        """

        if not isinstance(color, Color):
            color = Color(color)
        
        oldcolorstr = self.adapter.gethex()
        fullcolorstr = ''
        for i in range(0,72):
            if i == keycode:
                colstr = color.hex_l[1:]
            else:
                colstr = oldcolorstr[i*6:(i+1)*6]
            fullcolorstr += colstr
        self.adapter.sendhex(fullcolorstr)

    def setkeys(self, keycodes, colors):
        """ 
        Sets the colors of multiple keys at once
        TODO
        """
        pass

    def getcolors(self):
        colstring = self.adapter.gethex()
        inv_keymap = {v: k for k,v in keymap.items()}
        keycolors = {}
        for i in range(72):
            keycolors[inv_keymap[i]] = (colstring[i*6:i*6+2],colstring[i*6+2:i*6+4],colstring[i*6+4:i*6+6])
        return keycolors
