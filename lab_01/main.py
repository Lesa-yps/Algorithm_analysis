# Талышева Олеся ИУ7-55Б
# Анализ алгоритмов лабораторная работа №1

from typing import Tuple

from algo import algo_list
from graph import build_time_graph_all_algo, run_func_make_params
from make_str import read_two_str


DEF_TEST_LEN_STR_MAT = (25, 125, 25)
DEF_TEST_LEN_STR_REC = (1, 9, 2)


# запуск функции с параметрами и вывод результата c поясняющей строкой
def ioput_run_algo(func_work, params: Tuple[any], strk: str = "") -> None:
    res = func_work(*params)
    print(strk, "выдал результат =", res)


# меню
def main() -> None:
    act_choose = -1
    while act_choose != 0:
        print("\nМеню:\n\
    0 - выход из программы\n\
    1 - запустить алгоритм Левенштейна (матричная реализация)\n\
    2 - запустить алгоритм Левенштейна (рекурсивная реализация)\n\
    3 - запустить алгоритм Левенштейна (рекурсивно-матричная реализация)\n\
    4 - запустить алгоритм Дамерау-Левенштейна (матричная реализация)\n\
    5 - запустить алгоритм Дамерау-Левенштейна (рекурсивная реализация)\n\
    6 - запустить алгоритм Дамерау-Левенштейна (рекурсивно-матричная реализация)\n\
    7 - запустить все алгоритмы\n\
    8 - провести замеры времени всех алгоритмов\n\
    9 - провести замеры времени матричных реализаций алгоритмов\n\
    10 - провести замеры времени рекурсивных реализаций алгоритмов\n\
    11 - провести замеры времени рекурсивно-матричных реализаций алгоритмов\n\
    12 - провести замеры времени рекурсивно-матричных и матричных реализаций алгоритмов\n\
    13 - провести замеры времени реализаций алгоритмов Левенштейна\n\
    14 - провести замеры времени реализаций алгоритмов Дамерау-Левенштейна\n\
    Введите выбранное действие: ", end = '')
        try:
            act_choose = int(input())
        except ValueError:
            act_choose = -1
            print("Ошибка ввода выбранного действия! Повторите попытку!")
            continue
        if act_choose >= 1 and act_choose <= 6:
            ioput_run_algo(run_func_make_params, (algo_list[act_choose - 1][0], read_two_str), algo_list[act_choose - 1][-1])
        elif act_choose == 7:
             params = read_two_str()
             for i in range(len(algo_list)):
                 ioput_run_algo(algo_list[i][0], params, algo_list[i][-1])
        elif act_choose == 8:
             build_time_graph_all_algo(algo_list)
        elif act_choose == 9:
             mat_algo_list = [algo_list[i] for i in range(len(algo_list)) if i % 3 == 0]
             build_time_graph_all_algo(mat_algo_list , *DEF_TEST_LEN_STR_MAT)
        elif act_choose == 10:
             rec_algo_list = [algo_list[i] for i in range(len(algo_list)) if i % 3 == 1]
             build_time_graph_all_algo(rec_algo_list, *DEF_TEST_LEN_STR_REC)
        elif act_choose == 11:
             rec_mat_algo_list = [algo_list[i] for i in range(len(algo_list)) if i % 3 == 2]
             build_time_graph_all_algo(rec_mat_algo_list, *DEF_TEST_LEN_STR_MAT)
        elif act_choose == 12:
             mat_and_rec_mat_algo_list = [algo_list[i] for i in range(len(algo_list)) if i % 3 != 1]
             build_time_graph_all_algo(mat_and_rec_mat_algo_list, *DEF_TEST_LEN_STR_MAT)
        elif act_choose == 13:
             Levenstein_algo_list = [algo_list[i] for i in range(int(len(algo_list) / 2))]
             build_time_graph_all_algo(Levenstein_algo_list, *DEF_TEST_LEN_STR_REC)
        elif act_choose == 14:
             Damerau_Levenstein_algo_list = [algo_list[i] for i in range(int(len(algo_list) / 2), len(algo_list))]
             build_time_graph_all_algo(Damerau_Levenstein_algo_list, *DEF_TEST_LEN_STR_REC)
        elif act_choose == 0:
            print("Программа завершена ^-^")
        else:
            print("Ошибка! Номер действия должен быть в интервале 0-14! Повторите попытку!")
    

if __name__ == "__main__":
    main()
    
