$(document).ready(function() {

	canvas = document.getElementById('canvas-home');
	ctx = canvas.getContext('2d');

	var leftFoot = new Image;
	var rightFoot = new Image;
	leftFoot.src = 'img/leftFoot.png';
	rightFoot.src = 'img/rightFoot.png';
	var isLeft = true; // Starting with a left foot
	var coord = []; // array to keep mouse coordinates
	var currentCoord = [[0,0], [0,0], [0,0], [0,0]]; // 4 coordinate points for making steps


	var coordQuan = 6; // how many steps to draw + 2 (current mouse position + a step to erase)

	canvas.onmousemove = function (e) {

		var mouseX = e.pageX - e.target.offsetLeft; // 
		var mouseY = e.pageY - e.target.offsetTop; // 
		
		coord.push([mouseX, mouseY]); // Saving mouse coords. UPD from 2024: seems quite uneffective, but hey, I did it as an intern
		
		var saveCoord = function() {
			// Adding up to coordQuan coordinates with difference by 50 px 
			if(mouseX !== coord[0][0]) { 
				if(Math.abs(mouseX - coord[0][0]) > 50 || Math.abs(mouseY - coord[0][1]) > 50) {
					coord.unshift([mouseX, mouseY]); // Get the last point
				}
			}
			if(coord.length > coordQuan) { coord.pop(); }
			return coord;
		}
		
		
		
		var getAngle = function(coord) { // Get the angle to rotate the step
		
			var dy = coord[0][1] - coord[1][1];
			var dx = coord[0][0] - coord[1][0];
			var num = dy / dx; 
			var angle = Math.atan(num);
			if(dx < 0) { angle = angle + Math.PI; }
			return angle;
		}
		
		var draw = function (point) { 
		
			var img, n;
			isLeft = !isLeft; // Left - right - left - right

			if(isLeft) {
				img = leftFoot;
				n = -15;
			} else {
				img = rightFoot;
				n = 15;
			}
			
			ctx.save();
			ctx.translate(point[0], point[1]);
			ctx.rotate(getAngle(saveCoord()));
			ctx.drawImage(img, 0, n);
			ctx.restore();
		};
		
		if(currentCoord[0] !== saveCoord()[0]) {
			/* If the array is changed... */
			currentCoord = saveCoord().slice(); 
			
			if(saveCoord()[coordQuan - 1]) {
				/* ... erase the last one from canvas. Yep, that's messy */
				ctx.clearRect(saveCoord()[coordQuan - 1][0] - 36, saveCoord()[coordQuan - 1][1] - 36, 72, 72);
			}
			if(saveCoord()[1]) {
				/* ... and drawing the next one */
				draw(saveCoord()[1]);
			}

		}
	};
	
});
