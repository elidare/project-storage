//
// Ядро
function Core()
{
	this.matrix; // 
	var snake;
	var timer;
	//var count;
	var playerName;
	var firstCell = [[1, 1], [1, 2], [1, 3]];
	
	var that = this;
	
	this.load = function()
	{
		that.matrix = new Matrix('matrix1', 20, 20);
		//that.matrix.create();
		snake = new Snake(firstCell, 'right');
		//snake.create();
		//that.matrix.setFood(); //рандомная еда 
		
		$('#foodEaten').html(snake.numEaten);
		$('#lives').html(snake.lives);

	}

	this.start = function()
	{	
		//count = 0;
		that.matrix.create();
		snake.create();
		that.matrix.setFood(); //рандомная еда 
		
		if(typeof(timer) == 'undefined') { // если таймера нет по сути
			timer = setInterval(function(){
									if(snake.alive) { 
										snake.move(); 
									} else { 
										that.gameover();
										$('#divShowResults').show(); // результаты покажем после игры
									}
								}
								, 200)
		}
	}
	
	this.gameover = function()
	{	
		//завершаем игру
		alert('Oops!');

		playerName = prompt('Wanna get into history? Save your name/Хотите сохранить результат? Введите имя');
		
		if(playerName) {
			that.saveResult(playerName, snake.numEaten);
		} else {
			alert('No name given, no result saved!');
		}

		clearInterval(timer);
		timer = undefined;
	}
	
	this.cmdRight = function()
	{
		if(snake.course != 'left') snake.newCourse = 'right';
	}
	
	this.cmdLeft = function()
	{
		if(snake.course != 'right') snake.newCourse = 'left'; 
	}
	
	this.cmdUp = function()
	{
		if(snake.course != 'down') snake.newCourse = 'up';
	}
	
	this.cmdDown = function()
	{
		if(snake.course != 'up') snake.newCourse = 'down';
	}
	
	this.saveResult = function(playerName, score) {
		$.post("php/add.php",
				{name: playerName, score: score}, 
				"html" // "xml", "script", "json", "jsonp", "text"
				);
	}
}