import sys

import matplotlib.pyplot as plt
import numpy as np

def get_sizes(filenames):
    sizes = []
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as f:
            n = 0
            for line in f:
                if line.startswith('#'):
                    pass
                elif line.strip():
                    n += 1
                else:
                    assert n
                    sizes.append(n)
                    n = 0
    return sizes

sizes = get_sizes(sys.argv[1:])
plt.hist(sizes, 10)
plt.xlabel('Number of sign tokens')
plt.ylabel('Number of trees')
plt.savefig('treesizes.pdf')

print('Mean', np.mean(sizes))
print('Median', np.median(sizes))

