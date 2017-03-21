import sys
import re
import numpy as np

length = 0
lengths = []
for line in sys.stdin:
    if re.match(r'\d+\t', line):
        pos = line.rstrip('\n').split('\t')[3]
        if pos != 'PUNCT':
            length += 1
    elif line.startswith('#') or re.match(r'\d+-\d+', line):
        pass
    elif not line.strip():
        lengths.append(length)
        length = 0
    else:
        raise ValueError(line)

print('mean', np.mean(lengths), 'median', np.median(lengths))
print(len(lengths), 'trees', sum(lengths), 'tokens')

