#!/usr/bin/python

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

# Lego printer is responsible of controlling 3 motors
# paper_motor controls the paper feed ( y axis )
# rail_motor controls the horizontal move ( x axis)
# pen_motor controls the pen up-down state (on - off)
# touch_sensor is used to calibrate the rail motor position.

import math
import time
from time import sleep

from ev3dev.auto import *

from draw_action import DrawAction


class LegoPrinter:
    def __init__(self):

        self.touch_sensor = TouchSensor()
        assert self.touch_sensor.connected

        self.rail_motor = LargeMotor(OUTPUT_A)
        assert self.rail_motor.connected

        self.paper_motor = LargeMotor(OUTPUT_B)
        assert self.paper_motor.connected

        self.pen_motor = MediumMotor(OUTPUT_C)
        assert self.pen_motor.connected

        # List of draw commands
        self.draw_list = []

        self.motors_calibrated = False
        self.x_units_to_cm = 1 / 1.1  # multiply with x value to convert to motor positions
        self.y_units_to_cm = 1 / 1.2  # multiply with y value to convert to motor positions

        self.is_drawing = False
        self.is_busy = False
        self.is_pen_up = False
        self.current_draw_Item = None
        self.prev_draw_Item = None
        self.pen_is_adjustable = True

    def reset_motors(self):
        self.reset_rail_motor()
        self.reset_paper_motor()
        self.reset_pen_motor()

    def reset_rail_motor(self):
        self.rail_motor.reset()
        self.rail_motor.stop_command = Motor.STOP_COMMAND_HOLD
        self.rail_motor.duty_cycle_sp = 50
        self.rail_motor.polarity = Motor.POLARITY_INVERSED

    def reset_paper_motor(self):
        self.paper_motor.reset()
        self.paper_motor.stop_command = Motor.STOP_COMMAND_HOLD
        self.paper_motor.duty_cycle_sp = 50
        self.paper_motor.polarity = Motor.POLARITY_INVERSED

    def reset_pen_motor(self):
        self.pen_motor.reset()
        self.pen_motor.stop_command = Motor.STOP_COMMAND_HOLD
        self.pen_motor.duty_cycle_sp = 50

    def force_stop(self):
        self.draw_list = []
        self.current_draw_Item = None
        self.prev_draw_Item = None
        self.pen_up()
        self.rail_motor.stop()
        self.paper_motor.stop()
        self.is_drawing = False
        self.is_busy = False

    # Switch the pen motor adjustment state.
    # Pen motor can be adjusted in STOP_COMMAND_BRAKE state
    def switch_pen_state(self):
        if self.pen_is_adjustable is False:
            self.pen_is_adjustable = True
            self.pen_motor.stop_command = Motor.STOP_COMMAND_BRAKE
        else:
            self.pen_is_adjustable = True
            self.pen_motor.stop_command = Motor.STOP_COMMAND_HOLD

    def pen_up(self):
        if self.is_pen_up is False:
            self.is_pen_up = True
            self.pen_motor.run_to_abs_pos(position_sp=50, duty_cycles_sp=30)

    def pen_down(self):
        if self.is_pen_up is True:
            self.is_pen_up = False
            self.pen_motor.run_to_abs_pos(position_sp=0, duty_cycles_sp=30)

    # Draws the elements in the draw_list
    def draw(self, draw_list):
        if self.is_busy:
            return
        self.is_busy = True

        Sound.speak('Drawing Started').wait()

        self.draw_list = draw_list
        self.draw_list.reverse()
        self.current_draw_Item = self.draw_list.pop()

        self.start_draw()
        self.pen_up()

        self.is_busy = False
        Sound.speak('Drawing Finished').wait()

    def draw_next_item(self):
        if len(self.draw_list) > 0:

            if (self.current_draw_Item.t == DrawAction.PEN_MOVE):
                self.prev_draw_Item = DrawAction(self.current_draw_Item.t, self.current_draw_Item.x,
                                             self.current_draw_Item.y)
            self.current_draw_Item = self.draw_list.pop()
        else:
            self.prev_draw_Item = None
            self.current_draw_Item = None

    def start_draw(self):
        print "Start Drawing"
        while self.current_draw_Item is not None:
            if self.current_draw_Item.t == DrawAction.PEN_UP:
                self.pen_up()
                while self.pen_motor.position < 49:
                    time.sleep(0.1)

            elif self.current_draw_Item.t == DrawAction.PEN_DOWN:
                self.pen_down()
                while self.pen_motor.position > 2:
                    sleep(0.1)

            elif self.current_draw_Item.t == DrawAction.PEN_MOVE:

                to_x = math.floor(self.current_draw_Item.x * self.x_units_to_cm)
                to_y = math.floor(self.current_draw_Item.y * self.y_units_to_cm)

                ratio = 1
                dcsp = 30
                x_dcsp = dcsp
                y_dcsp = dcsp

                if self.prev_draw_Item is not None:
                    dx = abs(self.current_draw_Item.x - self.prev_draw_Item.x)
                    dy = abs(self.current_draw_Item.y - self.prev_draw_Item.y)
                else:
                    dx = abs(to_x - self.rail_motor.position)
                    dy = abs(to_y - self.paper_motor.position)

                if dx > 0 and dx > 0:
                    ratio = dy / dx

                if ratio > 1:  # y component is longer
                    x_dcsp = dcsp / ratio
                    if (x_dcsp < 10):
                        x_dcsp = 10
                        y_dcsp = 10 * ratio

                elif 1 > ratio > 0:  # x component is longer
                    y_dcsp = dcsp / ratio
                    if (y_dcsp < 10):
                        y_dcsp = 10
                        x_dcsp = 10 * ratio

                x_dcsp = math.ceil(max(0, (min(100, x_dcsp))))
                y_dcsp = math.ceil(max(0, (min(100, y_dcsp))))

                # print "Ratio:", ratio, "X DCSP:", x_dcsp, "Y DCSP:", y_dcsp, "ToX:", to_x, "ToY:", to_y, "DX:", dx, "DY:", dy
                print "CX:", self.current_draw_Item.x, "CY:", self.current_draw_Item.y
                if self.prev_draw_Item is not None:
                    print "PX", self.prev_draw_Item.x, "PY:", self.prev_draw_Item.y

                x_completed = True
                y_completed = True

                if dx > 0:
                    x_completed = False
                    self.rail_motor.run_to_abs_pos(position_sp=to_x, duty_cycle_sp=x_dcsp)

                if dy > 0:
                    y_completed = False
                    self.paper_motor.run_to_abs_pos(position_sp=to_y, duty_cycle_sp=y_dcsp)

                start_time = time.time()
                while self.current_draw_Item is not None and (x_completed is False or y_completed is False):

                    if x_completed is False:
                        dx = abs(to_x - self.rail_motor.position)
                        if dx <= 1:
                            x_completed = True
                            self.rail_motor.stop()

                    if y_completed is False:
                        dy = abs(to_y - self.paper_motor.position)
                        if dy <= 1:
                            y_completed = True
                            self.paper_motor.stop()

                    if time.time() - start_time > 15:
                        break

                    sleep(0.1)

            self.draw_next_item()

    def manual_paper_feed_inc(self, direction):
        self.paper_motor.run_forever(duty_cycle_sp=30 * direction)

    def manual_paper_feed_inc_stop(self):
        self.paper_motor.stop()

    def manual_paper_feed(self, direction):
        self.paper_motor.run_forever(duty_cycle_sp=50 * direction)

    def stop_paper_feed(self):
        self.reset_paper_motor()

    def manual_move_x(self, direction):
        self.rail_motor.run_forever(duty_cycle_sp=30 * direction)

    def manual_stop_x(self):
        self.rail_motor.stop()

    def switch_pen_pos(self):
        if self.is_pen_up is True:
            self.pen_down()
        else:
            self.pen_up()

    def calibrate(self):
        if self.is_busy:
            return
        self.is_busy = True

        Sound.speak('Calibrating Motor Positions').wait()

        self.rail_motor.polarity = Motor.POLARITY_INVERSED
        self.rail_motor.run_forever(duty_cycle_sp=-50)

        wait_for_button_press = True
        while wait_for_button_press:
            if self.touch_sensor.value():
                wait_for_button_press = False
                self.rail_motor.stop()
                self.reset_rail_motor()
                self.rail_motor.run_to_abs_pos(position_sp=100, duty_cycle_sp=100)

        self.motors_calibrated = True
        self.is_busy = False

        Sound.speak('Calibrating Motor Positions Completed').wait()

        return "Calibration Completed"

    def set_pen_position(self):
        self.pen_motor.reset()
        self.pen_motor.stop_command = Motor.STOP_COMMAND_BRAKE
        self.pen_motor.duty_cycle_sp = 100

    def feed_paper(self):

        if self.is_busy:
            return
        self.is_busy = True

        timer = 0
        max_time = 1000

        self.paper_motor.run_forever(duty_cycle_sp=-50)

        waiting_paper = True
        while waiting_paper:
            timer += 1
            if timer > max_time:
                waiting_paper = False
                print "User not provided the paper on time.. Quiting"
                self.is_busy = False
                return

        self.paper_motor.run_to_rel_pos(position_sp=-40, duty_cycle_sp=10)
        sleep(0.5)

        self.reset_paper_motor()

        self.is_busy = False
        Sound.speak('Paper Feeded').wait()
