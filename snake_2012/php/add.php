<?php

if($_SERVER['HTTP_REFERER'] != 'http://js7/') 
	die();


$name = $_POST['name'];
$score = $_POST['score'];

$f = fopen('../results.txt', 'a+');
//fwrite($f, $name . ":" . $score . "\n");
fwrite($f, $score . ":" . $name . "\r\n");

fclose($f);

