//
// Класс матрицы.
//
function Matrix(containerId, rows, cols)
{
	// id контейнера
	this.containerId = containerId;
	
	// число строк
	this.rows = rows;
	
	// число столбцов
	this.cols = cols;
	
	//подсчет съеденного
	this.foodEaten = 0;
	
	// создание сетки
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
	
	// получить значение ячейки
	this.getCell = function(row, col)
	{
		var ind = (row - 1) * this.cols + col - 1;
		var cell = $('#' + this.containerId).find('div').eq(ind);
		return cell.attr('class'); // return cell empty/cell food/cell snake // суровый метод
	}
	
	// установить значение ячейки
	this.setCell = function(row, col, type)
	{
		var ind = (row - 1) * this.cols + col - 1;
		var cell = $('#' + this.containerId).find('div').eq(ind);
		cell.removeAttr('class').addClass('cell').addClass(type); // суровый метод, до чего-нибудь изящного не додумалась
	}	

	this.setFood = function() { // из примеров дз
		
		do {
			i = Math.floor(Math.random() * this.rows) + 1;
			j = Math.floor(Math.random() * this.cols) + 1;
			var ind = (i - 1) * this.cols + j - 1; // эта строчка здесь третий раз за код
		} while (this.getCell(i, j) == 'cell snake')
		var cell = $('#' + this.containerId).find('div').eq(ind);
		cell.removeClass('empty').addClass('food');
	}	
	
	
}
		
