"""import time
from machine import I2C
import math"""

import machine
from network import WLAN
wlan = WLAN(mode=WLAN.STA)

__version__ = '0.0.1'

class WiFi:
    """ class for handling WiFi connection """

    def __init__(self):
        pass


    def connectwifi(ssid, pwd):
        nets = wlan.scan()
        status='Not connected'
        for net in nets:
            if net.ssid == ssid:
                """print('Network found!')"""
                wlan.connect(net.ssid, auth=(net.sec, pwd), timeout=5000)
                while not wlan.isconnected():
                    machine.idle() # save power while waiting
                    status='Connected'
                """print('WLAN connection succeeded!')"""
                break
        return status
