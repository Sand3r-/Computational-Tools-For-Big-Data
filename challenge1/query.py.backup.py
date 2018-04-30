''' #############
#### CLI Parsing ####
''' #############
import sys, os

# if len(sys.argv) < 4:
#     print("Please provide the query of form\n" +
#     "\"S1\" [a1,b1] \"S2\" ... \"Sx\" [ax,bx] \"Sx+1\" ... \"Sn-1\" [an,bn] \"Sn\"\n " +
#     "Where:\n" +
#     "S - string\n" +
#     "a - min number of characters to appear betweeen\n"
#     "b - max number of characters to appear betweeen\n")
#     exit(1)

# Simplest case:

S = ["cat", "hat", "But"]
boundaries = [(2, 4), (2, 30)]

'''
real    0m1.480s
user    0m0.000s
sys     0m0.062s
'''
for i in range(500000):

    line = "I have a really nice cat in hat at home. But he is really shy."

    start_position = -1
    last_position = 0
    next_chunk_line = line

    found_pos = next_chunk_line.find(S[0])
    start_position = found_pos
    a, b = boundaries[0]
    next_chunk_line = next_chunk_line[found_pos + len(S[0]) + a:]
    last_position = last_position +  found_pos + len(S[0]) + a

    found_pos = next_chunk_line[:b].find(S[1])
    a, b = boundaries[1]
    next_chunk_line = next_chunk_line[found_pos + len(S[1]) + a:]
    last_position = last_position +  found_pos + len(S[1]) + a

    found_pos = next_chunk_line[:b].find(S[2])
    last_position = last_position + found_pos + len(S[2])

    #print(line[start_position:last_position])

#for i in range(500000):

# line = "I have a really nice cat in hat at home. But he is really shy."

# start_position = -1

# found_pos = line.find(S[0])
# start_position = found_pos
# a, b = boundaries[0]

# print(line[found_pos + len(S[0]) + a:found_pos + len(S[0]) + a + b + len(S[1])])
# found_pos = line[found_pos + len(S[0]) + a:found_pos + len(S[0]) + a + b + len(S[1])].find(S[1])
# print(found_pos)
# a, b = boundaries[1]

# found_pos = line[found_pos + len(S[1]) + a:found_pos + len(S[1]) + a + b + len(S[2])].find(S[2])
# print(found_pos)
# print(line[start_position:found_pos+len(S[1]) + a + b + len(S[2])])

    # So the idea is as follows
    # Find string of some index
    # Read what follows that index (But up to max num of chars)
    # Check if the next word is inside
    # Then call that function recurrently to see if that new word
    # and following characters can find a new one and shits
    # TODO: Contemplate what should we do about the min number
    # And also on how to move on from a single match (probably
    # just add the relative index of found word to the left
    # boundary - so just [a + index + word_length, b])