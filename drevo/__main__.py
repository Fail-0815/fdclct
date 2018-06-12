"""
Parses and validates inputs for command line use
"""

import random
import argparse
import time
import drevo.keylights as keylights


keyboard = {}
keyboard["ESC"] = 0
keyboard["F1"] = 1
keyboard["F2"] = 2
keyboard["F3"] = 3
keyboard["F4"] = 4
keyboard["F5"] = 5
keyboard["F6"] = 6
keyboard["F7"] = 7
keyboard["F8"] = 8
keyboard["F9"] = 9
keyboard["F0"] = 10
keyboard["F"] = 11
keyboard["F2"] = 12
keyboard["DEL"] = 13
keyboard["TAB"] = 14
keyboard["Q"] = 15
keyboard["W"] = 16
keyboard["E"] = 17
keyboard["R"] = 18
keyboard["T"] = 19
keyboard["Y"] = 20
keyboard["U"] = 21
keyboard["I"] = 22
keyboard["O"] = 23
keyboard["P"] = 24
keyboard["["] = 25
keyboard["]"] = 26
keyboard["BACKSLASH"] = 27
keyboard["CAPS"] = 28
keyboard["A"] = 29
keyboard["S"] = 30
keyboard["D"] = 31
keyboard["F"] = 32
keyboard["G"] = 33
keyboard["H"] = 34
keyboard["J"] = 35
keyboard["K"] = 36
keyboard["L"] = 37
keyboard[";"] = 38
keyboard["'"] = 39
keyboard["ENTER"] = 40
keyboard["SHIFT"] = 41
keyboard["Z"] = 42
keyboard["X"] = 43
keyboard["C"] = 44
keyboard["V"] = 45
keyboard["B"] = 46
keyboard["N"] = 47
keyboard["M"] = 48
keyboard[","] = 49
keyboard["."] = 50
keyboard["/"] = 51
keyboard["SHIFT2"] = 52
keyboard["CTRL"] = 53
keyboard["WIN"] = 54
keyboard["ALT"] = 55
keyboard["SPACEBAR"] = 56
keyboard["ALT"] = 57
keyboard["FN"] = 58
keyboard["CTX"] = 59
keyboard["CTRL2"] = 60
keyboard["INS"] = 61
keyboard["HM"] = 62
keyboard["PU"] = 63
keyboard["DEL"] = 64
keyboard["END"] = 65
keyboard["PD"] = 66
keyboard["UP"] = 67
keyboard["LEFT"] = 68
keyboard["DOWN"] = 69
keyboard["RIGHT"] = 70

def main():
    """
        Parse arguments and start application appropriately
    """
    # TODO: Add parameter for a json object mapping key -> color
    parse = argparse.ArgumentParser(
        description='Change light color for switches of the Drevo Calibur keyboard')
    parse.add_argument("color")
    parse.add_argument("key", nargs='?')
    args = parse.parse_args()

    lightctl = keylights.Keylights()
    
    if args.key is not None:
        # Set light for specific key
        lightctl.setkey(keyboard[args.key],args.color)
    else:
        # Set light for all keys
        lightctl.setall(args.color)
        


if __name__ == "__main__":
    main()
