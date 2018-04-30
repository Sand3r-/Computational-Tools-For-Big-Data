import sys, re

S = []
boundaries = []
for i in range(1, len(sys.argv) - 1):
    if i % 2 == 1:
        S.append(sys.argv[i].replace("\"", ""))
    else:
        bound_list = sys.argv[i].replace("[", "").replace("]", "").split(",")
        bound_list = list(map(int, bound_list))
        boundaries.append((bound_list[0], bound_list[1]))

seek_pos = -1

with open("index.txt", 'r', encoding="utf-8") as index_file:
    pattern = re.compile("^" + sys.argv[len(sys.argv) - 1] + ":") # TODO: do this as regexp
    for line in index_file:                                       # and save the result as list of 
        if pattern.match(line):                                   # pos:chunks to be processed later
            seek_pos, size = map(int, line.split(":")[1:])        # (tuples)^

if seek_pos < 0:
    print("No article found")
    exit(1)

with open("database.txt", 'rb') as db:
    db.seek(seek_pos)
    article = db.read(size)
    #print(article)

def get_search_range(line, Sbeg, Send, a, b):
    found_pos = line.find(Sbeg)
    beg = found_pos + len(Sbeg) + a
    end = found_pos + len(Sbeg) + b + len(Send)
    return beg, end

def find_sentence(line, S, boundaries):
    found_pos = line.find(S[0])
    if found_pos == -1:
        return False, -1, -1
    start_position = found_pos
    for i in range(len(boundaries)):
        a, b = boundaries[i]
        beg, end = get_search_range(line, S[i], S[i+1], a, b)
        found_pos = line[beg:end].find(S[i+1])
        if found_pos == -1:
            break
    else:
        end_position = beg + found_pos + len(S[len(boundaries)])
        return True, start_position, end_position
    return False, -1, -1

# line = "I have a really nice cat in hat at home. But he is really shy."

article = str(article)

index = 0
solutions = []
while index < len(article):
    found, start, end = find_sentence(article[index:], S, boundaries)
    if found:
        solutions.append(article[index + start:index + end].encode(sys.stdout.encoding, errors='replace'))
        index = index + start + len(S[0])
    else:
        index = index + len(S[0])

for solution in solutions:
    print(solution)