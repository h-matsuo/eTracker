#!/usr/bin/python
# coding: UTF-8

"""
Read energy consumption data from INA219 chip
"""

__author__  = "Hiroyuki Matsuo <h-matsuo@ist.osaka-u.ac.jp>"

from subfact_pi_ina219.Subfact_ina219 import INA219

class ReadFromINA219:

    def __init__(self):

        self.ina219 = INA219()

        # Calibration to use Raspberry Pi 3 Model B
        self.ina219.ina219SetCalibration_RasPi3ModelB()
        # * If you want to use other devices,
        #   customize calibration settings in subfact_pi_ina219 library manually.
        # * See also the official Adafruit_INA219 library:
        #   https://github.com/adafruit/Adafruit_INA219

    def getShuntVoltage_mV(self):
        return self.ina219.getShuntVoltage_mV()

    def getBusVoltage_V(self):
        return self.ina219.getBusVoltage_V()

    def getCurrent_mA(self):
        return self.ina219.getCurrent_mA()

    def getPower_mW(self):
        return self.ina219.getPower_mW()
