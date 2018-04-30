from PIL import Image

# Testing on other image
im = Image.open("owl1.png")
im = im.convert('L')
print(im.size)
im_new = im.resize([8,9])

print(im_new.size)
out = []

im_new.show()
data = list(im_new.getdata())
print(data)

newData = [data[9*i : 9*(i+1)] for i in range(8)]

print(newData)
for line in newData:
    tmp = []
    for ii in range(len(line)-1):
        tmp.append(line[ii] > line[ii+1])
    out.append(tmp)

totalString = []
for difference in out:
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0
    totalString += hex_string
print(''.join(totalString))

# Testing on other image
im = Image.open("owl2.png")
im = im.convert('L')
print(im.size)
im_new = im.resize([8,9])

print(im_new.size)
out = []

im_new.show()
data = list(im_new.getdata())
print(data)

newData = [data[9*i : 9*(i+1)] for i in range(8)]

print(newData)
for line in newData:
    tmp = []
    for ii in range(len(line)-1):
        tmp.append(line[ii] > line[ii+1])
    out.append(tmp)

totalString = []
for difference in out:
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0
    totalString += hex_string
print(''.join(totalString))