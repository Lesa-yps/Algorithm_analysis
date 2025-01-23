import sys
from Const import NORM_FILE_FORMAT, CSV_FILE_FORMAT, TEX_FILE_FORMAT, COUNT_GRAPH_TEST, DEF_DIR, PARAM_RES_DIR
from Run_algo import read_data_from_file
from Algo_full_search_paths import Algo_full_search_paths
from Algo_ant_search_paths import Algo_ant_search_paths


# формирование строки из коэффициентов и результатов алгоритмов для записи в файл
def format_res_str(full_min_path_len, ant_min_path_len, koefs, type_file):

    alpha, beta, koef_evap, days = koefs

    if (type_file == CSV_FILE_FORMAT):
        separ = ", "
        ender = ""
    elif (type_file == TEX_FILE_FORMAT):
        separ = " & "
        ender = " \\\\"
    else:
        separ = " | "
        ender = ""

    str_res = f"{alpha:6.2f}{separ}{beta:6.2f}{separ}{koef_evap:6.2f}{separ}{days:6d}{separ}{full_min_path_len:10.2f}{separ}{ant_min_path_len:10.2f}{separ}{ant_min_path_len - full_min_path_len:10.2f}{ender}\n"

    return str_res
    

# проход по диапазонам разных вариантов коэффициентов, запуск на них алгоритмов и запись в файл
def func_run_param(type_file = TEX_FILE_FORMAT):

    # диапазоны изменения коэффициентов
    alpha_arr = [i / 10 for i in range(1, 10)]
    koef_evap_arr = [i / 10 for i in range(1, 10)]
    days_arr = [1, 3, 5, 10, 30, 60, 100, 150, 200, 300]

    len_str_max_num = len(str(COUNT_GRAPH_TEST)) + 1

    print("Число тестов =", COUNT_GRAPH_TEST, "\nЗапуск:")
    print("№" + " " * (len_str_max_num - 1) + "-" * int(len(alpha_arr) * len(koef_evap_arr) * len(days_arr) / 10))

    for test_num in range(COUNT_GRAPH_TEST):

        print(test_num + 1, " " * ((len_str_max_num - 1 - len(str(test_num)))), end = "")
        sys.stdout.flush()

        filename_input_matrix = DEF_DIR + "/city_Rus_" + str(test_num + 1) + ".txt"
        filename_param_res = PARAM_RES_DIR + "/city_Rus_" + str(test_num + 1) + "." + type_file

        params = read_data_from_file(filename_input_matrix)

        full_min_path = Algo_full_search_paths(*params)

        file = open(filename_param_res, "w")

        count_test = 0

        for alpha in alpha_arr:
            beta = 1 - alpha

            for koef_evap in koef_evap_arr:

                for days in days_arr:
                    count_test += 1

                    koefs = alpha, beta, koef_evap, days

                    ant_full_min_path = Algo_ant_search_paths(*params, *koefs)

                    res_str = format_res_str(full_min_path[0], ant_full_min_path[0], koefs, type_file)

                    file.write(res_str)

                    if count_test % 10 == 0:
                        print(".", end = "")
                        sys.stdout.flush()

        file.close()

        print()
    
    print(" " * len_str_max_num + "-" * int(len(alpha_arr) * len(koef_evap_arr) * len(days_arr) / 10))