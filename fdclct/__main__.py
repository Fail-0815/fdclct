"""
Parses and validates inputs for command line use
"""

import argparse

from . import keylights

def main():
    """
        Parse arguments and start application appropriately
    """
    parse = argparse.ArgumentParser(description='Change light color for switches of the Drevo Calibur keyboard')
    x = keylights.Keylights()
    x.allgreen()


if __name__ == "__main__":
    main()