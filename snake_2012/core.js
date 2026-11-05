//
// Core class
function Core() {
  this.matrix; //
  var snake;
  var timer;
  var playerName;
  var firstCell = [
    [1, 1],
    [1, 2],
    [1, 3],
  ];

  var that = this;

  this.load = function () {
    that.matrix = new Matrix("matrix1", 20, 20);

    snake = new Snake(firstCell, "right");

    $("#foodEaten").html(snake.numEaten);
    $("#lives").html(snake.lives);
  };

  this.start = function () {
    that.matrix.create();
    snake.create();
    that.matrix.setFood(); // Make random food

    if (typeof timer == "undefined") {
      // If no timer is set
      timer = setInterval(function () {
        if (snake.alive) {
          snake.move();
        } else {
          that.gameover();
          $("#divShowResults").show();
        }
      }, 200);
    }
  };

  this.gameover = function () {
    // Game over
    alert("Oops!");
    clearInterval(timer);
    timer = undefined;
  };

  this.cmdRight = function () {
    if (snake.course != "left") snake.newCourse = "right";
  };

  this.cmdLeft = function () {
    if (snake.course != "right") snake.newCourse = "left";
  };

  this.cmdUp = function () {
    if (snake.course != "down") snake.newCourse = "up";
  };

  this.cmdDown = function () {
    if (snake.course != "up") snake.newCourse = "down";
  };
}
