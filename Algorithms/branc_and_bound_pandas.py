import string

import numpy as np
import pandas as pd
from Algorithms.algorithm import Algorithm


# Convert int value to pandas row/column call
def _itoc(char: string, i: int):
    return char + str(i)


# Convert pandas row/column call to int value
def _ctoi(call: string):
    return int(call[1:])


class BranchAndBound(Algorithm):
    def __init__(self):
        self.Xopt = []
        self.Hopt = np.Inf
        self.C = pd.DataFrame()

    def solve(self, a, c):
        # Converting numpy array to pandas dataframe
        pd_len = range(0, len(c))
        c_pd = pd.DataFrame(c, index=[_itoc('r', x) for x in pd_len], columns=[_itoc('c', x) for x in pd_len])
        self.C = c_pd
        self.b_and_b(c_pd.copy(), [], 0)
        return self.Xopt, self.Hopt

    def b_and_b(self, m: pd.DataFrame, A: list, h: int):
        # Reduce matrix and increase the lower estimate
        m, h = self.reduce(m, h)
        if h >= self.Hopt:
            return
        i, j = self.choose_arc(m)
        # (-1, -1) is a dummy value, indicating that choose_arc failed to find an arc
        # because the matrix is all infs
        if (i, j) == (-1, -1):
            return
        # States that include the arc
        # If only 2 arcs left (i, j) not officially in A yet), only one full cycle is possible
        if len(A) == len(self.C) - 3:
            X = self.find_cycle(A + [(i, j)])
            H = self.evaluate(X)
            # If new solution better than current best solution, replace the best
            if H < self.Hopt:
                self.Xopt, self.Hopt = X, H
        # If more than 3 elements, start a new iteration
        else:
            Mnew = m.copy()
            # It's hard to delete rows or columns, but we can mark them as inf, effectively deleting them
            Mnew = Mnew.drop(_itoc('r', i), axis=0)
            Mnew = Mnew.drop(_itoc('c', j), axis=1)
            l, t = self.end_cycle(A, (i, j))[:2]
            Mnew.at[_itoc('r', l), _itoc('c', t)] = np.Inf
            self.b_and_b(Mnew, A + [(i, j)], h)
        # States that exclude the arc
        m.at[_itoc('r', i), _itoc('c', j)] = np.Inf
        self.b_and_b(m, A, h)
        return

    @staticmethod
    def reduce(m: pd.DataFrame, h: int):
        # Row reduction
        for r in m.index:
            h_temp = m.loc[r].min()
            # You can't reduce a deleted row
            if h_temp == np.Inf:
                h_temp = 0
            if h_temp != 0:
                h += h_temp
                m.loc[r] -= h_temp
        # Column reduction
        for c in m.columns:
            h_temp = m[c].min()
            # You can't reduce a deleted column
            if h_temp == np.Inf:
                h_temp = 0
            if h_temp != 0:
                h += h_temp
                m[c] -= h_temp
        return m, h

    @staticmethod
    def choose_arc(m: pd.DataFrame):
        w = -np.Inf
        # Dummy value, causes a special response in the main function
        k = (-1, -1)
        for r in m.index:
            for c in m.columns:
                if m.at[r, c] == 0:
                    p = m[m.index != r].min().min()
                    v = m[m.columns != c].min().min()
                    # If both p and v are Inf, this evaluates false
                    if (p + v) > w:
                        w = p + v
                        k = (_ctoi(r), _ctoi(c))
        return k

    @staticmethod
    def find_cycle(A):
        a1 = [x for (x, y) in A]
        a2 = [y for (x, y) in A]
        # Try to find element not features in list of req. arcs
        mid = [x for x in range(0, len(A) + 2) if a1.count(x) == 0 and a2.count(x) == 0]
        # If independent element found - arcs is one cycle, just add arcs for its edges
        if mid:
            mid = mid[0]
            forw, back = BranchAndBound.end_cycle(A, A[0])[:2]
            A.append((forw, mid))
            A.append((mid, back))
        # If no independent element found - arcs is split in two cycles, need to find a way to connect them
        else:
            # Front & back edges of both cycles
            exits = [x for x in a2 if x not in a1]
            entrances = [x for x in a1 if x not in a2]
            # Determine which way of connecting them produces the longer cycle
            conn1_eval = BranchAndBound.end_cycle(A + [(exits[0], entrances[0])],
                                                  (exits[1], entrances[1]))[2]
            conn2_eval = BranchAndBound.end_cycle(A + [(exits[0], entrances[1])],
                                                  (exits[1], entrances[0]))[2]
            if conn1_eval > conn2_eval:
                A.append((exits[0], entrances[0]))
                A.append((exits[1], entrances[1]))
            else:
                A.append((exits[0], entrances[1]))
                A.append((exits[1], entrances[0]))

        # Sorting it so that it's all ordered & starts from empty cup
        adjacency_matrix = {pair[0]: pair for pair in A}
        first_key = max(adjacency_matrix)
        sorted_A = [adjacency_matrix.pop(first_key)]
        while adjacency_matrix:
            sorted_A.append(adjacency_matrix.pop(sorted_A[-1][1]))
        return sorted_A

    @staticmethod
    def end_cycle(A, k):
        cycle_len = 1
        # Forward finish
        forw = k[1]
        while [a for a in A if a[0] == forw]:
            cycle_len += 1
            forw = [a for a in A if a[0] == forw][0][1]
        # Backward finish
        back = k[0]
        while [a for a in A if a[1] == back]:
            cycle_len += 1
            back = [a for a in A if a[1] == back][0][0]
        # Determine edges
        return forw, back, cycle_len

    def evaluate(self, X: list):
        cycle_sum = 0
        for x in X:
            cycle_sum += int(self.C.at[_itoc('r', x[0]), _itoc('c', x[1])])
        return cycle_sum


if __name__ == '__main__':
    import generator

    task = generator.Generator.generate_task(10)
    print(task[1])
    print(BranchAndBound().solve(task[0], task[1]))
