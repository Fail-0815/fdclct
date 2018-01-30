""" General platform independent USB related hassle """
from abc import ABC

class Usbadapter(ABC):
    # This is 1 because we're (at the moment) only interested in
    # the interface with id 1. This manages the color-messages.
    rgbinterface = 1
    # Interface 0 yields keypress-interrupts
    # Interface 2 is of unknown purpose atm. Perhaps macros or firmware update.
    # I suspect the latter

    # Device Specific USB message header
    initRGBmsg = bytearray.fromhex('00e1'+'00'*62)
    endRGBmsg = bytearray.fromhex('e6'*64)

    def write(self, string):
        """ Write is implemented platform specific """
        pass

    def sendhex(self, hexstr):
        """
        Send a Message with exactly 216 bytes as color message

        Keyword arguments:
        hexstr -- Message in a string in it's hexadecimal representation
        """
        error = ValueError(
            "Valid hexstring with excatly 432 characters needed")
        if len(hexstr) != 432:
            raise error
        try:
            bytearray.fromhex(hexstr)
        except ValueError:
            raise error
        header = '00e0'
        msglen = '3d'
        msglenlast = '21'

        self.write(self.initRGBmsg)
        for i in range(0, 3):
            self.write(
                bytearray.fromhex(header + msglen + hexstr[i*122:(i+1)*122])
            )
        self.write(
            bytearray.fromhex(header + msglenlast +
                              hexstr[366:432] + '00' * 28)
        )
        self.write(self.endRGBmsg)