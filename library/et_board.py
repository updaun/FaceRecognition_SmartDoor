# -*- coding: utf-8 -*-
"""
 * ID     : et_board
 * Author : SCS
 * Date : 2020.10.24 : SCS : Draft
 * Date : 2020.10.22
"""

import requests
import json
import time

class et_board():
    """et_board ip 주소를 먼저 설정하고 사용한다."""

    def __init__(self, ip, debug=False):
        super(et_board, self).__init__()
        self.ip = ip
        self.url = 'http://' + ip  + '/'
        self.debug = debug

    def log(self, str):
        if (self.debug == True):
            print(str)

    def run_digital(self, pin, value1):
        URL = self.url
        URL += 'run?device=digital&pin=' + str(pin) + '&value1=' + str(value1)
        response = requests.get(URL)
        self.log(response.text)

    def run_servo(self, value1):
        URL = self.url
        URL += 'run?device=servo&value1=' + str(value1)
        response = requests.get(URL)
        self.log(response.text)

    def get_analog(self):
        URL = self.url
        URL += 'get?device=analog'
        response = requests.get(URL)
        self.log(response.text)
        return response.text

    def get_digital(self):
        URL = self.url
        URL += 'get?device=digital'
        response = requests.get(URL)
        self.log(response.text)
        return response.text

    def parse_value(self, str, pin):
        json_data = json.loads(str)
        value1 = json_data[pin]
        return value1


# et_board initialize
#et = et_board("192.168.0.160", True)

# run digital
#et.run_digital(2,1)
#et.run_digital(2,0)

# run servo
#et.run_servo(0)
#time.sleep(1)
#et.run_servo(180)
#time.sleep(1)
#et.run_servo(90)

# get get_analog
#val_string = et.get_analog()
#print (et.parse_value(val_string, "A0"))

# get digital
#val_string = et.get_digital()
#print (et.parse_value(val_string, "D9"))
