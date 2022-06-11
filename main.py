import numpy as np
from generator import Generator
from Algorithms.greed import greed_alg
from Algorithms.aco import aco
from Algorithms.branc_and_bound import branch_and_bound_alg
from statistics import mean
import timeit


def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = timeit.default_timer()
        result = func(*args, **kwargs)
        t2 = timeit.default_timer()
        return result, t2 - t1

    return wrap_func


class Main:

    def __init__(self, initial_data_file):

        with open(initial_data_file) as f:
            self.R = list(map(int, f.readline().split(', ')))
            self.N = int(f.readline())
            self.average_time = np.zeros(shape=(len(self.R), 3))
            self.average_z = np.zeros(shape=(len(self.R), 3))

    def start_experiment(self):
        i = 0
        for n in self.R:
            time_iterations = np.zeros(shape=(3, self.N))
            z_iterations = np.zeros(shape=(3, self.N))
            for j in range(0, self.N):
                k, a, c = Generator.generate_tusk(n)
                z_iterations[0][j], time_iterations[0][j] = timer_func(greed_alg)()
                z_iterations[1][j], time_iterations[1][j] = timer_func(branch_and_bound_alg)()
                z_iterations[2][j], time_iterations[2][j] = timer_func(aco)()
            self.average_time[i] = [mean(time_iterations[0]), mean(time_iterations[0]), mean(time_iterations[0])]
            self.average_z[i] = [mean(z_iterations[0]), mean(z_iterations[0]), mean(z_iterations[0])]
            i += 1

    def print_result(self):
        print(self.average_time)
        print(self.average_z)


if __name__ == '__main__':
    experiment = Main("initial_data")
    experiment.start_experiment()
    experiment.print_result()
