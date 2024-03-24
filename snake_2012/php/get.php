
<?php
header('Content-type:text/html; charset=utf-8');
$results = file('../results.txt');

arsort($results, 1);
/*
foreach($results as $result)
{
	$arr = explode(':', $result);
	//echo '<p>' . $arr[1] . '&nbsp;.....&nbsp;' . $arr[0] . '&nbsp;pts</p>'; 
	
}*/
?>
<ol>
<?php foreach ($results as $result) : 
$arr = explode(':', $result); ?>
<li> <?=$arr[1]?> ..... <?=$arr[0]?> </li>
<?php endforeach ?>
</ol>