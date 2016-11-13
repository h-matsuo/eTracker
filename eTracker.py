#!/usr/bin/python
# coding: UTF-8

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

from datetime import datetime
import signal
import sys

from read_from_ina219 import ReadFromINA219
from lib.utils import Utils
from lib.utils import OutputController

# Get command line args (argv)
argv = sys.argv

if len(argv) < 2:
    print "Usage: ./eTracker.py <delay_time> [<out_path>]"
    exit()

# Set delay time from argv
delay_time = float(argv[1])

# Set output file name
out_path = None
if len(argv) > 2:
    out_path = argv[2]

# Connect to INA219 chip
ina219 = ReadFromINA219()


def SIGINTHandler(num, frame):
    out_control.stop()

def getOutputData():
    time = datetime.today()
    ina219_data = Utils.getINA219Data(ina219)
    return Utils.formatToJSON(Utils.formatDatetime(time), ina219_data)


signal.signal(signal.SIGINT, SIGINTHandler)


out_control = OutputController()
out_control.setOutputPath(out_path)
out_control.setDelayTime(delay_time)
out_control.setJSONFactory(getOutputData)

out_control.start()


def main():
    # print "This is main method"
    pass

if __name__ == "__main__":
    main()
