# fdclct
Free Drevo Calibur Lighting Control Tool

*Warning: at the moment just very little actually works*

## What is this?
This tool is to set the color of the RGB LEDs in the Drevo Calibur keyboard. By default this keyboard can be set to 8 different colors per key, but the Windows software by Drevo ([you can get from here](drevo.net/product/keyboard/calibur)) supports color selection per key with 24 bit color. Sadly it is closed source and Windows exclusive. So this project aims to reverse engineer the USB communication and implement a free version of the same tool to enable platform independent keyboard RGB glory.

## Requirements
### Software 
This package is written for Python 3.

Packages:
* [PyUSB 1.0+](https://github.com/pyusb/pyusb) (under Ubuntu also available via ```sudo apt install python3-usb```)
* [colour 0.1.5](https://github.com/vaab/colour)

### Hardware
The Drevo Calibur keyboard. I have the 71 key version, but the 72 key version should work as well. If not, please leave an issue.

Furthermore i run the keyboard with firmware V3.4 for the 71 key edition. This should be equivalent to firmware V2.3 for the 72 key version. Both come with the date 20170908. I don't know if this works for earlier versions. While I'm pretty sure it does not work for the initial factory firmware, it might work for intermediate versions. Please leave an issue or pr if you know.

## Restrictions
Due to the nature of the protocol the Calibur uses to set lighting it is not possible to hack fluid animations. This is due to the fact that for every single change in the configuration of the lighting a new colormap for every key is transfered to the keyboard. This process can take over half a second.