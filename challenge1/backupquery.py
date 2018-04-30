def find_sentence(line, S, boundaries):
    found_pos = line.find(S[0]) # Check if at least the first word can be found in the line
    if found_pos == -1:
        return False, []
    intervals = [(0, line)] # first value is the offset from the line
    start_position = found_pos
    end_positions = []
    for i in range(len(boundaries)):
        a, b = boundaries[i]
        new_intervals = []
        for j in range(len(intervals)):
            valid_intervals = []
            checked_intervals = get_search_range(intervals[j][1], S[i], S[i+1], a, b)
            for n in range(len(checked_intervals)):
                beg, end = checked_intervals[n]
                found_pos = intervals[j][1][beg:end].find(S[i+1])
                if found_pos != -1: # next word was found
                    valid_intervals.append((intervals[j][0], checked_intervals[n]))

                if i == len(boundaries) - 1:
                    found_positions = [m.start() for m in re.finditer('(?=' + S[i+1] + ')', line)]
                    end_positions = end_positions + found_positions
            new_intervals = new_intervals + [line[offset + inter[0]:offset + inter[1]] for offset, inter in valid_intervals]
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
