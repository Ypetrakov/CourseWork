import numpy as np

from generator import Generator
from main import Test, Solver


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

        print("Зберегти результати в файл?")
        self.print_menu({1: 'Так', 2: 'Ні'})
        wait = True
        option = int(input('Введіть ваш вибір: '))
        while wait:
            match option:
                case 1:
                    wait = False
                    # Code for saving it somewhere
                case 2:
                    wait = False
                case _:
                    print("Оберіть одну з опцій.")

    def InitialUI(self):
        menu = {
            1: 'Згенерувати випадкову задачу',
            2: 'Ввести таблицю інгредієнтів вручну',
            3: 'Зчитати задачу з таблиці інгредієнтів (excel)',
            4: 'Виконати тестування',
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
                        ings = input("Номери інгредієнтів: ").split(" ")
                        a[i] = [int(x) for x in ings]
                    c = Generator.get_c(a)
                    print("Матриця відстаней:")
                    print(c)

                    self.solving((a, c))
                case 3:
                    print("Оберіть одну з опцій.")
                    # Code for reading ingredients table from file
                case 4:
                    test = Test("initial_data")
                    test.start_experiment()
                    test.graph_result()
                case 5:
                    return
                case _:
                    print("Оберіть одну з опцій.")


if __name__ == '__main__':
    interface = Interface()
    interface.InitialUI()
