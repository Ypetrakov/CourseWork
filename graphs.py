import matplotlib.pyplot as plt


class Grapher:
    @staticmethod
    def plot_time(res_1, res_2, res_3, R):
        plt.figure(1)
        plt.plot(R, res_1, label='Жадібний алгоритм')
        plt.plot(R, res_2, label='Метод гілок та меж')
        plt.plot(R, res_3, label='Алгоритм мурашиних колоній')
        # plt.xlim([0, ???])
        # plt.ylim([0, ???])
        plt.xlabel('Розмірність задачі')
        plt.ylabel('Час виконання')
        plt.grid(True)
        plt.legend()
        plt.show()

    @staticmethod
    def plot_dev(res_1, res_2, res_3, R):
        plt.figure(2)
        plt.plot(R, res_1, label='Жадібний алгоритм')
        plt.plot(R, res_2, label='Метод гілок та меж')
        plt.plot(R, res_3, label='Алгоритм мурашиних колоній')
        # plt.xlim([0, ???])
        # plt.ylim([0, ???])
        plt.xlabel('Розмірність задачі')
        plt.ylabel('Похибка')
        plt.grid(True)
        plt.legend()
        plt.show()


if __name__ == "__main__":
    Grapher.plot_dev([0.2, 0.2, 0.2], [0.3, 0.2, 0.2], [0.1, 0.1, 0.1], [1, 2, 3])
    Grapher.plot_dev([2, 2, 2], [3, 2, 2], [0, 0, 0], [1, 2, 3])
