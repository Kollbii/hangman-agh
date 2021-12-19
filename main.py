f  = open('slowa.txt', 'r')

lines = [line.strip() for line in f.readlines()]

lst = sorted(lines, key=len)
occurences = {
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
    11: [],
    12: [],
    13: [],
    14: [],
    15: []
}

counted = {
    2: {},
    3: {},
    4: {},
    5: {},
    6: {},
    7: {},
    8: {},
    9: {},
    10: {},
    11: {},
    12: {},
    13: {},
    14: {},
    15: {}
}

for line in lines:
    occurences[len(line)].append(line)

for elem in occurences:
    print(elem,len(occurences[elem]))

from collections import Counter
import operator

total = dict(Counter())

for elem in occurences:
    whole_str = ''.join(word for word in occurences[elem])
    total = dict(Counter(whole_str))
    counted[elem] = dict(sorted(total.items(), key=operator.itemgetter(1), reverse=True))

f = open('temp.txt', 'w')
for elem in counted:
    f.write(f'Words of length {elem}. Total count {len(occurences[elem])}\n')
    f.write(str(list(counted[elem].keys())) + '\n')
