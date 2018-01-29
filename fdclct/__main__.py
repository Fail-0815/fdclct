"""
Parses and validates inputs for command line use
"""

import argparse

from . import keylights

def main():
    """
        Parse arguments and start application appropriately
    """
    # TODO: Add parameter for a json object mapping key -> color
    # TODO: Add parameter to change only a single key
    parse = argparse.ArgumentParser(
        description='Change light color for switches of the Drevo Calibur keyboard')
    parse.add_argument("color")
    args = parse.parse_args()
    lightctl = keylights.Keylights()
    lightctl.setall(args.color)


if __name__ == "__main__":
    main()
    