from scipy import misc
import scipy.ndimage as ndimage
import numpy as np
import matplotlib.pyplot as plt
import sys

def load_image(file_name):
    return misc.imread(file_name)

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def apply_lsh(image):
    filtered = np.ones(shape=(image.shape[0], image.shape[1] - 1), dtype=bool)
    for i in range(image.shape[0]):
        for j in range(image.shape[1] - 1):
            filtered[i][j] = image[i][j] > image[i][j+1]
    return filtered

# Author: David Kofoed Wind
def hash_differences(image):
    result = ''
    for difference in image:
        decimal_value = 0
        hex_string = []
        for index, value in enumerate(difference):
            if value:
                decimal_value += 2**(index % 8)
            if (index % 8) == 7:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value = 0
        result += ''.join(hex_string)
    return result


if len(sys.argv) < 3:
    sys.exit('Usage: %s file1 file2' % sys.argv[0])

filename_one = sys.argv[1]
filename_two = sys.argv[2]

grayscale_one = rgb2gray(load_image(filename_one))
grayscale_two = rgb2gray(load_image(filename_two))

resized_one = misc.imresize(grayscale_one, (8, 9))
resized_two = misc.imresize(grayscale_two, (8, 9))

filtered_one = apply_lsh(resized_one)
filtered_two = apply_lsh(resized_two)

print(hash_differences(filtered_one))
print(hash_differences(filtered_two))