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

# THE MAZE GENERATION ALGORITHM IS BASED ON THE PYTHON CODE AT
# https://rosettacode.org/wiki/Maze_generation . I made some
# modifications to support the my lego drawing system.

from random import shuffle, randrange

from draw_action import DrawAction


class Cell:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.v = False
        self.pre = None
        self.n = []


def make_maze(w=10, h=10):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+  "
            if yy == y:
                ver[y][max(x, xx)] = "   "
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    return s, hor, ver


def create_grid(w, h, n):
    temp_list = []
    for x in range(w):
        temp_list.append([])
        for y in range(h):
            temp_list[x].append(n)
    return temp_list


def parse_maze(w, h, gs, s, sh, sw):
    rw = w
    rh = h
    sy = 100
    grid_size = gs
    sx = (1650 - (w * grid_size)) * 0.5

    print("Parsing..")
    print(s)
    hor = create_grid(w + 1, h + 1, 0)
    ver = create_grid(w + 1, h + 1, 0)
    grid = create_grid(w, h, 0)

    print(len(sh[0]))
    rows = len(sh)
    cols = len(sh[0])
    for row in xrange(rows):
        for col in xrange(cols):
            if sh[row][col] == "+--":
                hor[row][col] = 1

    rows = len(sw)
    for row in xrange(rows):
        for col in xrange(len(sw[row])):
            if sw[row][col] == "|  ":
                ver[row][col] = 1

    draw_list = []
    draw_list.append(DrawAction(DrawAction.PEN_UP))
    draw_list.append(DrawAction(DrawAction.PEN_MOVE, sx, sy))
    draw_list.append(DrawAction(DrawAction.PEN_DOWN))
    draw_list.append(DrawAction(DrawAction.PEN_MOVE, sx, sy))
    draw_list.append(DrawAction(DrawAction.PEN_MOVE, sx + rw * grid_size, sy))
    draw_list.append(DrawAction(DrawAction.PEN_MOVE, sx + rw * grid_size, sy + (rh - 1) * grid_size))
    draw_list.append(DrawAction(DrawAction.PEN_UP))
    draw_list.append(DrawAction(DrawAction.PEN_MOVE, sx + rw * grid_size, sy + rh * grid_size))
    draw_list.append(DrawAction(DrawAction.PEN_DOWN))
    draw_list.append(DrawAction(DrawAction.PEN_MOVE, sx, sy + rh * grid_size))
    draw_list.append(DrawAction(DrawAction.PEN_MOVE, sx, sy + grid_size))
    draw_list.append(DrawAction(DrawAction.PEN_UP))

    rows = len(hor)
    cols = len(hor[0])
    for row in xrange(rows):
        prev_pos = False
        for col in xrange(cols):
            if 0 < row < rows - 1:
                if hor[row][col] == 1:
                    if prev_pos is False:
                        prev_pos = True
                        draw_list.append(
                                DrawAction(DrawAction.PEN_MOVE, sx + (col * grid_size), sy + (row * grid_size)))
                        draw_list.append(DrawAction(DrawAction.PEN_DOWN))
                else:
                    if prev_pos is True:
                        draw_list.append(
                                DrawAction(DrawAction.PEN_MOVE, sx + (col * grid_size), sy + (row * grid_size)))
                        draw_list.append(DrawAction(DrawAction.PEN_UP))
                    prev_pos = False

            if col == cols - 1 and prev_pos is True:
                draw_list.append(DrawAction(DrawAction.PEN_MOVE, sx + (col * grid_size), sy + (row * grid_size)))
                draw_list.append(DrawAction(DrawAction.PEN_UP))

    rows = len(ver)
    cols = len(ver[0])
    for col in xrange(cols):
        prev_pos = False
        for row in xrange(rows):
            if 0 < col < cols - 1:
                if ver[row][col] == 1:
                    if prev_pos is False:
                        prev_pos = True
                        draw_list.append(
                                DrawAction(DrawAction.PEN_MOVE, sx + (col * grid_size), sy + (row * grid_size)))
                        draw_list.append(DrawAction(DrawAction.PEN_DOWN))
                else:
                    if prev_pos is True:
                        prev_pos = False
                        draw_list.append(
                                DrawAction(DrawAction.PEN_MOVE, sx + (col * grid_size), sy + (row * grid_size)))
                        draw_list.append(DrawAction(DrawAction.PEN_UP))

            if row == row - 2 and prev_pos is True:
                draw_list.append(DrawAction(DrawAction.PEN_MOVE, sx + (col * grid_size), sy + (row * grid_size)))
                draw_list.append(DrawAction(DrawAction.PEN_UP))

    grid = []
    for x in range(w):
        grid.append([])
        for y in range(h):
            cell = Cell(x, y)

            l = ver[y][x]
            r = ver[y][x + 1]
            u = hor[y][x]
            d = hor[y + 1][x]

            if l == 0 and x > 0:
                cell.n.append([x - 1, y])
            if r == 0 and x < w - 1:
                cell.n.append([x + 1, y])
            if u == 0 and y > 0:
                cell.n.append([x, y - 1])
            if d == 0 and y < h - 1:
                cell.n.append([x, y + 1])
            grid[x].append(cell)

    start_cell = grid[0][0]
    end_cell = grid[w - 1][h - 1]

    search_list = [start_cell]

    def solve(current_list):

        while len(current_list) > 0:
            item = current_list.pop()

            item.v = True
            for n in item.n:
                ncell = grid[n[0]][n[1]]
                if ncell.v is False:
                    ncell.pre = item
                    current_list.append(ncell)
            if item.x == end_cell.x and item.y == end_cell.y:
                solved = []
                solved_cell = item
                solved.append(item)
                while solved_cell.pre is not None:
                    solved_cell = solved_cell.pre
                    solved.append(solved_cell)
                return solved
        return []

    result = solve(search_list)
    result.reverse()

    prev_pos = None

    for r in result:
        print ">>", r.x, r.y
        if prev_pos is None:
            draw_list.append(DrawAction(DrawAction.PEN_UP))
            draw_list.append(DrawAction(DrawAction.PEN_MOVE, sx + (r.x - 1) * grid_size + grid_size * 0.5,
                                        sy + r.y * grid_size + grid_size * 0.5))
            draw_list.append(DrawAction(DrawAction.PEN_DOWN))
            draw_list.append(DrawAction(DrawAction.PEN_MOVE, sx + r.x * grid_size + grid_size * 0.5,
                                        sy + r.y * grid_size + grid_size * 0.5))


        else:
            px = sx + r.x * grid_size + grid_size * 0.5
            py = sy + r.y * grid_size + grid_size * 0.5
            prev_x = sx + prev_pos.x * grid_size + grid_size * 0.5
            prev_y = sy + prev_pos.y * grid_size + grid_size * 0.5

            if prev_pos.x - r.x == 0:
                if r.y - prev_pos.y > 0:
                    py1 = prev_y + grid_size * 0.33
                    py2 = prev_y + grid_size * 0.33 * 2
                else:
                    py1 = prev_y - grid_size * 0.33
                    py2 = prev_y - grid_size * 0.33 * 2

                draw_list.append(DrawAction(DrawAction.PEN_MOVE, px, py1))
                draw_list.append(DrawAction(DrawAction.PEN_UP))
                draw_list.append(DrawAction(DrawAction.PEN_MOVE, px, py2))
                draw_list.append(DrawAction(DrawAction.PEN_DOWN))
                draw_list.append(DrawAction(DrawAction.PEN_MOVE, px, py))
            else:
                if r.x - prev_pos.x > 0:
                    px1 = prev_x + grid_size * 0.33
                    px2 = prev_x + grid_size * 0.33 * 2
                else:
                    px1 = prev_x - grid_size * 0.33
                    px2 = prev_x - grid_size * 0.33 * 2

                draw_list.append(DrawAction(DrawAction.PEN_MOVE, px1, py))
                draw_list.append(DrawAction(DrawAction.PEN_UP))
                draw_list.append(DrawAction(DrawAction.PEN_MOVE, px2, py))
                draw_list.append(DrawAction(DrawAction.PEN_DOWN))
                draw_list.append(DrawAction(DrawAction.PEN_MOVE, px, py))

        prev_pos = r

    draw_list.append(DrawAction(DrawAction.PEN_MOVE, sx + (prev_pos.x + 1) * grid_size + grid_size * 0.5,
                                sy + prev_pos.y * grid_size + grid_size * 0.5))

    draw_list.append(DrawAction(DrawAction.PEN_UP))

    return draw_list

