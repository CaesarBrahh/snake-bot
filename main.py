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
	time.sleep(3)
	 
	#while True:
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

		print("food position: " + str(food_pos[0]) + ", " + str(food_pos[1]))
		#print("snake positions" + snake_positions)

		# determine head

		# determine direction

		# orient snake towards ts
		#key = next_move()

		#actions.send_keys(key).perform()


def next_move():
	return 0

if __name__ == "__main__":
	main()