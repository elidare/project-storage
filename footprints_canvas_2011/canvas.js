$(document).ready(function() {

	canvas = document.getElementById('canvas-home');
	ctx = canvas.getContext('2d');

	var leftFoot = new Image;
	var rightFoot = new Image;
	leftFoot.src = 'img/leftFoot.png';
	rightFoot.src = 'img/rightFoot.png';
	var isLeft = true; // начинаем с левой
	var coord = []; // массив для записи всех координат мыши
	var currentCoord = [[0,0], [0,0], [0,0], [0,0]]; // 4 точки координат для шагов


	var coordQuan = 6; // количество ножек + 2(текущее положение мыши + стираемая ножка) // изменяемый параметр

	canvas.onmousemove = function (e) {

		var mouseX = e.pageX - e.target.offsetLeft; // 
		var mouseY = e.pageY - e.target.offsetTop; // 
		
		coord.push([mouseX, mouseY]); // сохраняем координаты мыши
		
		var saveCoord = function() {
			/* Записывает массив coordQuan количества координат с разницей в 50пх по верт. и гориз.. 
			Для вычисления угла поворота меньше - плохо */
			if(mouseX !== coord[0][0]) { 
				if(Math.abs(mouseX - coord[0][0]) > 50 || Math.abs(mouseY - coord[0][1]) > 50) {
					coord.unshift([mouseX, mouseY]); // записывает последнюю точку
				}
			}
			if(coord.length > coordQuan) { coord.pop();} // точек должно быть 6, лишние убираем
			return coord; //
		}
		
		
		
		var getAngle = function(coord) { // получает угол поворота, на который надо повернуть ножку
		
			var dy = coord[0][1] - coord[1][1];
			var dx = coord[0][0] - coord[1][0];
			var num = dy / dx; 
			var angle = Math.atan(num);
			if(dx < 0) { angle = angle + Math.PI; }
			return angle;
		}
		
		var draw = function (point) { 
		
			var img, n;
			isLeft = !isLeft; // левая - правая - левая - правая

			if(isLeft) {
				img = leftFoot;
				n = -15;
			} else {
				img = rightFoot;
				n = 15;
			}
			
			ctx.save();
			ctx.translate(point[0], point[1]); // 
			ctx.rotate(getAngle(saveCoord()));
			ctx.drawImage(img, 0, n);
			ctx.restore();
		};
		
		if(currentCoord[0] !== saveCoord()[0]) {
			/* Если массив шагов изменился... */
			currentCoord = saveCoord().slice(); 
			
			if(saveCoord()[coordQuan - 1]) {
				/* .. сотрем последнюю. Да, это хлипкий момент */
				ctx.clearRect(saveCoord()[coordQuan - 1][0] - 36,saveCoord()[coordQuan - 1][1] - 36, 72,72); //
			}
			if(saveCoord()[1]) {
				/* .. и нарисуем следующую */
				draw(saveCoord()[1]);
			}

		}
	};
	
});