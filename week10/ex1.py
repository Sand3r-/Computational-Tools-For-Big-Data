import json, sys
from itertools import chain

# Globals
jsons_num = 22
use_hasher = bool(int(sys.argv[1])) # Switch between using feature hashing 
                                    # and bag of words

# Reading files to memory
def load_file(file):
    with open(file) as contents:
        return json.load(contents)

articles_per_file = [None] * jsons_num
for i in range(jsons_num):
    file_name = "full/reuters-" + str(i).zfill(3) + ".json"
    articles_per_file[i] = load_file(file_name)

articles = list(chain(*articles_per_file)) # Merge all json lists into a single

vocabulary = set() # Used for bag of words
articles_bodies = []
labels = [] # Used as a ground truth by random forest classifier for articles
            # that cointain "earn" topic in their list.
# Removing those without topics or body.
for i in range(len(articles) - 1, -1, -1): # Hack allowing for removing elements
    article = articles[i]                  # from list while iterating over it.
    if "topics" not in article or "body" not in article:
        del articles[i] # Reduce the amount of memory used by the program
    else:
        lowercase_body = article['body'].lower()
        vocabulary.update(lowercase_body.split())
        articles_bodies.append(lowercase_body)
        if 'earn' in article['topics']:
            labels.append(1)
        else:
            labels.append(0)

from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import csr_matrix

def simple_feature_hasher():
    num_features = 1000
    row_num = len(articles_bodies)

    row_indices = [] # These 2 lists are used to indicate nonzero 
    col_indices = [] # positions in the sparse matrix...
    data = []        # ...and data is used to indicate the respective values

    for i in range(row_num):
        words = articles_bodies[i].split()
        current_row = [0] * num_features # Create an empty row
        for word in words:
            col_idx = hash(word) % num_features # Find the column index by hashing
            current_row[col_idx] += 1
        for j in range(len(current_row)): # Only add the positive values to
            if current_row[j] > 0:        # the list
                row_indices.append(i)
                col_indices.append(j)
                data.append(current_row[j])

    return csr_matrix((data, (row_indices, col_indices)), 
            shape=(row_num, num_features), dtype=int).toarray()

def extract_features():
    if use_hasher:
        return simple_feature_hasher()
    else:
        cv = CountVectorizer(vocabulary=list(vocabulary)) # Use bag of words
        return cv.fit_transform(articles_bodies).toarray() # generator from scipy

features = extract_features()

print(len(features))
# 10377
print(len(features[0]))
# 70793 (bag of words) or
# 1000 (feature hashing)

eighty_percent = int(len(features) * 0.8) # Used for dividing the dataset into
                                          # training and validation parts
training_data = features[:eighty_percent]
training_labels = labels[:eighty_percent]

testing_data = features[eighty_percent:]
testing_labels = labels[eighty_percent:]

from sklearn.ensemble import RandomForestClassifier

rfc = RandomForestClassifier(50)
rfc.fit(training_data, training_labels)

print(rfc.score(testing_data, testing_labels))




