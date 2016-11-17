#!/usr/bin/python
# coding: UTF-8

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

from datetime import datetime
import json
import sys

# NOTE: Format of time must follow: 2016/11/01-10:05:20.010
def calculateDiffInSec(previous_time, current_time):
    previous_millisec = previous_time[previous_time.rfind('.')+1:]
    previous_datetime = datetime.strptime(previous_time[:previous_time.rfind('.')], "%Y/%m/%d-%H:%M:%S")
    current_millisec = current_time[current_time.rfind('.')+1:]
    current_datetime = datetime.strptime(current_time[:current_time.rfind('.')], "%Y/%m/%d-%H:%M:%S")
    return (current_datetime - previous_datetime).total_seconds() - 1 + ((1000 + int(current_millisec) - int(previous_millisec)) / 1000.0)

def main():

    # Get command line args (argv)
    argv = sys.argv

    # Show usage if lack of argv
    if len(argv) < 4:
        print "Usage: python analyze.py <input_path> <begin_time> <end_time>"
        exit()

    # Set input file path
    input_path = argv[1]

    # Set begin time of analyzation
    begin_time = argv[2]

    # Set end time of analyzation
    end_time = argv[3]

    # Open input file and parse JSON data
    fin = open(input_path, "r")
    input_data = json.load(fin)

    # Start analyzation

    status = 0  # 0: Ignore this entry beause it is before the begin time 
                # 1: The first of target entry (#1)
                # 2: Target entries (#2 - #(N-1))
                # 3: The last of target entry (#N)
                # 4: Ignore this entry beause it is after the end time

    consumed_joules = 0.0

    for entry in input_data:

        current_time = entry["date"]
        current_power = entry["data"]["power_mw"]

        if current_time == begin_time:
            status = 1
        elif current_time == end_time:
            status = 3

        if status == 0 or status == 4:
            continue

        if status == 1:
            previous_time = current_time
            previous_power = current_power
            status = 2
            continue

        # Caluclate diff of time in sec
        diff_s = calculateDiffInSec(previous_time, current_time)

        # Calculate area of trapezoid
        # NOTE: The measure of current_power is [mW]
        consumed_joules += ((current_power / 1000.0) + (previous_power / 1000.0)) * diff_s / 2.0

        previous_time = current_time
        previous_power = current_power

        if status == 3:
            status = 4
            continue

    # End analyzation

    # Close input file
    fin.close()

    # Print calculated value
    print "Consumed: %f [J]" % consumed_joules

if __name__ == "__main__":
    main()
