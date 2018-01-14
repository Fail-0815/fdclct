import usb.core
import usb.util

class Keylights:
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
            # match the first OUT endpoint
            custom_match= \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT
        )
        if writergbendpoint is None:
            raise ValueError("Endpoint not found")

        self.writergbendpoint = writergbendpoint

    def allgreen(self):
        pass
