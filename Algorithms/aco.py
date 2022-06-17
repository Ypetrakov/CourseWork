import random
import generator
from Algorithms.algorithm import Algorithm
import numpy as np


class ACO(Algorithm):

    def __init__(self):
        self.ant_count = 5
        self.max_iteration = 200
        self.alpha = 4
        self.rho = 0.8
        self.init_pheromone = 0.1
        self.path = []
        self.record = np.inf

    def solve(self, a, c):

        self._initialize_pheromone_matrix(len(c))
        record_not_changed = 0
        while record_not_changed < self.max_iteration:
            path = []
            z_value = np.inf
            visited_states = np.zeros(shape=(len(c), len(c), self.ant_count))
            z_values = np.zeros(shape=self.ant_count)
            for ant in range(self.ant_count):
                temp_path = []
                temp_z_value = 0
                available_states = [i for i in range(len(c) - 1)]
                current_state = len(c) - 1
                while available_states:
                    next_state = self._choose_next_state(available_states, current_state, c)
                    visited_states[current_state][next_state][ant] += 1
                    temp_path.append((current_state, next_state))
                    temp_z_value += c[current_state][next_state]
                    current_state = next_state

                    available_states.remove(next_state)
                temp_path.append((current_state, len(c) - 1))
                temp_z_value += 1

                z_values[ant] = temp_z_value

                if temp_z_value < z_value:
                    z_value = temp_z_value
                    path = temp_path

            self._update_pheromone_matrix(len(c), visited_states, z_values)
            # time.sleep(6)
            if z_value < self.record:
                self.record = z_value
                self.path = path
                record_not_changed = 0
            else:
                record_not_changed += 1

        return self.path, int(self.record)

    def _remove_node(self):
        pass

    def _choose_next_state(self, available_states, current_state, c):
        total = sum([self.pheromone_matrix[current_state][next_state] + (1 - c[current_state][next_state])
                     for next_state in available_states])
        transition_probabilities = [
            (self.pheromone_matrix[current_state][next_state] + (1 - c[current_state][next_state]))
            / total for next_state in available_states]
        distribution_values = [sum(transition_probabilities[:i]) for i in range(len(transition_probabilities) + 1)]
        random_number = random.uniform(0, 1)
        for i in range(len(distribution_values)):
            if distribution_values[i] < random_number < distribution_values[i + 1]:
                return available_states[i]
        return available_states[-1]

    def _initialize_pheromone_matrix(self, k):
        self.pheromone_matrix = np.full((k, k), self.init_pheromone)
        self.pheromone_matrix[np.eye(k) == 1] = 0

    def _update_pheromone_matrix(self, k, visited_states, z_values):
        for i in range(k):
            for j in range(k):
                delta_r = 0
                for ant in range(self.ant_count):
                    if visited_states[i][j][ant]:
                        delta_r += z_values[ant]
                self.pheromone_matrix[i][j] = (1 - self.rho) * self.pheromone_matrix[i][j] + delta_r


if __name__ == "__main__":
    task = generator.Generator.generate_task(10)
    # print(task[0])
    print(ACO().solve(task[0], task[1]))
