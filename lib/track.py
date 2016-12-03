#!/usr/bin/python
# coding: UTF-8

"""
Implementation of command: track
"""

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

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
        # Whether exporting data to the external file or not
        self.does_export = False
        # Initialize output data
        self.tracked_data = []
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
        self.does_export = True

    def start(self):
        """
        Start tracking
        """
        self.__track()

    def stop(self):
        """
        Stop tracking
        """
        self.thread_id.cancel()
        if self.does_export:
            fout = open(self.output_path, "w")
            json.dump(self.tracked_data, fout, indent = 2, separators = (",", ": "))
            fout.close()

    def __track(self):
        """
        Track INA219 repeatedly
        """
        begin = datetime.today()
        if self.does_export:
            self.tracked_data.append(self.__getTrackedData())
        else:
            print json.dumps(self.__getTrackedData(), indent = 2, separators = (",", ": "))
        end = datetime.today()

        diff = self.interval - (end - begin).total_seconds()
        if diff < 0: diff = 0
        self.thread_id = threading.Timer(diff, self.__track)
        self.thread_id.start()

    def __getTrackedData(self):
        """
        Prepare for data
        """
        return {
            "date": Utils.formatDatetime(datetime.today()),
            "power_w": self.ina219.getPower_W()
        }

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
