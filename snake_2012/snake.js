//
// Класс змеи
//
function Snake(body, course)
{
	// координаты строк и столбцов
	this.body = body;
	var startCells = body.slice();
	
	// направление движения
	this.course = course;
	this.newCourse = course;
	
	// съела ли змейка фрукт
	//this.eaten = false;
	this.numEaten = 0;
	// жива ли змейка
	this.alive = true;
	// жизни
	this.lives = 3; 
	
	var that = this;
	
	var snakeLength = that.body.length;
	
	this.create = function() {
		//отрисовываем змейку
		for(var i = 0; i < snakeLength; i++) {
			_game.matrix.setCell(startCells[i][0], startCells[i][1], 'snake'); // отрисовка по начальным координатам написана для экспериментов, а обратно менять боюсь
		}
	}
	
	this.move = function()
	{	
		that.eaten = false;
		that.course = that.newCourse;

		var snakeHead = that.body[that.body.length - 1].slice();
		
		switch(that.course) {		
			case 'right':
				snakeHead[1]++;
				if((snakeHead[1] % _game.matrix.cols) == 1) { // проверка на стены
					that.kill();
					return;
				}
			break;	
			case 'left':
				snakeHead[1]--;
				if((snakeHead[1] % _game.matrix.cols) == 0) {
					that.kill();
					return;
				}
			break;
			case 'down':
				snakeHead[0]++;
				if((snakeHead[0] % _game.matrix.rows) == 1) {
					that.kill();
					return;
				}
			break;
			case 'up':
				snakeHead[0]--;
				if((snakeHead[0] % _game.matrix.rows) == 0) {
					that.kill();
					return;
				}
			break;
		}
		
		if(_game.matrix.getCell(snakeHead[0], snakeHead[1]) == 'cell snake') { // если врезались в себя, убить
			that.kill();
			return;
		} else if(_game.matrix.getCell(snakeHead[0], snakeHead[1]) == 'cell empty') { // если нет еды, отрезать хвост
			var snakeTail = that.body.shift();
			_game.matrix.setCell(snakeTail[0], snakeTail[1], 'empty');
		} else { // если не врезались и не пусто, значит, еда
			that.eat();
		}
		that.body.push([snakeHead[0], snakeHead[1]]);
		
		_game.matrix.setCell(snakeHead[0], snakeHead[1], 'snake'); // пририсовали голову
	}	
	
	this.eat = function()
	{	
		$('#foodEaten').html(++that.numEaten);
		_game.matrix.setFood();
	}	
	
	this.kill = function() // 
	{	
		that.lives--;
		if (that.lives > 0) { // 

			$('#lives').html(that.lives);
			that.alive = true;
			that.newCourse = 'right'; // 
			that.body = startCells.slice();
			//_game.matrix.create();
			//this.create(); 
			//_game.matrix.setFood();
			_game.start();
						
		} else {
			that.alive = false; 
		}
	}	
	
}