# Талышева Олеся ИУ7-55Б
# Анализ алгоритмов лабораторная работа №2

from typing import Tuple

from algo import algo_list
from graph import build_time_graph_all_algo, run_func_make_params
from bar_graph import build_linear_search_histogram, build_binary_search_histogram, build_binary_search_sorted_by_comparisons
from work_input import read_arr_x

DEF_TEST_SIZE_ARR = (10000, 20000, 1000)
# массив для тестов
ARR_BAR_GRAPH = [i for i in range(50)]
STEP_BAR_GRAPH = 1


# запуск функции с параметрами и вывод результата c поясняющей строкой
def ioput_run_algo(func_work, params: Tuple[any], strk: str = "") -> None:
    res = func_work(*params)
    if res < 0:
        print(strk, " - элемент не найден.")
    else:
        print(strk, "выдал индекс:", res)


# меню
def main() -> None:
    act_choose = -1
    while act_choose != 0:
        print("\nМеню:\n\
    0 - выход из программы\n\
    1 - запустить стандартный алгоритм поиска\n\
    2 - запустить бинарный алгоритм поиска\n\
    3 - запустить все алгоритмы\n\
    4 - провести замеры времени работы алгоритмов\n\
    5 - провести замеры числа сравнений для линейного алгоритма\n\
    6 - провести замеры числа сравнений для бинарного алгоритма\n\
    7 - провести замеры числа сравнений для бинарного алгоритма (с сортировкой по числу сравнений)\n\
    Введите выбранное действие: ", end = '')
        try:
            act_choose = int(input())
        except ValueError:
            act_choose = -1
            print("Ошибка ввода выбранного действия! Повторите попытку!")
            continue
        if act_choose >= 1 and act_choose <= 2:
            ioput_run_algo(run_func_make_params, (algo_list[act_choose - 1][0], read_arr_x), algo_list[act_choose - 1][-1])
        elif act_choose == 3:
             params = read_arr_x()
             for i in range(len(algo_list)):
                 ioput_run_algo(algo_list[i][0], params, algo_list[i][-1])
        elif act_choose == 4:
             build_time_graph_all_algo(algo_list, *DEF_TEST_SIZE_ARR)
        # Построение гистограмм
        elif act_choose == 5:
            build_linear_search_histogram(ARR_BAR_GRAPH, STEP_BAR_GRAPH)
        elif act_choose == 6:
            build_binary_search_histogram(ARR_BAR_GRAPH, STEP_BAR_GRAPH)
        elif act_choose == 7:
            build_binary_search_sorted_by_comparisons(ARR_BAR_GRAPH, STEP_BAR_GRAPH)
        elif act_choose == 0:
            print("Программа завершена ^-^")
        else:
            print("Ошибка! Номер действия должен быть в интервале 0-7! Повторите попытку!")
    

if __name__ == "__main__":
    main()
    
