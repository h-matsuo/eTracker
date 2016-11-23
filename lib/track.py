#!/usr/bin/python
# coding: UTF-8

"""
Implementation of command: track
"""

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

import collections
from datetime import datetime
import json
import signal
import threading

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
        self.firstData = True
        # Default output: standard output
        self.output_path = None
        # Connect to INA219 chip
        self.ina219 = ReadFromINA219()
        # Handle SIGINT
        signal.signal(signal.SIGINT, self.__SIGINTHandler)

    def setInterval(self, interval):
        """
        Set interval between tracking

        @param interval Interval
        """
        self.interval = interval

    def setOutputPath(self, output_path):
        """
        Set file path for writing tracked data

        @param output_path Output file path
        """
        self.output_path = output_path
        self.fout = open(self.output_path, "w")

    def start(self):
        """
        Start tracking
        """
        self.__write("[\n")
        self.__track()

    def stop(self):
        """
        Stop tracking
        """
        self.thread_id.cancel()
        self.__write("\n]")
        if self.output_path != None:
            self.fout.close()

    def __write(self, data):
        """
        Write data to standard output or file

        @param str Output string
        """
        if self.output_path != None:
            self.fout.write(data)
        else:
            print data, # Print without "\n"

    def __track(self):
        """
        Track INA219 repeatedly
        """
        self.thread_id = threading.Timer(self.interval, self.__track)
        self.thread_id.start()
        # Get JSON data
        data = self.__getJSONData(datetime.today(), self.ina219).split("\n")
        # Write data delimiter (",")
        if self.firstData == True:
            self.firstData = False
        else:
            self.__write(",\n")
        # Format and write JSON data
        for i in range(0, len(data)):
            self.__write("  " + data[i].rstrip())
            if i != len(data) - 1:
                self.__write("\n")

    def __getJSONData(self, datetime_obj, ina219_obj):
        """
        Prepare for data to be output in JSON format

        @param datetime_obj datetime.datetime object
        @param ina219_obj ReadFromINA219 object
        @return Data to be output in JSON format
        """
        return json.dumps({
            "date": Utils.formatDatetime(datetime_obj),
            "data": {
                "bus_voltage_v": ina219_obj.getBusVoltage_V(),
                "current_ma"   : ina219_obj.getCurrent_mA(),
                "power_w"      : ina219_obj.getPower_W()
            }
        }, indent = 2)

    def __SIGINTHandler(self, num, frame):
        """
        Signal SIGINT handler
        """
        self.stop()

def exec_track(argv):
    """
    Execute command: track

    @param argv Command options
    """

    # Print error message if no argv specified
    if len(argv) < 1:
        print "ERROR: track: specify interval in [sec];"
        print "       See 'python eTracker.py help'."
        exit()

    # Instantiate contoroller
    controller = TrackController()

    # Parse argv

    # Set interval
    controller.setInterval(float(argv[0]))

    # Set output file path
    if len(argv) > 1:
        controller.setOutputPath(argv[1])

    # Print message
    print "Start tracking..."
    print 'Press "Ctrl + c" to quit.'

    # Start tracking
    controller.start()
