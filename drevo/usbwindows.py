""" Windows related implementation of USB code """
import pywinusb.hid as hid
import usbadapter

class Usbwindows(usbadapter.Usbadapter):
    """ Class that implements Windows specific USB handling """
    def __init__(self):
        devices = hid.HidDeviceFilter(vendor_id=0x0483).get_devices()
        dev = devices[1]
