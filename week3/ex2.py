#def lagrange_basis_poly(x, )
import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt

x = []
y = []

with open('points.txt') as file:
	for line in file:
		line = line.split(" ")
		x.append(float(line[0]))
		y.append(float(line[1]))

poly = np.poly1d(np.polyfit(x, y, 3))
roots = optimize.fsolve(poly, -10.0)
print(roots)

# Printing
X = np.linspace(-3.0, 3.0, 256, endpoint=True)
Y = poly(X)
fig, ax = plt.subplots()
ax.plot(X, Y)
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
plt.show()


