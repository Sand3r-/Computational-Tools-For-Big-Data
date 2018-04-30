def compute():
    cdef float sum = 0.0
    # cdef int i
    for i in range(1, 10000):
        sum += 1.0 / (i ** 2)
    return sum