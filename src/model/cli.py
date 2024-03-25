import pandas as pd
from neural_networks import CustomNN
from clearml import Task


HELP_TEXT = """task <name>
\tсоздаёт задачу clearml
\t<name>:str - название задачи

new <input_size> <output_size> <hidden_size> <hidden_count> <seed>
\tсоздаёт новую нейронную сеть
\t<input_size>:int - размер входных данных
\t<output_size>:int - размер выходных данных
\t<hidden_size>:int - размер скрытых слоёв
\t<hidden_count>:int - кол-во скрытых слоёв
\t<seed>:int - ключ для случайных значений

load_file <filepath|filename>
\tзагружает нейронную сеть из файла
\t<filepath|filename>:str - путь к файлу

save_file <filepath|filename>
\tсохраняет нейронную сеть в файл
\t<filepath|filename>:str - путь к файлу

train <training_data> <iterations> <learning_rate> <batch_size> <seed> [testing_data]
\tобучает нейронную сеть
\t<training_data>:str - путь к файлу данных для обучения
\t<iterations>:int - кол-во итераций
\t<learning_rate>:float - скорость обучения, большие значения ускоряют процесс, малые улучшают качество обучения (рекомендуется использовать 0.1, 0.01 и т.д.)
\t<batch_size>:int - размер частей при разбиении данных
\t<seed>:int - ключ для случайных значений
\t[testing_data]:str - путь к файлу данных для тестирования (выводит для каждой итерации результат тестов)

exit - выход из программы"""


def main():
    network = None
    task = None
    print('Введите "help" для списка команд')
    while True:
        try:
            print(">> ", end="")
            inp = input()
            if inp == "help":
                print(HELP_TEXT)
            elif inp.startswith("task"):
                task = Task.init("ProjectX", inp.split()[1])
            elif inp.startswith("new"):
                network = CustomNN(*map(int, inp.split()[1:6]))
            elif inp.startswith("load_file"):
                network = CustomNN.from_file(inp.split()[1])
            elif inp.startswith("save_file"):
                network.save_to_file(inp.split()[1])
            elif inp.startswith("train"):
                param = inp.split()
                network.train(
                    pd.read_csv(param[1]),
                    int(param[2]),
                    float(param[3]),
                    int(param[4]),
                    int(param[5]),
                    pd.read_csv(param[6]) if len(param) > 6 else None,
                    task.get_logger() if task is not None else None
                )
            elif inp == "exit":
                if task is not None:
                    task.close()
                break
            else:
                print("Неизвестная команда")
        except Exception as e:
            print("Ошибка обработки команды. Описание ошибки:")
            print(e)
            print(e.__traceback__.tb_next)


if __name__ == "__main__":
    main()
