from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

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

		print(snake_positions)

		# If snake's position hasn't updated yet (because the computer's just so dang fast), continue
		#if (find_head.positions == snake_positions):
			#continue

		# determine snake's head and direction
		'''
		Every time the game starts the snake's direction is always downward, with a tail trailing behind it
		Given this we can assume that the snake's direction is x=0, y=-1 
		and head is the last value in the array...
		Perhaps we can use this to remember and "store" the head and direction and any change with these 
		values will tell us to then re-point to what the head of the snake is!
		'''
		#head = find_head(snake_positions)

		# orient snake towards ts
		#key = next_move()

		#actions.send_keys(key).perform()

		# Modify the find_head functional attribute for direction
		#find_head.dir = [dir_x, dir_y] # this new direction value is determined from the next_move() function

'''
Overall sequence:
1. Get snake's positions and the food's position
2. WE determine the snake's head and direction based off this new data
3. We determine which move to make in order to bring us close to the food
4. The key is sent
'''

def find_head(positions):
	# check whether this function has any attributes (only true at the start of the game)
	if not hasattr(find_head, "prev_positions"):
		find_head.prev_positions = positions
		find_head.dir = [0, 1]
		find_head.head = positions[-1]

		# head is the last value in the positions array
		return positions[-1]

	# find new cell position within the arrays (once snake moves, tail dissapears and head moves to new position)
	prev = set(find_head.prev_positions)
	curr = set(positions)
	new_cell = curr - prev 

	# if a new cell was found, our head is that new cell, but if no new cell was found, return the previous cell we found
	if new_cell:
		head = new_cell
		find_head.head = head
	else:
		head = find_head.head

	# set previous positions to given positions and head to head
	find_head.prev_positions = positions

	return head

def next_move():
	return 0

if __name__ == "__main__":
	main()