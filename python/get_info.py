#!/usr/bin/env python

# MIT License
#
# Copyright (c) [2016] [Okan Ulas Gezeroglu]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Brick info returns info about the printer modules.

import json

from ev3dev.auto import *


class BrickInfo:
    def __init__(self):
        self.status = ""

    @staticmethod
    def get_motor_info(motor):
        info = dict(connected='true', address=motor.address, duty_cyle=motor.duty_cycle, position=motor.position,
                    stop_command=motor.stop_command, polarity=motor.polarity)
        return info

    def get_info(self):

        # touch sensor
        try:
            touch_sensor = TouchSensor()
            touch_data = {
                'connected': 'true',
                'address': touch_sensor.address,
                'mode': touch_sensor.mode,
                'value': touch_sensor.value()
            }
        except:
            # There is no color sensor
            touch_data = {'connected': 'false'}

        # rail motor
        try:
            rail_motor = LargeMotor(OUTPUT_A)
            rail_data = self.get_motor_info(rail_motor)
        except:
            # There is no color sensor
            rail_data = {'connected': 'false'}

        # paper motor
        try:
            paper_motor = LargeMotor(OUTPUT_B)
            paper_data = self.get_motor_info(paper_motor)
        except:
            # There is no color sensor
            paper_data = {'connected': 'false'}

        # pen motor
        try:
            pen_motor = LargeMotor(OUTPUT_B)
            pen_data = self.get_motor_info(pen_motor)
        except:
            # There is no color sensor
            pen_data = {'connected': 'false'}

        self.status = {
            'rail_motor': rail_data,
            'paper_motor': paper_data,
            'pen_motor': pen_data,
            'touch_sensor': touch_data,
        }

        return json.dumps(self.status)
