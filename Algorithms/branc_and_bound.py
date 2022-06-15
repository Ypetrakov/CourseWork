from functools import cmp_to_key

import numpy as np
from Algorithms.algorithm import Algorithm


class BranchAndBound(Algorithm):
    def __init__(self):
        self.Xopt = []
        self.Hopt = np.Inf
        self.C = []

    def solve(self, a, c):
        self.C = c
        self.b_and_b(c, [], 0)
        return self.Xopt, self.Hopt

    def b_and_b(self, m: np.array, A: list, h: int):
        m, h = self.reduce(m, h)
        if h >= self.Hopt:
            # print("Solution too fat, breaking.")
            # print("A at time of break: "+str(A))
            return
        i, j = self.choose_arc(m)
        # States that include the arc
        if len(A) == len(m) - 3:
            X = self.find_cycle(A + [(i, j)])  # Write up later
            H = self.evaluate(X)
            if H < self.Hopt:
                self.Xopt, self.Hopt = X, H
            # print("Cycle assembled.")
            # print("A at time of break: "+str(A + [(i, j)]))
            # print("X at time of break: "+str(X))
        else:
            Mnew = np.copy(m)
            for t in range(0, len(m)):
                Mnew[i][t] = np.Inf
                Mnew[t][j] = np.Inf
            # print("Column "+str(j)+" and row "+str(i)+" removed.")
            l, t = self.end_cycle(A, (i, j))
            Mnew[l][t] = np.Inf
            # print("Slot "+str(l) + " " +str(t) + " infinitized.")
            # print(Mnew)
            self.b_and_b(Mnew, A + [(i, j)], h)
        # States that exclude the arc
        m[i][j] = np.Inf
        # print("Slot "+str(i) + " " +str(j) + " infinitized.")
        # print(m)
        self.b_and_b(m, A, h)
        return

    @staticmethod
    def reduce(m: np.array, h: int):
        # Row reduction
        for i in range(0, len(m)):
            h_temp = min(min(m[i] + [1]), 1)
            h += h_temp
            for j in range(0, len(m[0])):
                m[i, j] -= h_temp

        # Column reduction
        for j in range(0, len(m[0])):
            h_temp = min(min(m[:, j]), 1)
            h += h_temp
            for i in range(0, len(m)):
                m[i, j] -= h_temp

        return m, h

    @staticmethod
    def choose_arc(m: np.array):
        w = -np.Inf
        for i in range(0, len(m)):
            for j in range(0, len(m[0])):
                if m[i][j] == 0:
                    p = min(np.concatenate((m[i, :j], m[i, j+1:])))
                    v = min(np.concatenate((m[:i, j], m[i+1:, j])))
                    if (p + v) > w:
                        w = p + v
                        k = (i, j)
        return k

    # UNFINISHED, NOT DONE, NEED TO WORK ON IT
    @staticmethod
    def find_cycle(A):
        forw, back = BranchAndBound.end_cycle(A, A[0])
        a1 = [x for (x, y) in A]
        a2 = [y for (x, y) in A]
        mid = [x for x in range(0, len(A)+2) if a1.count(x) == 0 and a2.count(x) == 0]
        mid = mid[0]
        A.append((forw, mid))
        A.append((mid, back))
        # Can't get the sort to work, IDK
        # A.sort(key=cmp_to_key(lambda x, y: x[1] != y[0]))
        return A

    @staticmethod
    def end_cycle(A, k):
        # Forward finish
        forw = k[1]
        while [a for a in A if a[0] == forw]:
            forw = [a for a in A if a[0] == forw][0][1]
        # Backward finish
        back = k[0]
        while [a for a in A if a[1] == back]:
            back = [a for a in A if a[1] == back][0][0]
        # Determine edges
        return forw, back

    def evaluate(self, X: list):
        sum = 0
        for x in X:
            sum += self.C[x[0]][x[1]]
        return sum


if __name__ == '__main__':
    import generator
    task = generator.Generator.generate_task(25)
    print(BranchAndBound().solve(task[0], task[1]))