import os

import numpy as np

from generator import Generator
from test import Test, Solver
from read_write_data import IOData


class Interface:
    @staticmethod
    def print_menu(menu_options):
        for key in menu_options.keys():
            print(key, '--', menu_options[key])

    def solving(self, task):
        results = Solver.single_task(task[0], task[1])
        print("Розв'язки:")
        print("Жадібний алгоритм:")
        print(results[0])
        print("Метод гілок та меж:")
        print(results[1])
        print("Алгоритм мурашиних колоній:")
        print(results[2])

    def initial_UI(self):
        menu = {
            1: 'Згенерувати випадкову задачу',
            2: 'Ввести таблицю інгредієнтів вручну',
            3: 'Зчитати задачу з таблиці інгредієнтів (excel)',
            4: 'Виконати експеримент',
            5: 'Вийти',
        }
        while True:
            self.print_menu(menu)
            option = int(input('Введіть ваш вибір: '))
            match option:
                case 1:
                    print("Якого розміру повинно бути завдання?")
                    n = int(input('Введіть кількість соків: '))
                    task = Generator.generate_task(n)
                    print("Таблиця інгредієнтів:")
                    print(task[0])
                    print("Матриця відстаней:")
                    print(task[1])

                    self.solving(task)
                case 2:
                    print("Якого розміру повинно бути завдання?")
                    k = int(input('Введіть кількість інгредієнтів: '))
                    n = int(input('Введіть кількість соків: '))
                    a = np.zeros(shape=(n + 1, k))
                    for i in range(0, n):
                        print("Введіть номери інгредієнтів (від нуля) в " + str(i + 1) + "-му соці: ")
                        print("Приклад: 0 1 2 4 6")
                        ings = [int(x) for x in input("Номери інгредієнтів: ").split(" ")]
                        for j in range(0, k):
                            if j in ings:
                                a[i][j] = 1
                            else:
                                a[i][j] = 0
                    c = Generator.get_c(a)
                    print("Матриця відстаней:")
                    print(c)

                    self.solving((a, c))
                case 3:
                    print("Вкажіть розташування таблиці.")
                    print("(Без вибору, буде зчитуватися з data/input_data.xlsx)")
                    loc = input('Розташування таблиці: ')
                    if loc == '':
                        loc = 'data/input_data.xlsx'
                    a = IOData.get_data(loc)
                    
                    print("Таблиця інгредієнтів:")
                    print(a)
                    c = Generator.get_c(a)
                    print("Матриця відстаней:")
                    print(c)

                    self.solving((a, c))
                case 4:
                    test = Test("initial_data")
                    test.start_experiment()
                    test.graph_result()

                    print("Зберегти результати в файл?")
                    self.print_menu({1: 'Так', 2: 'Ні'})
                    wait = True
                    option = int(input('Введіть ваш вибір: '))
                    while wait:
                        match option:
                            case 1:
                                wait = False
                                IOData.output_data(test.average_time, test.average_z, test.R)
                                print("Результати збережено в "+os.getcwd()+"\data\output_data.xlsx")
                            case 2:
                                wait = False
                            case _:
                                print("Оберіть одну з опцій.")
                case 5:
                    return
                case _:
                    print("Оберіть одну з опцій.")


if __name__ == '__main__':
    interface = Interface()
    interface.initial_UI()
