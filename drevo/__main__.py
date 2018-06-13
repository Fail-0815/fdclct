"""
Parses and validates inputs for command line use
"""

import random
import argparse
import time
import drevo.keylights as keylights
from drevo import keyboard



def main():
    """
        Parse arguments and start application appropriately
    """
    # TODO: Add parameter for a json object mapping key -> color
    parse = argparse.ArgumentParser(
        description='Change light color for switches of the Drevo Calibur keyboard')
    parse.add_argument("-c", "--color", nargs='?')
    parse.add_argument("-k", "--key", nargs='?')
    parse.add_argument("-r", "--random", action="store_true")
    parse.add_argument("-R", "--allrandom", action="store_true")
    parse.add_argument("-v", "--verbose", action="store_true")
    args = parse.parse_args()

    lightctl = keylights.Keylights()
    
    if not args.allrandom and args.color is None and not args.random and not args.verbose:
        parse.print_usage()

    if args.allrandom:
        lightctl.setrandom()

    if args.random:
        args.color = "#" + "".join(random.sample("0123456789abcdef", 6))

    if args.color is not None:
        if args.key is not None:
            # Set light for specific key
            lightctl.setkey(keyboard[args.key], args.color)
        else:
            # Set light for all keys
            lightctl.setall(args.color)
        
    if args.verbose:
        print(lightctl.getcolors())

if __name__ == "__main__":
    main()
