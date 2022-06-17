import numpy as np
from generator import Generator
from Algorithms.greed import Greedy
from Algorithms.aco import ACO
from Algorithms.branc_and_bound import BranchAndBound
from graphs import Grapher
from statistics import mean
import timeit


class Test:
    @staticmethod
    def timer_func(func, a, c):
        def wrap_func(*args, **kwargs):
            t1 = timeit.default_timer()
            result = func(*args, **kwargs)[1]
            t2 = timeit.default_timer()
            return result, t2 - t1

        return wrap_func(a, c)

    def __init__(self, initial_data_file):
        with open(initial_data_file) as f:
            self.R = list(map(int, f.readline().split(', ')))
            self.N = int(f.readline())
            self.average_time = np.zeros(shape=(len(self.R), 3))
            self.average_z = np.zeros(shape=(len(self.R), 3))

    def start_experiment(self):
        i = 0
        for n in self.R:
            print(n)
            time_iterations = np.zeros(shape=(3, self.N))
            z_iterations = np.zeros(shape=(3, self.N))
            for j in range(0, self.N):
                a, c = Generator.generate_task(n)
                z_iterations[0][j], time_iterations[0][j] = self.timer_func(Greedy().solve, a, c)
                z_iterations[1][j], time_iterations[1][j] = self.timer_func(BranchAndBound().solve, a, c)
                z_iterations[2][j], time_iterations[2][j] = self.timer_func(ACO().solve, a, c)
                print(z_iterations[:, j], time_iterations[:, j])
            self.average_time[i] = [mean(time_iterations[0]), mean(time_iterations[0]), mean(time_iterations[0])]
            self.average_z[i] = [mean(z_iterations[0]), mean(z_iterations[0]), mean(z_iterations[0])]
            i += 1

    def print_result(self):
        print(self.average_time)
        print(self.average_z)

    def graph_result(self):
        Grapher.plot_time(self.average_time[0], self.average_time[1], self.average_time[2], self.R)
        Grapher.plot_dev(self.average_z[0], self.average_z[1], self.average_z[2], self.R)


class Solver:
    @staticmethod
    def single_task(a, c):
        greedy = Greedy().solve(a, c)
        bandb = BranchAndBound().solve(a, c)
        ants = ACO().solve(a, c)
        return greedy, bandb, ants


if __name__ == '__main__':
    experiment = Test("initial_data")
    experiment.start_experiment()
    experiment.print_result()
