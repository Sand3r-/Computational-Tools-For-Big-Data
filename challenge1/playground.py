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

# Old version
# def get_search_range(line, Sbeg, Send, a, b):
#     found_pos = line.find(Sbeg)
#     beg = found_pos + len(Sbeg) + a
#     end = found_pos + len(Sbeg) + b + len(Send)
#     return beg, end

# New, taking into account overlapping matches
def get_search_range(line, Sbeg, Send, a, b):
    found_positions = [m.start() for m in re.finditer('(?=' + Sbeg + ')', line)]
    # found_pos = line.find(Sbeg)
    intervals = []
    for pos in found_positions:
        beg = pos + len(Sbeg) + a
        end = pos + len(Sbeg) + b + len(Send)
        intervals.append((beg, end))
        # beg = found_pos + len(Sbeg) + a
        # end = found_pos + len(Sbeg) + b + len(Send)
    return intervals
    #return beg, end

# Old version, not using intervals
# def find_sentence(line, S, boundaries):
#     found_pos = line.find(S[0])
#     if found_pos == -1:
#         return False, -1, -1
#     start_position = found_pos
#     for i in range(len(boundaries)):
#         a, b = boundaries[i]
#         beg, end = get_search_range(line, S[i], S[i+1], a, b)
#         found_pos = line[beg:end].find(S[i+1])
#         if found_pos == -1:
#             break
#     else:
#         end_position = beg + found_pos + len(S[len(boundaries)])
#         return True, start_position, end_position
#     return False, -1, -1

# New version using intevals
# K so imo the problem is that, the strings that are searched through
# they don't have enough characters (currently temp solved by
# adding inter[0]: instead of inter[0]:inter[1] in line 75 (new inter
# vals). You may wanna try this shit on paper to see if it makes
# sense, it'll be a sure way to debug this, although might take long.
# AND BTW! RUN THE PREPROCESSING WHEN GOING TO DO THE DINNER)
def find_sentence(line, S, boundaries):
    found_pos = line.find(S[0])
    if found_pos == -1:
        return False, []
    intervals = [line]
    start_position = found_pos
    end_positions = []
    for i in range(len(boundaries)):
        a, b = boundaries[i]
        new_intervals = []
        for j in range(len(intervals)):
            checked_intervals = get_search_range(intervals[j], S[i], S[i+1], a, b)
            for n in range(len(checked_intervals)):
                beg, end = checked_intervals[n]
                found_pos = intervals[j][beg:end].find(S[i+1])
                if found_pos == -1:
                    del checked_intervals[n]
                elif i == len(boundaries) - 1:
                    found_positions = [m.start() for m in re.finditer('(?=' + S[i+1] + ')', line)]
                    end_positions = end_positions + found_positions
            new_intervals = new_intervals + [intervals[j][inter[0]:inter[1]] for inter in checked_intervals]
            print(new_intervals)
        if not new_intervals:
            break
        else:
            intervals = new_intervals
    else:
        found_intervals = []
        for end in end_positions:
            end_position = end + len(S[len(boundaries)])
            found_intervals.append((start_position, end_position))
        return True, found_intervals
    return False, []

article = "For instance, cats are able to tolerate"

article = str(article)

index = 0
solutions = []
while index < len(article): # - len(S[len(S)-1]) perhaps??
    found, intervals = find_sentence(article[index:], S, boundaries)
    if found:
        for start, end in intervals:
            solutions.append(article[index + start:index + end].encode(sys.stdout.encoding, errors='replace'))
        index = index + start + len(S[0])
    else:
        index = index + len(S[0]) # If there is a repeating string, we should incr by that repeating part

for solution in solutions:
    print(solution)