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

*/

error_reporting(E_ALL);

header("Content-Type: text/event-stream");
header("Cache-Control: no-cache");
header("Connection: keep-alive");

set_time_limit (0);

$host = "localhost";
$port = 3000;

$socket = socket_create(AF_INET, SOCK_STREAM,SOL_TCP) or die("Could not create socket\n");

$data = "receive";

socket_connect ($socket , $host,$port );
socket_write($socket, $data, strlen ($data)) or die("Could not write output\n");
$out = '';
echo "Reading response:\n\n";

$id = 0;
while ($out = socket_read($socket, 2048)) {
    // echo $out;
    $id++;
	sendMessage($id,$out);

    ob_flush(); flush(); 
}

function sendMessage($id, $data) {
	echo "id: $id\n";
	echo "data: $data\n\n";
	ob_flush();
	flush();
}

socket_close($socket);

echo "python_console.php 1052";
?>
