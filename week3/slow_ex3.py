def compute():
	sum = 0.0
	for i in range(1, 10000):
		sum += 1.0 / (i ** 2)
	return sum

for i in range(500):
    compute()

print(compute())
