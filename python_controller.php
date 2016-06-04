<?php

/*

MIT License

Copyright (c) [2016] [Okan Ulas Gezeroglu]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This is my first attemp which calls python scripts from php to execute draw commands. 
Although it is an effective method but very slow. I started to use python socket server
to execute commands on the brick which is more robust and responsive. 
*/

putenv('PYTHONPATH=/var/www/.local/lib/python2.7/site-packages:/var/www/.local/lib/python2.7/site-packages:');

if($_POST["action"])
	{
		$action  = $_POST["action"];
		if($action == "calibrate"){
			$calibrate = shell_exec('sudo python /var/www/pathfinder/python/calibrate.py ' );
			echo "Calibrate ".$calibrate;
		}else if ($action == "set_up_pen"){
			$penPos = shell_exec('sudo python /var/www/pathfinder/python/set_pen_position.py ' );
			echo "Pen Position ".$penPos;
		}else if ($action == "draw_svg"){
			$svgData = array('file' =>$_POST["svg_file"]);
			$drawSvg = shell_exec('sudo python /var/www/pathfinder/python/draw_svg.py '. escapeshellarg(json_encode($svgData)).'  2>&1' );
			echo $drawSvg;
		}else if ($action == "draw_maze"){
			$rows = $_POST["rows"];
			$cols = $_POST["cols"];
			$gridSize = $_POST["grid_size"];
			$mazeData = array('rows' =>$rows,'cols'=>$cols,'gridSize'=>$gridSize);
			$maze = shell_exec('sudo python /var/www/pathfinder/python/draw_maze.py '. escapeshellarg(json_encode($mazeData))); // .'  2>&1'
			echo $maze;
		}else if ($action == "get_info"){
			$info = shell_exec('sudo python /var/www/pathfinder/python/get_info.py');
			$infoResult = json_decode($info, true);
			var_dump($infoResult);

		}else if ($action == "stop_printer"){
			$stopMotors = shell_exec('python /var/www/pathfinder/python/stop_printer.py');
			echo $stopMotors;
		}
	}
	
?>