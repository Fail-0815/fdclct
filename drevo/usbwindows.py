""" Windows related implementation of USB code """
from pywinusb import hid
import usbadapter

class Usbwindows(usbadapter.Usbadapter):
    """ Class that implements Windows specific USB handling """
    def __init__(self):
        # TODO: implement. Documentation at https://github.com/rene-aguirre/pywinusb/wiki/Introduction
        devices = hid.HidDeviceFilter(vendor_id=0x0483, product_id=0x4010).get_devices()
        if not devices:
            raise ValueError("Device not found")
        dev = devices[1]
