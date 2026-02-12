from main import find_head

def test_find_head():
	assert find_head([(10, 13), (10, 14)]) == (10, 14)