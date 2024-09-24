# Талышева Олеся ИУ7-55Б
# Анализ алгоритмов лабораторная работа №2

from typing import Tuple

from algo import algo_list, OK, ERROR
from graph import build_time_graph_all_algo, run_func_make_params
from work_mat import read_two_mat, output_mat


DEF_TEST_SIZE_MAT_EVEN = (50, 250, 50)
DEF_TEST_SIZE_MAT_ODD = (51, 251, 50)


# запуск функции с параметрами и вывод результата c поясняющей строкой
def ioput_run_algo(func_work, params: Tuple[any], strk: str = "") -> None:
    res_mat, err_code = func_work(*params)
    if not err_code:
        print(strk, "для входных матриц посчитать невозможно.")
    else:
        print(strk, "выдал результат:")
        output_mat(res_mat)


# меню
def main() -> None:
    act_choose = -1
    while act_choose != 0:
        print("\nМеню:\n\
    0 - выход из программы\n\
    1 - запустить стандартный алгоритм умножения матриц\n\
    2 - запустить алгоритм Винограда умножения матриц\n\
    3 - запустить алгоритм Винограда (оптимизированный) умножения матриц\n\
    4 - запустить все алгоритмы\n\
    5 - провести замеры времени работы алгоритмов на чётных размерностях\n\
    6 - провести замеры времени работы алгоритмов на нечётных размерностях\n\
    Введите выбранное действие: ", end = '')
        try:
            act_choose = int(input())
        except ValueError:
            act_choose = -1
            print("Ошибка ввода выбранного действия! Повторите попытку!")
            continue
        if act_choose >= 1 and act_choose <= 3:
            ioput_run_algo(run_func_make_params, (algo_list[act_choose - 1][0], read_two_mat), algo_list[act_choose - 1][-1])
        elif act_choose == 4:
             params = read_two_mat()
             for i in range(len(algo_list)):
                 ioput_run_algo(algo_list[i][0], params, algo_list[i][-1])
        elif act_choose == 5:
             build_time_graph_all_algo(algo_list, *DEF_TEST_SIZE_MAT_EVEN)
        elif act_choose == 6:
             build_time_graph_all_algo(algo_list, *DEF_TEST_SIZE_MAT_ODD)
        elif act_choose == 0:
            print("Программа завершена ^-^")
        else:
            print("Ошибка! Номер действия должен быть в интервале 0-6! Повторите попытку!")
    

if __name__ == "__main__":
    main()
    
