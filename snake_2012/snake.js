//
// Snake class
//
function Snake(body, course)
{
	// Rows and columns coords
	this.body = body;
	var startCells = body.slice();
	
	// Movement direction
	this.course = course;
	this.newCourse = course;
	
	// How many fruits are eaten
	//this.eaten = false;
	this.numEaten = 0;
	// If the Snake is alive
	this.alive = true;
	// Snake's lives
	this.lives = 3; 
	
	var that = this;
	
	var snakeLength = that.body.length;
	
	this.create = function() {
		// Draw Snake
		for(var i = 0; i < snakeLength; i++) {
			_game.matrix.setCell(startCells[i][0], startCells[i][1], 'snake'); // it was an experiment with drawing it by the start cells, and I am too scared to change it back
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
				if((snakeHead[1] % _game.matrix.cols) == 1) { // Walls check
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
		
		if(_game.matrix.getCell(snakeHead[0], snakeHead[1]) == 'cell snake') { // If Snake runs into herself, kill it
			that.kill();
			return;
		} else if(_game.matrix.getCell(snakeHead[0], snakeHead[1]) == 'cell empty') { // If next cell has no food, cut off Snake's tail
			var snakeTail = that.body.shift();
			_game.matrix.setCell(snakeTail[0], snakeTail[1], 'empty');
		} else { // If next cell is not a Snake and not empty, that means food
			that.eat();
		}
		that.body.push([snakeHead[0], snakeHead[1]]);
		
		_game.matrix.setCell(snakeHead[0], snakeHead[1], 'snake'); // Add up a head cell in any case
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
