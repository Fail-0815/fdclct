""" Class to control the lights """
import usb.core
import usb.util
from colour import Color

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

    # This is 1 because we're (at the moment) only interested in
    # the interface with id 1. This manages the color-messages.
    rgbinterface = 1
    # Interface 0 yields keypress-interrupts
    # Interface 2 is of unknown purpose atm. Perhaps macros or firmware update.
    # I suspect the latter

    def __init__(self):
        dev = usb.core.find(
            idVendor=0x0483,  # STMicroelectronics
            idProduct=0x4010  # Drevo Calibur Keyboard
        )
        if dev is None:
            # Device not present, or user is not allowed to access device.
            raise ValueError(
                "Keyboard not present or insufficient permissions")

        self.reattach = False
        if dev.is_kernel_driver_active(self.rgbinterface):
            self.reattach = True
            dev.detach_kernel_driver(self.rgbinterface)
        conf = dev.get_active_configuration()
        interface = conf[(self.rgbinterface, 0)]
        writergbendpoint = usb.util.find_descriptor(
            interface,
            bEndpointAddress=0x1
        )
        if writergbendpoint is None:
            raise ValueError("Endpoint not found")
        self.writergbendpoint = writergbendpoint
        self.write = writergbendpoint.write
        self.dev = dev

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
        self.__sendhexstring(fullcolorstr)

    def setkey(self, keyname, color):
        """
        Sets the color of a single key. Massive TODO.
        """
        pass

    def __sendhexstring(self, hexstr):
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

    def __del__(self):
        # This is needed to release interface, otherwise attach_kernel_driver fails
        # due to "Resource busy"
        usb.util.dispose_resources(self.dev)

        # In theory you don't even need to reattach the kernel.
        # The kernel does not use this part of the device
        if self.reattach:
            self.dev.attach_kernel_driver(self.rgbinterface)
