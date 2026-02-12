from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import math

# store board variables
BOARD_WIDTH = 21
BOARD_HEIGHT = 15

def main():
	# open snake game
	driver = webdriver.Chrome()
	actions = ActionChains(driver)
	driver.get("http://playsnake.org")

	# Wait until levels buttons come into view and store into "elem," then simulate click
	elem = WebDriverWait(driver, 10).until(
    	EC.presence_of_element_located((By.CSS_SELECTOR, 'p.level[data-level="2"]'))
	)
	elem.click()

	# wait until game actually starts (3 second countdown)
	time.sleep(2)
	 
	while True:
		# pull snake locations, pull food location
		js = """
			const cells = Array.from(document.querySelectorAll('.game .board .cell'));
			const snake = [];
			let food = -1;

			for (let i = 0; i < cells.length; i++) {
				if (cells[i].classList.contains('snake')) {
					snake.push(i);
				}
				if (cells[i].classList.contains('food')) {
					food = i;
				}
			}

			return {
				"snake": snake, 
				"food": food, 
				"count": cells.length
			};
		"""
		state = driver.execute_script(js)

		# determine food position
		# x = index % BOARD_WIDTH
		# y = index // BOARD_WIDTH
		food_pos = (state['food'] % BOARD_WIDTH, state['food'] // BOARD_WIDTH)

		# determine snake positions
		snake_positions = []
		for i in state["snake"]:
			snake_positions.append((i % 21, i // 21))

		# determine snake's head and direction
		head = find_head(snake_positions)

		# orient snake towards food
		key = greedy_algo(head, food_pos)

		if key != None:
			actions.send_keys(key).perform()

def serpentine_scan(head):
	MOVES = {
	    Keys.ARROW_RIGHT: (1, 0),
	    Keys.ARROW_LEFT: (-1, 0),
	    Keys.ARROW_UP: (0, -1),
	    Keys.ARROW_DOWN: (0, 1)
	}

	key = None

	# scan mode = right (initial)

	# if scan mode == right
		# if going down
			# if next step hits bottom wall
				# key = left
			# else
				# key = down
		# else if going left
			# key = up
		# else if going up
			# if next step hits top wall
				# key = right
			# else
				# key = bottom
		# else if going right
			# key = down

		# if x = WIDTH
			# switch to left scan

	# if scan mode == left
		# if going down
			# if next step hits bottom wall
				# key = right
			# else
				# key = down
		# if going right
			# key = up
		# if going up
			# if next step hit top wall
				# key = left
			# else
				# key = up
		# if going left
			# key = down

		# if x == 0
			# switch to right scan


	return key

def greedy_algo(head, food):
	MOVES = {
	    Keys.ARROW_RIGHT: (1, 0),
	    Keys.ARROW_LEFT: (-1, 0),
	    Keys.ARROW_UP: (0, -1),
	    Keys.ARROW_DOWN: (0, 1)
	}

	best_key = None
	best_dist = float("inf")

	for key, (dx, dy) in MOVES.items():
		# skip if it tries to go "backwards"
		backwards_pos = (-find_head.dir[0], -find_head.dir[1])
		if (dx, dy) == backwards_pos:
			continue

		# determine distance of potential next position
		next_pos = (head[0] + dx, head[1] + dy)
		d = math.dist(next_pos, food)

		# skip if next_pos is in the snake's current positions
		if next_pos in find_head.prev_positions:
			continue

		# check if it brings us closer
		if d < best_dist:
			best_dist = d
			best_key = key

	# Modify the find_head functional attribute for direction
	if best_key != None:
		find_head.dir = [MOVES[best_key][0], MOVES[best_key][1]]

	# return best_key... duh
	return best_key

def find_head(positions):
	# check whether this function has any attributes (only true at the start of the game)
	if not hasattr(find_head, "prev_positions"):
		find_head.prev_positions = positions
		find_head.dir = [0, 1]

		# head is the last value in the positions array
		find_head.head = positions[-1]
		return positions[-1]

	# find new cell position within the arrays (once snake moves, tail dissapears and head moves to new position)
	prev = set(find_head.prev_positions)
	curr = set(positions)
	new_cell = curr - prev 

	# if a new cell was found, our head is that new cell, but if no new cell was found, return the previous cell we found
	if new_cell:
		head = new_cell.pop()
		find_head.head = head
	else:
		head = find_head.head

	# set previous positions to given positions and head to head
	find_head.prev_positions = positions

	return head

if __name__ == "__main__":
	main()