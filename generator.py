import math
from time import time

import numpy as np
import random

""" function to generate individual task
input: n - The amount of juices in an individual task (does not include an empty state)
output: k - amount of ingredients
        a - table of ingredients
        c - Distance matrix
"""


def generate_tusk(n):
    k = int(1.25 * math.log2(n + 1))
    a = np.zeros(shape=(n + 1, k))
    c = np.zeros(shape=(n + 1, n + 1))

    for i in range(0, k):
        for j in range(0, n):
            a[j][i] = round(random.uniform(0, 1))
        a[n][i] = 0

    for i in range(0, n + 1):
        for j in range(0, n + 1):
            if i == j:
                c[i][j] = float('-inf')
            elif all([a[i][l] <= a[j][l] for l in range(0, k)]):
                c[i][j] = 0
            else:
                c[i][j] = 1
    return k, a, c


if __name__ == "__main__":
    generate_tusk(5)
