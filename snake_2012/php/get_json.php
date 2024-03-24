<?php
header('Content-type:text/html; charset=utf-8');
$results = file('../results.txt');

arsort($results, 1);

$list = array();

foreach($results as $line)
{
	$arr = explode(':', $line);
	$list[] = $arr;
}

echo json_encode($list);
