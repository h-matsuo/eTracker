#!/usr/bin/python
# coding: UTF-8

"""
Utilities for internal implementation
"""

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

import json

class Utils:
    """
    Utility class for internal implementation
    """

    @staticmethod
    def printUsage():
        """
        Print usage to standard output
        """
        fin = open("usage.txt")
        for line in fin:
            print line.rstrip()
        fin.close()

    @staticmethod
    def formatDatetime(datetime_obj):
        """
        Receive a datetime.datetime object and format it like "2016/09/22-09:59:30.005"
    
        @param datetime_obj datetime.datetime object
        @return Formatted string
        """
        return datetime_obj.strftime("%Y/%m/%d-%H:%M:%S.") + "%03d" % (datetime_obj.microsecond // 1000)

    @staticmethod
    def getINA219Data(ina219_obj):
        """
        Get data from ReadFromINA219 object

        @param ina219_obj ReadFromINA219 object
        @return Got data in JSON format (dictionary)
        """
        return {
            "shunt_voltage_mv": ina219_obj.getShuntVoltage_mV(),
            "bus_voltage_v"   : ina219_obj.getBusVoltage_V(),
            "current_ma"      : ina219_obj.getCurrent_mA(),
            "power_w"         : ina219_obj.getPower_W()
        }

    @staticmethod
    def formatToJSON(time_string, ina219_data):
        """
        Format data to JSON string

        @param time_string Date and time 
        @param ina219_data Value returned from getINA219Data() function
        @return Formatted JSON string
        """
        return json.dumps({
            "date": time_string,
            "data": ina219_data
        }, indent = 2)
