""" Windows related implementation of USB code """
import usb.core
import usb.util
import drevo.usbadapter as usbadapter

class Usbwindows(usbadapter.Usbadapter):
    """ Class that implements Windows specific USB handling """
    def __init__(self):
        backend = usb.backend.libusb1.get_backend(find_library=lambda x: "libusb-1.0.dll")
        dev = usb.core.find(
            idVendor=0x0483,  # STMicroelectronics
            idProduct=0x4010,  # Drevo Calibur Keyboard
            backend=backend
        )
        if dev is None:
            # Device not present, or user is not allowed to access device.
            raise ValueError(
                "Keyboard not present or insufficient permissions")

        #self.reattach = False
        #if dev.is_kernel_driver_active(self.rgbinterface):
        #    self.reattach = True
        #    dev.detach_kernel_driver(self.rgbinterface)
        conf = dev.get_active_configuration()
        interface = conf[(self.rgbinterface, 0)]
        self.dev = dev

        writergbendpoint = usb.util.find_descriptor(
            interface,
            bEndpointAddress=0x1
        )
        if writergbendpoint is None:
            raise ValueError("Endpoint for writing not found")
        self.writergbendpoint = writergbendpoint
        self.write = writergbendpoint.write
        
        readrgbendpoint = usb.util.find_descriptor(
            interface,
            bEndpointAddress=0x84
        )
        if readrgbendpoint is None:
            raise ValueError("Endpoint for reading not found")
        self.readrgbendpoint = readrgbendpoint
        self.read = readrgbendpoint.read
        

    def __del__(self):
        # This is needed to release interface, otherwise attach_kernel_driver fails
        # due to "Resource busy"
        usb.util.dispose_resources(self.dev)

        # In theory you don't even need to reattach the kernel.
        # The kernel does not use this part of the device
        #if self.reattach:
        #    self.dev.attach_kernel_driver(self.rgbinterface)
