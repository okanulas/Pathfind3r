# Pathfinder
Pathfinder is a Lego Mindstorms based printing system that can generate and solve 2D mazes. Grid size and dimensions are customizable. Maze width and height is limited to 20 tiles to support international A4 sized paper. In addition to draw and solve mazes Pathfinder can also draw simple SVG paths as well. Draw area of the SVG file should be set as 1750x1650.

## Software
Hearth of the brick is a Debian-Linux based operating system developed by folks at http://www.ev3dev.org/ . Many programming languages can be used with this distribution. Pathfind3r uses python for core functions, php for backend support and query for web interface.

Generating and solving mazes, printing svg files and core printing scripts are seperate classes. A python socket server is used to control these functions. Also feedback from the socket server is written into the console.

Basic flow of data is: Command -> Web Interface -> Php Script -> Python Socket Server -> Execution.

## Dependencies
1. Ev3 should be started using ev3dev debian linux distribution.
2. Local git should be set up on the ev3dev. There is a good tutorial about setting up the development environment at this address -> http://www.ev3dev.org/docs/tutorials/setting-up-python-pycharm/
3. Apache.
3. Php 5.

##Demo
You can watch the Pathfind3r in action here -> youtube link will be here soon.

##Project Page
For more info please visit the project page.
www.okanulas.com/pathfinder/

