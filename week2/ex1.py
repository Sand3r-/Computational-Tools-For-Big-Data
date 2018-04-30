import sys

def add_one(bit_list):
	result = bit_list[:]
	for i in range(len(bit_list) - 1, -1, -1):
		if bit_list[i] == 0:
			result[i] = 1
			return result
		else:
			result[i] = 0

def create_all_combinations(N):
	list_of_binary_lists = []

	binary_list = [0] * N
	for y in range(2**N):
		list_of_binary_lists += [binary_list]
		binary_list = add_one(list_of_binary_lists[y])
	return list_of_binary_lists


N = int(sys.argv[1])
print(create_all_combinations(N))