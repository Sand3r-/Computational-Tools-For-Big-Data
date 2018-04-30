import json
from pprint import pprint
import sys, re

def extract_bag_of_words(data):
	bag_of_words = set([])
	request_lists_of_words = []
	for dictionary in data:
		request_text = dictionary["request_text"].encode('utf-8') 
		list_of_words = re.sub("[^\w]", " ", str(request_text)).split()
		unique_words = set(list_of_words)
		bag_of_words = bag_of_words.union(unique_words)
		request_lists_of_words += [list_of_words]

	return bag_of_words, request_lists_of_words

def get_count_list(word_list, bag_of_words):
	row = [0] * len(bag_of_words)
	for i in range(len(bag_of_words)):
		if bag_of_words[i] in word_list:
			for word in word_list:
				if word == bag_of_words[i]:
					row[i] += 1
	return row

with open('pizza-train.json') as file:
	data = json.load(file)

bag_of_words, request_lists_of_words = extract_bag_of_words(data)
bag_of_words = list(bag_of_words)
	
word_matrix = [None] * len(request_lists_of_words)
for i in range(len(request_lists_of_words)):
	word_matrix[i] = get_count_list(request_lists_of_words[i], bag_of_words)

# TODO: check if the string happens to b there.

index_to_check = 0
for possible_word_index in range(len(word_matrix[index_to_check])):
	if word_matrix[index_to_check][possible_word_index] != 0:
		print(str(bag_of_words[possible_word_index]) + ": " + str(word_matrix[index_to_check][possible_word_index]))
		# print(word_matrix[index_to_check][possible_word_index])

print("Matrix rows = " + str(len(word_matrix)))
print("Matrix columns = " + str(len(word_matrix[0])))

# print_x_words = 50
# print(bag_of_words[len(bag_of_words) - print_x_words:len(bag_of_words)])
# print(request_lists_of_words[len(request_lists_of_words) - print_x_words:len(request_lists_of_words)])
# print(word_matrix)
