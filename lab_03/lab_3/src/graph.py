from prettytable import PrettyTable
from time import process_time
import matplotlib.pyplot as plt
from typing import Tuple, List

from work_input import generate_random_arr_x

# константы
DEF_TEST_COUNT_RUNS = 50

DEF_TEST_START_SIZE_ARR = 10
DEF_TEST_FINAL_SIZE_ARR = 100
DEF_TEST_STEP_SIZE_ARR = 10

# запуск переданной функции с параметрами, которые сгенерировала другая функция
def run_func_make_params(func_work, func_make_main_params, params = ()) -> any:
    main_params = func_make_main_params(*params)
    res = func_work(*main_params)
    return res

# замеры времени работы функции
def time_measurements(func_test, params, count_runs: int = DEF_TEST_COUNT_RUNS) -> float:
    calc_algo_time = process_time()
    for _ in range(count_runs):
        func_test(*params)
    calc_algo_time = (process_time() - calc_algo_time) / count_runs
    return calc_algo_time

# вызов функции замеряющей времени работы алгоритма и отрисовка графика
def build_time_graph_one_algo(algo_test: Tuple[any], start_size_arr: int = DEF_TEST_START_SIZE_ARR, final_size_arr: int = DEF_TEST_FINAL_SIZE_ARR, step_size_arr: int = DEF_TEST_STEP_SIZE_ARR) -> List[float]:
    x_arr, y_arr = [], []
    for size_arr in range(start_size_arr, final_size_arr + 1, step_size_arr):
        #print(size_arr)
        res_time = time_measurements(run_func_make_params, (algo_test[0], generate_random_arr_x, (size_arr,)))
        res_time -= time_measurements(generate_random_arr_x, (size_arr,))
        x_arr.append(size_arr)
        y_arr.append(res_time)
    # Строим график
    plt.plot(x_arr, y_arr, color = algo_test[1], label = algo_test[-1], marker = '*')
    return y_arr

# вызов функции замеряющей времени работы алгоритмов и отрисовка графика
def build_time_graph_all_algo(algo_list: List[Tuple[any]], start_size_arr: int = DEF_TEST_START_SIZE_ARR, final_size_arr: int = DEF_TEST_FINAL_SIZE_ARR, step_size_arr: int = DEF_TEST_STEP_SIZE_ARR) -> None:
    table = PrettyTable()
    table.field_names = ["алгоритм"] + [i for i in range(start_size_arr, final_size_arr + 1, step_size_arr)]
    for ind in range(len(algo_list)):
        y_arr = build_time_graph_one_algo(algo_list[ind], start_size_arr, final_size_arr, step_size_arr)
        table.add_row([algo_list[ind][-1]] + ["{:.2}".format(i) for i in y_arr])
        # Очищаем экран в командной строке
        print("\033[H\033[J")
        print(table)
    # Настройки и отображение графика
    plt.xlabel('Размерность массива (N)')
    plt.ylabel('Среднее время (сек)')
    plt.title('Замеры времени работы алгоритмов')
    plt.legend()
    plt.show()