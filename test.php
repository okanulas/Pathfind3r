<?php
echo "\n-----------------------------\n";
echo shell_exec("whoami");
echo "\n-----------------------------\n";
echo shell_exec("php -v  2>&1");
echo "\n-----------------------------\n";
echo shell_exec("ls -lah 2>&1");
echo "\n-----------------------------\n";
echo shell_exec("pwd 2>&1");
echo "\n-----------------------------\n";
echo shell_exec('sudo python python/socket_server.py 2>&1' );
echo "\n-----------------------------\n";
?>