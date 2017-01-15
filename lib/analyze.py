#!/usr/bin/python
# coding: UTF-8

"""
Implementation of command: analyze
"""

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

import json

from lib.utils import Utils

class SearchForBoundary:
    """
    Calculate the boundary of section to analyze
    """

    def __init__(self, begin_time, end_time, json_data):
        """
        Constructor

        @param begin_time Begin time of section to analyze
        @param end_time   End time of section to analyze
        @param json_data  JSON data created by track command
        """
        self.begin_time = begin_time
        self.end_time   = end_time
        self.json_data  = json_data
        self.begin_index = -1
        self.end_index   = -1
        self.__search()

    def getBeginIndex(self):
        """
        Return begin index of section to analyze

        @return Begin index 
        """
        return self.begin_index

    def getEndIndex(self):
        """
        Return end index of section to analyze

        @return End index 
        """
        return self.end_index

    def __search(self):
        """
        Calculate the boundary
        """

        # Search for begin_index
        if self.begin_time == "-":
            self.begin_index = 0
        else:
            for i in range(0, len(self.json_data)):

                diff_begin_s = Utils.calculateDiffInSec(self.begin_time, self.json_data[i]["date"])

                if diff_begin_s < 0:
                    continue

                if i == 0:
                    self.begin_index = i    # 0
                else:
                    diff_tmp_s = Utils.calculateDiffInSec(self.begin_time, self.json_data[i - 1]["date"])
                    if diff_begin_s < abs(diff_tmp_s):
                        self.begin_index = i
                    else:
                        self.begin_index = i - 1

                break

        # Search for end_index
        if self.end_time == "-":
            self.end_index = len(self.json_data) - 1
        else:
            for i in range(0, len(self.json_data)):

                diff_end_s = Utils.calculateDiffInSec(self.end_time, self.json_data[i]["date"])

                if diff_end_s < 0:
                    continue

                if i == len(self.json_data) - 1:
                    self.end_index = i      # len(self.json_data) - 1
                else:
                    diff_tmp_s = Utils.calculateDiffInSec(self.end_time, self.json_data[i - 1]["date"])
                    if diff_end_s < abs(diff_tmp_s):
                        self.end_index = i
                    else:
                        self.end_index = i - 1

                break

def exec_analyze(flags):
    """
    Execute command: analyze

    @param flags Result of parsing argv
    """

    # Set input filename
    input_filename = flags.in_file

    # Set the beginning of the section of time to analyze
    begin_time = flags.begin

    # Set the end of the section of time to analyze
    end_time = flags.end

    # Open input file and parse JSON data
    fin = open(input_filename, "r")
    json_data = json.load(fin)

    # Calculate boundary of begin and end for analyzation
    boundary = SearchForBoundary(begin_time, end_time, json_data)

    # Print info
    print "Beginning of the section: %s" % json_data[boundary.getBeginIndex()]["date"]
    print "      End of the section: %s" % json_data[boundary.getEndIndex()]["date"]

    # Print duration
    print "Duration: %.3f [sec]" % Utils.calculateDiffInSec(json_data[boundary.getBeginIndex()]["date"], json_data[boundary.getEndIndex()]["date"])

    # Print info
    print "Calculating..."

    # Calculate energy consumption with the trapezoidal approximation

    consumed_joules = 0.0
    previous_time  = json_data[boundary.getBeginIndex()]["date"]
    previous_power = json_data[boundary.getBeginIndex()]["power_w"]

    for i in range(boundary.getBeginIndex() + 1, boundary.getEndIndex() + 1):

        current_time  = json_data[i]["date"]
        current_power = json_data[i]["power_w"]

        # Caluclate diff of time in sec
        diff_s = Utils.calculateDiffInSec(previous_time, current_time)

        # Calculate area of trapezoid
        consumed_joules += (current_power + previous_power) * diff_s / 2.0

        previous_time  = current_time
        previous_power = current_power

    # Close input file
    fin.close()

    # Print calculated value
    print "Total energy consumption: %f [J]" % consumed_joules
