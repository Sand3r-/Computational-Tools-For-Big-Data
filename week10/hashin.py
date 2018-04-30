from scipy.sparse import csr_matrix

num_features = 10
article_bodies = ['Peter Piper picked a peck of pickled peppers', 
                  'A peck of pickled peppers Peter Piper picked', 
                  'If Peter Piper picked a peck of pickled peppers', 
                  'Where\'s the peck of pickled peppers Peter Piper picked?']

row_num = len(article_bodies)


row_indices = []
col_indices = []
data = []

for i in range(len(article_bodies)):
    words = article_bodies[i].split()
    current_row = [0] * num_features
    for word in words:
        col_idx = hash(word) % num_features
        current_row[col_idx] += 1
    for j in range(len(current_row)):
        if current_row[j] > 0:
            row_indices.append(i)
            col_indices.append(j)
            data.append(current_row[j])

features = csr_matrix((data, (row_indices, col_indices)), shape=(row_num, num_features), dtype=int)
print(features.toarray())
