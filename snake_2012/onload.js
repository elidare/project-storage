//
// Точка входа.
//
$(document).ready(function(){

	/* на случай, если спрашивать имя в начале, но оно не доведено до работающего состояния
		$("#saveName").click(function(elem){
		playerName = $('#playerNameInput').val();
		//console.log(snake.numEaten);
		$('#hello').hide();
		$('#matrix1').show();
		$('#aboutGame').show();
		snake.create();
		$('#playerName').html(playerName); 
	});*/
	
	_game = new Core();
	_game.load();
	_game.start();
	
		
	$(document).keydown(function (evt) { // document.onkeypress не работал в Chrome 
	
		var evt = (evt) ? evt : window.event;
		var code = (evt.charCode) ? (evt.charCode) : (evt.keyCode); //
		
		switch (code) {
			case 37: //влево 
				_game.cmdLeft();
			break;
			case 38: //вверх
				_game.cmdUp();
			break;
			case 39: //вправо
				_game.cmdRight();
			break;
			case 40: //вниз 
				_game.cmdDown();
			break;
		}
	});
	
/* Вариант без JSON 
	$("#btnShowResults").click(function(elem){
		$("#showResults").load("php/get.php", 
							   "data=content" 							
							   );
	}); */
	
/* // c JSON */
	$("#btnShowResults").click(function(elem){
		$.get("php/get_json.php", 
			   {data: "content"}, showResults, "json" 							
			   );
	});
	
	function showResults(playersList) {
		
		$('#showResults').html('');
		var htmlList = '';
		for(var i = 0; i < playersList.length; i++){
			htmlList += '<li>' + playersList[i][1] + '&nbsp;......&nbsp;' + playersList[i][0] + '</li>';
		}
		$('#showResults').html('<ol>' + htmlList + '</ol>');
	}
/* */
	
/* // Живой поиск без jQuery UI */
	$('#playerSearch input').keyup(function(evt) {
		
		//var evt = (evt) ? evt : window.event; // необходимы проверки на входящий символ
		//var code = (evt.charCode) ? (evt.charCode) : (evt.keyCode); 
		
		$.post('php/get_json_live.php', {searchName: $('#playerSearch input').val()}, findPlayer, "json");
		
		function findPlayer(playersFound) {
		
			$('#playerFound').html('');
			var htmlList = '';
			for(var i = 0; i < playersFound.length; i++){
				htmlList += '<li>' + playersFound[i][1] + '&nbsp;......&nbsp;' + playersFound[i][0] + '</li>';
			}
			$('#playerFound').html('<ul>' + htmlList + '</ul>');
		}
			
	});

/* // jQuery UI Autocomplete */	
	$(function() {
		var availableTags = [];
		
		$.get("php/get_json.php", 
			   {data: "content"}, makeList, "json" 							
			 );
		
		function makeList(playersList) { // создает массив только имен без счета очков. Только не знаю, зачем. Зато работает
		
			for(var i = 0; i < playersList.length; i++){
				availableTags[i] = playersList[i][1];
			}
		}
			   
		$( "#playerSearchUI input" ).autocomplete({
			source: availableTags
		});
	});
/* */	
});		