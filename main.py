import numpy as np
from generator import generate_tusk
from greed import greed_alg
from aco import aco
from branc_and_bound import branch_and_bound_alg
from statistics import mean
import timeit


def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = timeit.default_timer()
        result = func(*args, **kwargs)
        t2 = timeit.default_timer()
        return result, t2 - t1

    return wrap_func


def do_experiment(R, N):
    average_time = np.zeros(shape=(len(R), 3))
    average_z = np.zeros(shape=(len(R), 3))
    i = 0
    for n in R:

        time_iterations = np.zeros(shape=(3, N))
        z_iterations = np.zeros(shape=(3, N))
        for j in range(0, N):
            k, a, c = generate_tusk(n)
            z_iterations[0][j], time_iterations[0][j] = timer_func(greed_alg)()
            z_iterations[1][j], time_iterations[1][j] = timer_func(branch_and_bound_alg)()
            z_iterations[2][j], time_iterations[2][j] = timer_func(aco)()
        average_time[i] = [mean(time_iterations[0]), mean(time_iterations[0]), mean(time_iterations[0])]
        average_z[i] = [mean(z_iterations[0]), mean(z_iterations[0]), mean(z_iterations[0])]
        i += 1
    print(average_time)
    print(average_z)
    return 1


if __name__ == '__main__':
    do_experiment([5, 10, 20, 30, 40, 50], 10)
