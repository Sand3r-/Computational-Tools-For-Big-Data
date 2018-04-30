import numpy as np

matrix_as_list = []
b_as_list = []

with open('matrix.txt') as file:
	for line in file:
		row = []
		line = line.replace("\n", "").split(",")
		for i in range(len(line) - 1):
			row.append(int(line[i]))
		matrix_as_list.append(row)
		b_as_list.append(int(line[len(line) - 1]))

matrix = np.array(matrix_as_list)
b = np.array(b_as_list)

x = np.linalg.solve(matrix, b)
y = np.dot(matrix, x)

print("A = " + str(matrix))
print("b = " + str(b))
print("After linsolve: ")
print("x = " + str(x))
print("A * x = b' = " + str(y))


