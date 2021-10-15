<?php
	session_start();
	session_unset();
	session_destroy();
	
	$path = getcwd();
	$path = dirname($path);
	$path = $path."\python";
	chdir($path);
	
	$command = escapeshellcmd("ClearMemory.py");
	$output = shell_exec($command);
	echo $output;
	
	header("Location: ..");
?>