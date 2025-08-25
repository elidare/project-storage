//
// Matrix class
//
function Matrix(containerId, rows, cols)
{
	this.containerId = containerId;
	
	// Rows number
	this.rows = rows;
	
	// Columns number
	this.cols = cols;
	
	// Eaten food count
	this.foodEaten = 0;
	
	// Create the grid
	this.create = function()
	{
		var matrix = $('#' + this.containerId);
		var n = this.rows * this.cols;	
		
		matrix.html("");
		
		for (var i = 0; i < n; i++)
		{
			var div = document.createElement('div');
			matrix.append(div);
			matrix.children().addClass('cell').addClass('empty');
		}
	}
	
	// Get cell's value
	this.getCell = function(row, col)
	{
		var ind = (row - 1) * this.cols + col - 1;
		var cell = $('#' + this.containerId).find('div').eq(ind);
		return cell.attr('class'); // return cell empty/cell food/cell snake // Quite straightforward
	}
	
	// Set cell's value
	this.setCell = function(row, col, type)
	{
		var ind = (row - 1) * this.cols + col - 1;
		var cell = $('#' + this.containerId).find('div').eq(ind);
		cell.removeAttr('class').addClass('cell').addClass(type); // Yeah well it's awkward but it just works
	}	

	this.setFood = function() {
		do {
			i = Math.floor(Math.random() * this.rows) + 1;
			j = Math.floor(Math.random() * this.cols) + 1;
			var ind = (i - 1) * this.cols + j - 1; // This line could have been made a function
		} while (this.getCell(i, j) == 'cell snake')
		var cell = $('#' + this.containerId).find('div').eq(ind);
		cell.removeClass('empty').addClass('food');
	}	
}
