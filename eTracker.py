#!/usr/bin/python
# coding: UTF-8

"""
eTracker -- Utility Tool for Raspberry Pi

Track energy consumption of your device with Adafruit INA219 chip.
"""

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

import sys

from lib.utils import Utils

def main():

    # Parse command line args
    result = Utils.parseArgv()

    # Execute track sub-command
    if result.sub_command == "track":
        from lib.track import exec_track
        exec_track(result)
    # Execute analyze sub-command
    elif result.sub_command == "analyze":
        from lib.analyze import exec_analyze
        exec_analyze(result)

if __name__ == "__main__":
    main()
