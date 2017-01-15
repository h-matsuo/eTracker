#!/usr/bin/python
# coding: UTF-8

"""
Utilities for internal implementation
"""

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

from argparse import ArgumentParser
from datetime import datetime

class Utils:
    """
    Utility class for internal implementation
    """

    prog_name = "eTracker.py"

    @staticmethod
    def getUsage():
        """
        Get usage
        """
        fin = open("usage.txt", "r")
        usage = fin.read()
        fin.close()
        return usage

    @staticmethod
    def formatDatetime(datetime_obj):
        """
        Receive a datetime.datetime object and format it like "2016/09/22-09:59:30.005"
    
        @param datetime_obj datetime.datetime object
        @return Formatted string
        """
        return datetime_obj.strftime("%Y/%m/%d-%H:%M:%S.") + "%03d" % (datetime_obj.microsecond // 1000)

    @staticmethod
    def calculateDiffInSec(previous_time, current_time):
        """
        Calculate diff time in [sec] between two time string
    
        NOTE: Format of time must follow: 2016/11/01-10:05:20.010
    
        @param previous_time Time string #1
        @param current_time  Time string #2
        @return Diff time in [sec]
        """
        previous_millisec = previous_time[previous_time.rfind('.')+1:]
        previous_datetime = datetime.strptime(previous_time[:previous_time.rfind('.')], "%Y/%m/%d-%H:%M:%S")
        current_millisec = current_time[current_time.rfind('.')+1:]
        current_datetime = datetime.strptime(current_time[:current_time.rfind('.')], "%Y/%m/%d-%H:%M:%S")
        return (current_datetime - previous_datetime).total_seconds() - 1 + ((1000 + int(current_millisec) - int(previous_millisec)) / 1000.0)

    @staticmethod
    def parseArgv():
        """
        Parse the command line arguments
    
        @return Result of parsing
        """
        parser = ArgumentParser(prog        = Utils.prog_name,
                                description = "track energy consumption of your device with Adafruit INA219 chip")
        subparsers = parser.add_subparsers(title = "sub-commands",
                                           dest  = "sub_command")

        parser_track = subparsers.add_parser("track",
                                             description = "track energy consumption of target device",
                                             help        = "track energy consumption")
        parser_track.add_argument("-i",
                                  type    = float,
                                  default = 0.02,
                                  metavar = "<interval>",
                                  dest    = "interval",
                                  help    = "set the tracking interval in [sec]; default = %(default)s")
        parser_track.add_argument("-o",
                                  metavar = "<filename>",
                                  dest    = "out_file",
                                  help    = "write output to %(metavar)s")

        parser_analyze = subparsers.add_parser("analyze",
                                               description = "analyze the json file created by track sub-command",
                                               help        = "analyze tracked data")
        parser_analyze.add_argument("in_file",
                                    metavar = "<filename>",
                                    help    = "specify the file to analyze")
        parser_analyze.add_argument("-b", "--begin",
                                    default = "-",
                                    metavar = "<begin_date>",
                                    dest    = "begin",
                                    help    = "specify the beginning of the section of time to analyze; if '-' is given, analyze from the beginning of the file; default = '%(default)s'")
        parser_analyze.add_argument("-e", "--end",
                                    default = "-",
                                    metavar = "<end_date>",
                                    dest    = "end",
                                    help    = "specify the end of the section of time to analyze; if '-' is given, analyze to the end of the file; default = '%(default)s'")

        result = parser.parse_args()

        return result
