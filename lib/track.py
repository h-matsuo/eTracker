#!/usr/bin/python
# coding: UTF-8

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

from datetime import datetime
import signal

from read_from_ina219 import ReadFromINA219
from utils import Utils
from utils import OutputController

def SIGINTHandler(num, frame):
    global out_control
    out_control.stop()

def getOutputData():
    global ina219
    time = datetime.today()
    ina219_data = Utils.getINA219Data(ina219)
    return Utils.formatToJSON(Utils.formatDatetime(time), ina219_data)

def track(argv):

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
