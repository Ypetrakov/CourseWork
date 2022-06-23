import numpy as np

from Algorithms.algorithm import Algorithm


class Greedy(Algorithm):
    def solve(self, a, c):
        # Derive length-based traits
        n = len(a) - 1
        K = len(a[0])

        x = []
        i = n
        while len(x) < n:
            def target_function(j):
                return (K + 1) * c[i][j] + np.count_nonzero(a[j])
            x.append(i)
            k = min([j for j in range(0, n) if j not in x], key=target_function)
            i = k
        # Add the last found state in
        x.append(i)
        # Add empty state in
        x.append(n)
        return x, self.evaluate(x, c)

    @staticmethod
    def evaluate(x, c):
        sum = 0
        for i in range(1, len(x)):
            sum += int(c[x[i-1]][x[i]])
        return sum


if __name__ == '__main__':
    import generator
    task = generator.Generator.generate_task(5)
    print(task[1])
    print(Greedy().solve(task[0], task[1]))