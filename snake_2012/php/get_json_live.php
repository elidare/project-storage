<?php
header('Content-type:text/html; charset=utf-8');
$results = file('../results.txt');

$list = array();

$searchfor = $_POST['searchName'];

foreach($results as $line)
{
	$arr = explode(':', $line);
	$symb = substr($arr[1], 0, strlen($searchfor));
	
	if ($searchfor == $symb && $searchfor != '') {
		$list[] = $arr;
	}
}

echo json_encode($list);
