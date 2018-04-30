keys = [
	"id",
	"name",
	"city",
	"country",
	"iata",
	"icao",
	"latitude",
	"longitude",
	"altitude",
	"timezone",
	"dst",
	"tz",
	"type",
	"source"
]

# Extract lines as strings
lines = [line.rstrip('\n') for line in open('airports.dat', encoding="cp850", errors="replace")]

# Load data into dictionaries
dictionaries = [None] * len(lines)
for j in range(len(lines)): # len(lines)
	line = lines[j].split(",")

	for i in range(len(line)):
		if (line[i].replace(".","").replace("-","")).isdigit() and line[i].find(".") != -1:
			line[i] = float(line[i])
		elif line[i].isdigit():
			line[i] = int(line[i])
		else:
			line[i] = line[i].replace('"', '')

	dictionary = {}
	for i in range(len(keys)):
		dictionary[keys[i]] = line[i]
	dictionaries[j] = dictionary

airports_amount_per_country = {}

for dictionary in dictionaries:
	if int(dictionary['altitude']) < 10000:
		continue
	if dictionary['country'] in airports_amount_per_country:
		airports_amount_per_country[dictionary['country']] = airports_amount_per_country[dictionary['country']] + 1
	else:
		airports_amount_per_country[dictionary['country']] = 1

'''
for first, second in sorted_x:
	print(first.replace('\xa9', '') + ' ' + str(second))
'''

print("Country,  No. of airports above 10000 feet above sea level")
for key, value in airports_amount_per_country.items():
	print(key.replace('\xa9', '') + ", " + str(value))


#print(str(country.values()) + "\n" for country in airports_amount_per_country)

'''
import operator
sorted_x = sorted(airports_amount_per_country.items(), key=operator.itemgetter(1))
'''

'''
dictionaries = [None] * len(lines)
for i in range(len(lines)):
	lines[i]
	dictionaries[i] = lines[i]
'''