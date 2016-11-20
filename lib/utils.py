#!/usr/bin/python
# coding: UTF-8

"""
Utilities for internal implements
"""

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

import json
import threading

class Utils:

    @staticmethod
    def printUsage():
        fin = open("usage.txt")
        for line in fin:
            print line.rstrip()
        fin.close()

    @staticmethod
    def formatDatetime(datetime_obj):
        """
        Receive a datetime.datetime object and format it like "2016/09/22-09:59:30.005"
    
        @param datetime_obj datetime.datetime obj
        @return formatted string
        """
        return datetime_obj.strftime("%Y/%m/%d-%H:%M:%S.") + "%03d" % (datetime_obj.microsecond // 1000)

    @staticmethod
    def getINA219Data(ina219_obj):
        return {
            "shunt_voltage_mv": ina219_obj.getShuntVoltage_mV(),
            "bus_voltage_v"   : ina219_obj.getBusVoltage_V(),
            "current_ma"      : ina219_obj.getCurrent_mA(),
            "power_w"         : ina219_obj.getPower_W()
        }

    @staticmethod
    def formatToJSON(time_string, ina219_data):
        return json.dumps({
            "date": time_string,
            "data": ina219_data
        }, indent = 2)


class OutputController:

    def __init__(self):
        self.is_first_write = True

    def setOutputPath(self, path):
        self.output_path = path
        if self.output_path != None:
            self.fout = open(self.output_path, "w")

    def setDelayTime(self, time):
        self.delay_time = time

    def setJSONFactory(self, factory_func):
        self.JSON_factory_func = factory_func

    def start(self):
        self.write("[")
        self.output()

    def stop(self):
        self.thread_id.cancel()
        self.write("\n]\n")
        if self.output_path != None:
            self.fout.close()
        #exit()

    def output(self):
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
        if self.output_path == None:
            print str
        else:
            self.fout.write(str)
            self.fout.flush()
