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
    initwritemsg = bytearray.fromhex('00e1'+'00'*62)
    initreadmsg = bytearray.fromhex('00e2'+'00'*62)
    endmsg = bytearray.fromhex('e6'*64)

    
    def write(self, string):
        """ Write is implemented platform specific """
        pass

    def read(self, size):
        """ Read is implemented platform specific """
        pass

    def sendhex(self, hexstr):
        """
        Send a message with exactly 216 bytes as color message

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

        self.write(self.initwritemsg)
        for i in range(0, 3):
            self.write(
                bytearray.fromhex(header + msglen + hexstr[i*122:(i+1)*122])
            )
        self.write(
            bytearray.fromhex(header + msglenlast +
                              hexstr[366:432] + '00' * 28)
        )
        self.write(self.endmsg)

    def gethex(self):
        """
        Recieve a message representing the current color values of the keyboard
        """
        self.write(self.initreadmsg)
        responses = bytearray()
        for _ in range(4):
            response = self.read(64)
            length = response[2]
            message = response[3:length+3]
            responses = responses + message
        _ = self.read(64) # Here comes the end message. should be self.endmsg
        return responses.hex()
        