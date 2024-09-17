from prettytable import PrettyTable
from time import process_time
import matplotlib.pyplot as plt
from typing import Tuple, List

from work_mat import generate_random_two_mat

# константы
DEF_TEST_COUNT_RUNS = 50

DEF_TEST_START_SIZE_MAT = 10
DEF_TEST_FINAL_SIZE_MAT = 100
DEF_TEST_STEP_SIZE_MAT = 9

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
def build_time_graph_one_algo(algo_test: Tuple[any], start_size_mat: int = DEF_TEST_START_SIZE_MAT, final_size_mat: int = DEF_TEST_FINAL_SIZE_MAT, step_size_mat: int = DEF_TEST_STEP_SIZE_MAT) -> List[float]:
    x_arr, y_arr = [], []
    for size_str in range(start_size_mat, final_size_mat + 1, step_size_mat):
        #print(size_str)
        res_time = time_measurements(run_func_make_params, (algo_test[0], generate_random_two_mat, (size_str,)))
        res_time -= time_measurements(generate_random_two_mat, (size_str,))
        x_arr.append(size_str)
        y_arr.append(res_time)
    # Строим график
    plt.plot(x_arr, y_arr, label = algo_test[-1], marker = '*')
    return y_arr

# вызов функции замеряющей времени работы алгоритмов и отрисовка графика
def build_time_graph_all_algo(algo_list: List[Tuple[any]], start_size_mat: int = DEF_TEST_START_SIZE_MAT, final_size_mat: int = DEF_TEST_FINAL_SIZE_MAT, step_size_mat: int = DEF_TEST_STEP_SIZE_MAT) -> None:
    table = PrettyTable()
    table.field_names = ["алгоритм"] + [i for i in range(start_size_mat, final_size_mat + 1, step_size_mat)]
    for ind in range(len(algo_list)):
        y_arr = build_time_graph_one_algo(algo_list[ind], start_size_mat, final_size_mat, step_size_mat)
        table.add_row([algo_list[ind][-1]] + ["{:.2}".format(i) for i in y_arr])
        # Очищаем экран в командной строке
        print("\033[H\033[J")
        print(table)
    # Настройки и отображение графика
    plt.xlabel('Размерность матрицы (NxN)')
    plt.ylabel('Среднее время (сек)')
    plt.title('Замеры времени работы алгоритмов')
    plt.legend()
    plt.show()