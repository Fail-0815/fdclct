""" Class to control the lights """
import usb.core
import usb.util

class Keylights:
    """
    Primary (maybe only) class of the fdclct project.
    This tries to find an attached Drevo Calibur keyboard and
    opens a connection to the device.

    Throws ValueError if something is wrong, description in message.

    see: Keylights.setall() and Keylights.setkey() for practical uses
    """
    initRGBmsg = bytearray.fromhex('00e1'+'00'*62)
    endRGBmsg = bytearray.fromhex('e6'*64)


    def __init__(self):
        dev = usb.core.find(
            idVendor=0x0483, # STMicroelectronics
            idProduct=0x4010 # Drevo Calibur Keyboard
        )
        if dev is None:
            # Device not present, or user is not allowed to access device.
            raise ValueError("Keyboard not present or insufficient permissions")

        conf = dev.get_active_configuration()
        interface = conf[(1, 0)]
        writergbendpoint = usb.util.find_descriptor(
            interface,
            bEndpointAddress=0x1
        )
        if writergbendpoint is None:
            raise ValueError("Endpoint not found")
        self.writergbendpoint = writergbendpoint
        self.writeout = writergbendpoint.write

    def allgreen(self):
        """
        Sets the color of all keys to green.
        In the future this will have parameters for RGB input.
        """
        color = '00FF00'
        fullcolorstr = color * 72
        # TODO: construct this string from some kind of list.
        # said list should have a corresponding map solving keynames to ids.
        self.__sendhexstring(fullcolorstr)

    def setkey(self, keyname, color):
        """
        Sets the color of a single key. Massive TODO.
        """
        pass

    def __sendhexstring(self, hexstr):
        error = ValueError("Valid hexstring with excatly 432 characters needed")
        if len(hexstr) != 432:
            raise error
        try:
            bytearray.fromhex(hexstr)
        except ValueError:
            raise error
        header = '00e0'
        msglen = '3d'
        msglenlast = '21'

        self.writeout(self.initRGBmsg)
        for i in range(0, 3):
            self.writeout(
                bytearray.fromhex(header + msglen + hexstr[i*122:(i+1)*122])
                )
        self.writeout(
            bytearray.fromhex(header + msglenlast + hexstr[366:432] + '00' * 28)
            )
        self.writeout(self.endRGBmsg)
