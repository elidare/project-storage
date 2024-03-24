<?php header('Content-type:text/html; charset=utf-8'); ?>
<!DOCTYPE html> 
<html>
<head>
	<!--<meta charset="utf-8">-->
	<title>GAME</title>
	<link rel="stylesheet" href="style.css" type="text/css" media="screen" /> 	
	<link rel="stylesheet" href="jquery/jquery.ui.all.css" type="text/css" media="screen" /> 	
	<script language="javascript" src="jquery/jquery-1.8.2.js"></script><!-- Подключить сразу один файл min -->
	<script language="javascript" src="jquery/jquery.ui.core.js"></script>
	<script language="javascript" src="jquery/jquery.ui.widget.js"></script>
	<script language="javascript" src="jquery/jquery.ui.position.js"></script>
	<script language="javascript" src="jquery/jquery.ui.menu.js"></script>
	<script language="javascript" src="jquery/jquery.ui.autocomplete.js"></script>
	
	<script language="javascript" src="core.js"></script>
	<script language="javascript" src="matrix.js"></script>
	<script language="javascript" src="snake.js"></script>
	<script language="javascript" src="onload.js"></script>

</head>
<body>
	<!--<p id="hello"> 
		Здравствуйте! Введите ваше имя:<br />
		<form><input id="playerNameInput" type="text" name="name" /><br />
		<input type="button" id="saveName" value="Сохранить"></form><br />
		<span id="content"></span>
	</p>-->
	<div id="matrix1"> 
    </div>
	<div id="aboutGame">
		<!--Вы играете как:
		<span id="playerName"></span><br />-->
		<p>
			Eaten/Съедено:&nbsp;
			<span id="foodEaten"></span><br />
			Lives/Жизней:&nbsp;
			<span id="lives"></span>
		</p>
		<div id="divShowResults">
			<input type="button" id="btnShowResults" value="Results/Результаты"/>
			<p id="showResults">
			</p>
		</div>
	</div>
	
	<!-- div для поиска без UI -->
	<div id="playerSearch">
		<p>Live search simple/Поиск игрока по имени<br />
			<input type="text" name="inputPlayerSearch" /><br />
		</p>
		<p id="playerFound">
		</p>
	</div>
	
	<!-- div для поиска UI -->
	<div id="playerSearchUI">
		<p>Live <strong>UI autocomplete</strong> search<br />
			<input type="text" name="inputPlayerSearchUI" /><br />
		</p>
	</div>
</body>
</html>

