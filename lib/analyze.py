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

class SearchForBoundary:

    def __init__(self, begin_time, end_time, json_data):
        self.begin_time = begin_time
        self.end_time   = end_time
        self.json_data  = json_data
        self.begin_index = -1
        self.end_index   = -1
        self.__search()

    def getBeginIndex(self):
        return self.begin_index

    def getEndIndex(self):
        return self.end_index

    def __search(self):

        # Search for begin_index
        for i in range(0, len(self.json_data)):

            diff_begin_s = calculateDiffInSec(self.begin_time, self.json_data[i]["date"])

            if diff_begin_s < 0:
                continue

            if i == 0:
                self.begin_index = i    # 0
            else:
                diff_tmp_s = calculateDiffInSec(self.begin_time, self.json_data[i - 1]["date"])
                if diff_begin_s < abs(diff_tmp_s):
                    self.begin_index = i
                else:
                    self.begin_index = i - 1

            break

        # Search for end_index
        for i in range(0, len(self.json_data)):

            diff_end_s = calculateDiffInSec(self.end_time, self.json_data[i]["date"])

            if diff_end_s < 0:
                continue

            if i == len(self.json_data) - 1:
                self.end_index = i      # len(self.json_data) - 1
            else:
                diff_tmp_s = calculateDiffInSec(self.end_time, self.json_data[i - 1]["date"])
                if diff_begin_s < abs(diff_tmp_s):
                    self.end_index = i
                else:
                    self.end_index = i - 1

            break

def analyze(argv):

    # Print error message if lack of argv
    if len(argv) < 3:
        print "ERROR: analyze: indicate options;"
        print "       See 'python eTracker.py help'."
        exit()

    # Set input file path
    input_path = argv[0]

    # Set begin time of analyzation
    begin_time = argv[1]

    # Set end time of analyzation
    end_time = argv[2]

    # Open input file and parse JSON data
    fin = open(input_path, "r")
    json_data = json.load(fin)

    # Print info
    print "Checking start/end date..."

    # Calculate boundary of begin and end for analyzation
    boundary = SearchForBoundary(begin_time, end_time, json_data)

    # Print info
    print "Begin date of analyzation: %s" % json_data[boundary.getBeginIndex()]["date"]
    print "  End date of analyzation: %s" % json_data[boundary.getEndIndex()]["date"]

    # Print info
    print "Calculating power..."

    # Calculate power with the trapezoidal approximation

    consumed_joules = 0.0
    previous_time  = json_data[boundary.getBeginIndex()]["date"]
    previous_power = json_data[boundary.getBeginIndex()]["data"]["power_w"]

    for i in range(boundary.getBeginIndex() + 1, boundary.getEndIndex() + 1):

        current_time  = json_data[boundary.getEndIndex()]["date"]
        current_power = json_data[boundary.getEndIndex()]["data"]["power_w"]

        # Caluclate diff of time in sec
        diff_s = calculateDiffInSec(previous_time, current_time)

        # Calculate area of trapezoid
        consumed_joules += (current_power + previous_power) * diff_s / 2.0

        previous_time = current_time
        previous_power = current_power

    # Close input file
    fin.close()

    # Print calculated value
    print "Consumed power: %f [J]" % consumed_joules
