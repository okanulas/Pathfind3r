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

## Permissions
Super user permisions are needed to run python scripts from php server.  

1. Open sudoers using command sudo visudo.
2. Add following entry under "# User privilege specification" after root: 'www-data ALL=(ALL) NOPASSWD:ALL'
	*![](http://www.okanulas.com/pathfind3r/files/visudo.png =400x)
3. Hit Ctrl+X, Accept changes and quit.


## Installation

1. Install Ev3dev from http://www.ev3dev.org/docs/getting-started/ . Latest tested and working version is ev3dev-jessie-ev3-generic-2017-02-11
2. Follow instructions at http://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/ and connect to ev3 brick using terminal.
3. Run Below commands
	* sudo apt-get update
	* sudo apt-get dist-upgrade
	* sudo apt-get install apache2 php5 libapache2-mod-php5
	* sudo /etc/init.d/apache2 restart
	* sudo mkdir /var/www/html/pathfind3r/
	* sudo git clone https://github.com/okanulas/Pathfind3r.git /var/www/html/pathfind3r/
4. Open your browser and goto the http://[ip_of_your_brick]/pathfind3r/info.php . If should see info about php installation. If there is something wrong try installing php again.
5. Open http://[ip_of_your_brick]/pathfind3r/

## Usage
1. Connect your motors:
	* A > Rail Motor
	* B > Paper Feed Motor
	* C > Pen Motor
2. Connect Touch Sensor to Input 1
3. Open http://[ip_of_your_brick]/pathfind3r/
4. Click Start Server button and wait for "Server is started" call.
5. Press Display Info button and check if every is ok.
6. Use arrow keys and space bar to check motors.
7. You need to press calibrate each time you start the server.
8. Put the pen in its place and turn the motor by hand until the pen touches the paper. Then press check button next to pen button. You can check pen up and down status using up and down buttons.

## SVG Drawing
Download Inkscape at https://inkscape.org/en/download/ .Goto Edit>Preferences .Select Input/Output>SVG Output> Path Data should be Absolute. Create a new document and set size to 1000x1000px. Start drawing with path tool. This version only sports vertical, horizontal and diagonal lines. Curves and circles are not supported. Select Inkscape svg when saving your file. Upload to the brick using web interface. You should see list of uploads when you click "Draw Svg" button. Select one and press print. Thats all.

## Demo
You can watch the Pathfind3r in action here -> [Youtube Video](https://www.youtube.com/watch?v=tg4IwxdkICM)

## Project Page
For more info please visit the project page.
[Project Page](http://www.okanulas.com/pathfind3r/)

