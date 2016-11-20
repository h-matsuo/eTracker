#!/usr/bin/python
# coding: UTF-8

"""
eTracker -- Utility Tool for Raspberry Pi

Track energy consumption of your device with Adafruit INA219 chip.
"""

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

import sys

from lib.utils import Utils
from lib.track import track
from lib.analyze import analyze

def main():

    # Get command line args (argv)
    argv = sys.argv

    # Print usage if no commands indicated
    if len(argv) < 2:
        Utils.printUsage()
        exit()

    # Parse command

    # Command: help
    if argv[1] == "help":
        Utils.printUsage()
    # Command: track
    elif argv[1] == "track":
        del argv[0:2]
        track(argv)
    # Command: analyze
    elif argv[1] == "analyze":
        del argv[0:2]
        analyze(argv)
    # Invalid command indicated
    else:
        print "ERROR: %s: invalid command;" % argv[1]
        print "       See 'python eTracker.py help'."

if __name__ == "__main__":
    main()
