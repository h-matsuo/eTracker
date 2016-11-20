#!/usr/bin/python
# coding: UTF-8

"""
Implementation of command: track
"""

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

from datetime import datetime
import signal
import threading

from lib.read_from_ina219 import ReadFromINA219
from lib.utils import Utils

class OutputController:
    """
    Control string output and repeatedly-tracking
    """

    def __init__(self):
        """
        Constructor
        """
        self.is_first_write = True

    def setOutputPath(self, path):
        """
        Set output file path for tracked data

        @param path Output file path
        """
        self.output_path = path
        if self.output_path != None:
            self.fout = open(self.output_path, "w")

    def setDelayTime(self, delay_time):
        """
        Set delay time of getting data repeatedly

        @param delay_time Delay time
        """
        self.delay_time = delay_time

    def setJSONFactory(self, factory_func):
        """
        Set JSON factory function to prepare for output data

        @param factory_func JSON factory function
        """
        self.JSON_factory_func = factory_func

    def start(self):
        """
        Start tracking
        """
        self.write("[")
        self.output()

    def stop(self):
        """
        Stop tracking
        """
        self.thread_id.cancel()
        self.write("\n]\n")
        if self.output_path != None:
            self.fout.close()
        # exit()

    def output(self):
        """
        Execute myself recursively to track
        """
        self.thread_id = threading.Timer(self.delay_time, self.output)
        self.thread_id.start()
        if self.is_first_write:
            out_str = ""
            self.is_first_write = False
        else:
            out_str = ","
        out_str += "\n" + self.JSON_factory_func()
        self.write(out_str)

    def write(self, str):
        """
        Write string to standard output or file

        @param str Output string
        """
        if self.output_path == None:
            print str
        else:
            self.fout.write(str)
            self.fout.flush()

def SIGINTHandler(num, frame):
    """
    SIGINT signal handler
    """
    global out_control
    out_control.stop()

def getOutputData():
    """
    Prepare for output data

    @return Output data
    """
    global ina219
    time = datetime.today()
    ina219_data = Utils.getINA219Data(ina219)
    return Utils.formatToJSON(Utils.formatDatetime(time), ina219_data)

def track(argv):
    """
    Execute command: track

    @param argv Command options
    """

    # Print error message if no argv indicated
    if len(argv) < 1:
        print "ERROR: track: indicate delay time in [sec];"
        print "       See 'python eTracker.py help'."
        exit()

    # Parse argv

    # Set delay time
    delay_time = float(argv[0])

    # Set output file path
    output_path = None
    if len(argv) > 1:
        output_path = argv[1]

    # Connect to INA219 chip
    global ina219
    ina219 = ReadFromINA219()

    # Handle signal SIGINT
    signal.signal(signal.SIGINT, SIGINTHandler)

    # Instantiate controller
    global out_control
    out_control = OutputController()

    # Configuration
    out_control.setOutputPath(output_path)
    out_control.setDelayTime(delay_time)
    out_control.setJSONFactory(getOutputData)

    # Print message
    print "Start tracking..."
    print 'Press "Ctrl + c" to quit.'

    # Start tracking
    out_control.start()
