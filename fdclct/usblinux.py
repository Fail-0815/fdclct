""" Linux related implementation of USB code """
import usb.core
import usb.util
from . import usbadapter

class Usblinux(usbadapter.Usbadapter):
    """ Class that implements Linux specific USB handling """

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

    def __del__(self):
        # This is needed to release interface, otherwise attach_kernel_driver fails
        # due to "Resource busy"
        usb.util.dispose_resources(self.dev)

        # In theory you don't even need to reattach the kernel.
        # The kernel does not use this part of the device
        if self.reattach:
            self.dev.attach_kernel_driver(self.rgbinterface)