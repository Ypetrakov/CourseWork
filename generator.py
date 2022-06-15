import math
import numpy as np
import random


class Generator:
    """ function to generate individual task
    input: n - The amount of juices in an individual task (does not include an empty state)
    output: k - amount of ingredients
            a - table of ingredients
            c - Distance matrix
    """

    @staticmethod
    def generate_task(n):
        # The log has to round up - otherwise it may break on certain values
        k = math.ceil(1.25 * math.log2(n + 1))
        a = np.zeros(shape=(n + 1, k))

        # Represent the sum of ai* as one number, which can be converted to binary to determine ail
        # No need to comb over all previously generated values over and over
        temp_a = random.sample(range(1, pow(2, k)), n)
        for i in range(0, n):
            temp_a[i] = list(bin(temp_a[i])[2:].zfill(k))
            for l in range(0, len(temp_a[i])):
                temp_a[i][l] = int(temp_a[i][l])
            a[i] = temp_a[i]
        a[n] = [0] * k

        c = Generator.get_c(a)
        return a, c

    """ 
    Create distance array C based off of ingredients table a
    Seperating it out will be useful for reading from files
    """

    @staticmethod
    def get_c(a):
        n = len(a) - 1
        k = len(a[0])
        c = np.zeros(shape=(n + 1, n + 1))

        for i in range(0, n + 1):
            for j in range(0, n + 1):
                if i == j:
                    c[i][j] = np.inf
                elif all([a[i][l] <= a[j][l] for l in range(0, k)]):
                    c[i][j] = 0
                else:
                    c[i][j] = 1
        return c


if __name__ == "__main__":
    print(Generator.generate_task(5))
