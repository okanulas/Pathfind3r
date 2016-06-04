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

# SVG parser supports only absolute path items for now. Content can be extended
# to support rectangle, circle and other shapes as well.

import math
import xml.sax

from draw_action import DrawAction


class SvgParser(xml.sax.ContentHandler):

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.current_data = ""
        self.draw_list = []
        self.draw_list.append(DrawAction(t=DrawAction.PEN_UP))

    def startElement(self, tag, attributes):
        self.current_data = tag
        if tag == "path":
            path = attributes["d"]
            path_data = path.split(' ')
            moved_to_start_pos = False
            start_pos_x = 0
            start_pos_y = 0
            self.draw_list.append(DrawAction(t=DrawAction.PEN_UP))

            for item in path_data:
                sitem = item.strip()

                if sitem == 'M' or sitem == 'C':
                    continue

                if sitem == 'Z':
                    self.draw_list.append(DrawAction(DrawAction.PEN_MOVE, start_pos_x, start_pos_y))
                    continue

                pos = item.split(',')
                x = math.floor(float(pos[0]))
                y = math.floor(float(pos[1]))

                if moved_to_start_pos is False:
                    moved_to_start_pos = True
                    start_pos_x = x
                    start_pos_y = y
                    self.draw_list.append(DrawAction(DrawAction.PEN_MOVE, x, y))
                    self.draw_list.append(DrawAction(t=DrawAction.PEN_DOWN))

                self.draw_list.append(DrawAction(DrawAction.PEN_MOVE, x, y))
