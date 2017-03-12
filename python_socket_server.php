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

This script basically opens a new socket connection and sends the data to 
python socket server.

*/

if(isset($_POST["action"])){
	$action  = $_POST["action"];	
	
	if($action == "send"){
		$data = $_POST["data"];
		$host = "localhost";
		$port = 3000;
		$socket = socket_create(AF_INET, SOCK_STREAM,SOL_TCP) or die("Could not create socket\n");

		socket_connect ($socket , $host,$port );
		socket_write($socket, $data, strlen ($data)) or die("Could not write output\n");
		socket_close($socket);

	}elseif ($action == "receive") {
		$host = "localhost";
		$port = 3000;
		$socket = socket_create(AF_INET, SOCK_STREAM,SOL_TCP) or die("Could not create socket\n");

		socket_connect ($socket , $host,$port );
		socket_write($socket, $data, strlen ($data)) or die("Could not write output\n");
		socket_close($socket);
	}elseif ($action == "start_server") {

		// putenv('PYTHONPATH=/var/www/.local/lib/python2.7/site-packages:/var/www/.local/lib/python2.7/site-packages:');
		$start_server = shell_exec('sudo python3 ./python/socket_server.py' );
	}elseif ($action == "stop_server") {

		// putenv('PYTHONPATH=/var/www/.local/lib/python2.7/site-packages:/var/www/.local/lib/python2.7/site-packages:');
		echo shell_exec('sudo sudo killall python -9  2>&1' );
	}
}
?>
