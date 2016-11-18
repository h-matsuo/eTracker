#!/usr/bin/python
# coding: UTF-8

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

from datetime import datetime
import signal
import sys

from read_from_ina219 import ReadFromINA219
from lib.utils import Utils
from lib.utils import OutputController

def SIGINTHandler(num, frame):
    global out_control
    out_control.stop()

def getOutputData():
    global ina219
    time = datetime.today()
    ina219_data = Utils.getINA219Data(ina219)
    return Utils.formatToJSON(Utils.formatDatetime(time), ina219_data)

def main():

    # Get command line args (argv)
    argv = sys.argv

    # Show usage if lack of argv
    if len(argv) < 2:
        print "Usage: python eTracker.py <delay_time> [<output_file>]"
        exit()

    # Set delay time
    delay_time = float(argv[1])

    # Set output file path
    output_path = None
    if len(argv) > 2:
        output_path = argv[2]

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

if __name__ == "__main__":
    main()
