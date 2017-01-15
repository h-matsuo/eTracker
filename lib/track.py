#!/usr/bin/python
# coding: UTF-8

"""
Implementation of command: track
"""

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

from datetime import datetime
import json
import os
import signal
import sys
import time

from lib.read_from_ina219 import ReadFromINA219
from lib.utils import Utils

class TrackController:
    """
    Control tracking INA219
    """

    def __init__(self):
        """
        Constructor
        """
        # Initialize output data
        self.__tracked_data = []
        # Stop flag for tracking
        self.__stop_flag = False
        # Default values
        self.__interval = 0.02
        self.__out_file = None
        # Connect to INA219 chip
        self.__ina219 = ReadFromINA219()

    def setInterval(self, interval):
        """
        Set tracking interval

        @param interval Tracking interval
        """
        self.__interval = interval

    def setOutputFilename(self, filename):
        """
        Set filename to write output

        @param filename Filename to write output
        """
        self.__out_file = filename

    def start(self):
        """
        Start tracking
        """
        self.__track()

    def stop(self):
        """
        Stop tracking
        """
        self.__stop_flag = True
        if self.__out_file != None:
            fout = open(self.__out_file, "w")
            json.dump(self.__tracked_data, fout, indent = 2, separators = (",", ": "))
            fout.close()

    def __track(self):
        """
        Track INA219 repeatedly
        """
        while not self.__stop_flag:
            begin = datetime.today()
            tracked_data = self.__getTrackedData()
            if self.__out_file != None:
                self.__tracked_data.append(tracked_data)
            else:
                print json.dumps(tracked_data, indent = 2, separators = (",", ": "))
            end = datetime.today()

            diff = self.__interval - (end - begin).total_seconds()
            if diff < 0: diff = 0
            time.sleep(diff)

    def __getTrackedData(self):
        """
        Get data from INA219

        @return Tracked data
        """
        return {
            "date": Utils.formatDatetime(datetime.today()),
            "power_w": self.__ina219.getPower_W()
        }

def SIGINTHandler(signum, frame):
    """
    Signal SIGINT handler
    """
    global controller
    controller.stop()

def exec_track(flags):
    """
    Execute command: track

    @param flags Result of parsing argv
    """

    # Check if executed as root
    if os.getuid() != 0:
        sys.stderr.write("Sorry, sub-command 'track' must be executed as root user.\n")
        sys.exit(1)

    # Instantiate controller
    global controller
    controller = TrackController()

    # Set interval
    controller.setInterval(flags.interval)

    # Set output filename
    if flags.out_file != None:
        controller.setOutputFilename(flags.out_file)

    # Print message
    print "Start tracking..."
    print 'Press "Ctrl + c" to quit.'

    # Handle SIGINT
    signal.signal(signal.SIGINT, SIGINTHandler)

    # Start tracking
    controller.start()
