/**
 * Cycle between background colors for pressed buttons.
 */
function toggleColor(button) {
	const colors = ['black', 'goldenrod', 'limegreen'];
	const currentColor = button.style.backgroundColor || 'black';
	const nextColor = colors[(colors.indexOf(currentColor) + 1) % colors.length];
	button.style.backgroundColor = nextColor;
}		

/**
 * Used to ensure Wordle answers are consistently capitalized.
 */
function convertToUpper(elem){
	elem.value = elem.value.toUpperCase();
}

/**
 * Clear the grid buttons and text field.
 */
function clearAll() {
	const buttons = document.querySelectorAll('.button');
	buttons.forEach(button => {
		button.style.backgroundColor = 'black';
		button.textContent = '';
	});
	document.querySelector('.control-text').value = '';
}

/**
 * Post pattern and key, then update grid with solution.
 */
async function draw(){
	// get pattern and key
	const buttons = document.querySelectorAll('.button');
	const colors = Array.from(buttons).map(button => button.style.backgroundColor || 'black');
	const key = document.querySelector('.control-text').value;
	
	// post request passing along colors and key
	const response = await fetch('/solveboard', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ colors, key })
	});
	
	if (!response.ok) {
		throw new Error(`HTTP error! Status: ${response.status}`);
	}
	
	// get solution words, split into letters, and assign to board
	const solution = await response.json();
	const letters = solution.match.flatMap(word => word.split(''));
	buttons.forEach(button => {
		button.textContent = '';
	});
	letters.forEach((letter, index) => {
		buttons[index].textContent = letter;
	});
}