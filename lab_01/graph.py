from time import process_time
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from typing import Tuple, List

from make_str import generate_random_two_str

# константы
DEF_TEST_COUNT_RUNS = 50
DEF_TEST_START_LEN_STR = 1 #100
DEF_TEST_FINAL_LEN_STR = 8 #1000
DEF_TEST_STEP_LEN_STR = 1 #100


# запуск переданной функции с параметрами, которые сгенерировала другая функция
def run_func_make_params(func_work, func_make_main_params, params = ()) -> any:
    main_params = func_make_main_params(*params)
    res = func_work(*main_params)
    return res

# замеры времени работы функции
def time_measurements(func_test, params, count_runs: int = DEF_TEST_COUNT_RUNS) -> float:
    calc_algo_time = process_time()
    for i in range(count_runs):
        func_test(*params)
    calc_algo_time = (process_time() - calc_algo_time) / count_runs
    return calc_algo_time

# вызов функции замеряющей времени работы алгоритма и отрисовка графика
def build_time_graph_one_algo(algo_test: Tuple[any], start_len_str: int = DEF_TEST_START_LEN_STR, final_len_str: int = DEF_TEST_FINAL_LEN_STR, step_len_str: int = DEF_TEST_STEP_LEN_STR) -> List[float]:
    x_arr, y_arr = [], []
    for size_str in range(start_len_str, final_len_str + 1, step_len_str):
        #print(size_str)
        res_time = time_measurements(run_func_make_params, (algo_test[0], generate_random_two_str, (size_str,)))
        res_time -= time_measurements(generate_random_two_str, (size_str,))
        x_arr.append(size_str)
        y_arr.append(res_time)
    # Строим график
    plt.plot(x_arr, y_arr, label = algo_test[-1], marker = '*')
    return y_arr

# вызов функции замеряющей времени работы алгоритмов и отрисовка графика
def build_time_graph_all_algo(algo_list: List[Tuple[any]], start_len_str: int = DEF_TEST_START_LEN_STR, final_len_str: int = DEF_TEST_FINAL_LEN_STR, step_len_str: int = DEF_TEST_STEP_LEN_STR) -> None:
    table = PrettyTable()
    table.field_names = ["алгоритм"] + [i for i in range(start_len_str, final_len_str + 1, step_len_str)]
    for ind in range(len(algo_list)):
        #print(algo_list[ind][-1])
        y_arr = build_time_graph_one_algo(algo_list[ind], start_len_str, final_len_str, step_len_str)
        table.add_row([algo_list[ind][-1]] + ["{:.2}".format(i) for i in y_arr])
        # Очищаем экран в командной строке
        print("\033[H\033[J")
        print(table)
    # Настройки и отображение графика
    plt.xlabel('Длина строки (сим)')
    plt.ylabel('Среднее время (сек)')
    plt.title('Замеры времени работы алгоритмов')
    plt.legend()
    plt.show()