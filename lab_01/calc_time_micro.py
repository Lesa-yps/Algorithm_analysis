from time import ticks_ms, ticks_diff
import random

# Константы для тестирования
DEF_TEST_COUNT_RUNS = 20
DEF_TEST_START_LEN_STR = 5
DEF_TEST_FINAL_LEN_STR = 45
DEF_TEST_STEP_LEN_STR = 5



# алгоритм Левенштейна (матричная реализация, хранит всю матрицу)
def algo_Levenstein_matrix_old(str1: str, str2: str, output: bool = False) -> int:
    len1, len2 = len(str1) + 1, len(str2) + 1
    mat = [[(i * (j == 0) + j * (i == 0)) for i in range(len2)] for j in range(len1)]
    for i in range(1, len1):
        for j in range(1, len2):
            mat[i][j] = min(mat[i][j - 1] + 1,
                            mat[i - 1][j] + 1,
                            mat[i - 1][j - 1] + (str1[i - 1] != str2[j - 1]))
            #print(i, j, mat, mat[-1][-1])
    return mat[-1][-1]

# алгоритм Левенштейна (матричная реализация, хранит только текущую и предыдущую строки матрицы)
def algo_Levenstein_matrix(str1: str, str2: str, output: bool = False) -> int:
    len1, len2 = len(str1) + 1, len(str2) + 1
    if len2 > len1:
        str1, str2 = str2, str1
        len1, len2 = len2, len1
    old_str = [i for i in range(len2)]
    cur_str = [0 for _ in range(len2)]
    for i in range(1, len1):
        cur_str[0] = i
        for j in range(1, len2):
            cur_str[j] = min(cur_str[j - 1] + 1, # удаление (вес операции = 1)
                            old_str[j] + 1, # вставка (вес операции = 1)
                            old_str[j - 1] + (str1[i - 1] != str2[j - 1])) # замена (вес операции = 1)
        old_str = cur_str.copy()
    return cur_str[-1]

# алгоритм Левенштейна (рекурсивная реализация)
def algo_Levenstein_recursion(str1: str, str2: str, output: bool = False) -> int:
    len1, len2 = len(str1), len(str2)
    if len1 * len2 == 0:
        return abs(len2 - len1)
    return min(algo_Levenstein_recursion(str1, str2[:-1]) + 1,
                algo_Levenstein_recursion(str1[:-1], str2) + 1,
                algo_Levenstein_recursion(str1[:-1], str2[:-1]) + (str1[-1] != str2[-1]))

# алгоритм Левенштейна (рекурсивная реализация, при каждом вызове передаётся матрица)
def algo_Levenstein_recursion_matrix(str1: str, str2: str, output: bool = False) -> int:
    len1, len2 = len(str1) + 1, len(str2) + 1
    mat = [[float("-inf") for i in range(len2)] for j in range(len1)]
    # сама рекурсивная часть
    def recursion_part(str1: str, str2: str, mat = []) -> int:
        len1, len2 = len(str1), len(str2)
        if mat[len1][len2] > float("-inf"):
            pass
        elif len1 * len2 == 0:
            mat[len1][len2] = abs(len2 - len1)
        else:
            mat[len1][len2] = min(recursion_part(str1, str2[:-1], mat) + 1,
                    recursion_part(str1[:-1], str2, mat) + 1,
                    recursion_part(str1[:-1], str2[:-1], mat) + (str1[-1] != str2[-1]))
        return mat[len1][len2]
    return recursion_part(str1, str2, mat)


# алгоритм Дамерау-Левенштейна (матричная реализация)
def algo_Damerau_Levenstein_matrix(str1: str, str2: str, output: bool = False) -> int:
    len1, len2 = len(str1) + 1, len(str2) + 1
    if len2 > len1:
        str1, str2 = str2, str1
        len1, len2 = len2, len1
    old_str = [i for i in range(len2)]
    cur_str = [0 for _ in range(len2)]
    for i in range(1, len1):
        cur_str[0] = i
        for j in range(1, len2):
            m = str1[i - 1] != str2[j - 1]
            cur_str[j] = min(cur_str[j - 1] + 1, # удаление (вес операции = 1)
                            old_str[j] + 1, # вставка (вес операции = 1)
                            old_str[j - 1] + m) # замена (вес операции = 1)
            if (i > 1) and (j > 1) and m and (str1[i - 2] == str2[j - 1]) and (str1[i - 1] == str2[j - 2]):
                cur_str[j] = min(cur_str[j], old_str[j - 1])
        old_str = cur_str.copy()
    return cur_str[-1]

# алгоритм Дамерау-Левенштейна (рекурсивная реализация)
def algo_Damerau_Levenstein_recursion(str1: str, str2: str, output: bool = False) -> int:
    len1, len2 = len(str1), len(str2)
    if len1 * len2 == 0:
        return abs(len2 - len1)
    res = min(algo_Damerau_Levenstein_recursion(str1, str2[:-1]) + 1,
                algo_Damerau_Levenstein_recursion(str1[:-1], str2) + 1,
                algo_Damerau_Levenstein_recursion(str1[:-1], str2[:-1]) + (str1[-1] != str2[-1]))
    if ((len(str1) >= 2) and (len(str2) >= 2) and (str1[-1] == str2[-2]) and (str1[-2] == str2[-1])):
        res = min(res, algo_Damerau_Levenstein_recursion(str1[:-2], str2[:-2]) + 1)
    return res

# Алгоритм Дамерау-Левенштейна (рекурсивная реализация, при каждом вызове передаётся матрица)
def algo_Damerau_Levenstein_recursion_matrix(str1: str, str2: str, output: bool = False) -> int:
    len1, len2 = len(str1) + 1, len(str2) + 1
    mat = [[float("inf") for i in range(len2)] for j in range(len1)]
    # сама рекурсивная часть
    def recursion_part(str1: str, str2: str, mat = []) -> int:
        len1, len2 = len(str1), len(str2)
        if mat[len1][len2] < float("inf"):
            pass
        elif len1 * len2 == 0:
            mat[len1][len2] = abs(len2 - len1)
        else:
            mat[len1][len2] = min(recursion_part(str1, str2[:-1], mat) + 1,
                    recursion_part(str1[:-1], str2, mat) + 1,
                    recursion_part(str1[:-1], str2[:-1], mat) + (str1[-1] != str2[-1]))
            if ((len(str1) >= 2) and (len(str2) >= 2) and (str1[-1] == str2[-2]) and (str1[-2] == str2[-1])):
                mat[len1][len2] = min(mat[len1][len2], recursion_part(str1[:-2], str2[:-2], mat) + 1)
        return mat[len1][len2]
    return recursion_part(str1, str2, mat)
    

algo_list = [(algo_Levenstein_matrix, "Levenshtein algorithm (matrix implementation)"),
             (algo_Levenstein_recursion, "Levenshtein algorithm (recursive implementation)"),
             (algo_Levenstein_recursion_matrix, "Levenshtein algorithm (recursive matrix implementation)"),
             (algo_Damerau_Levenstein_matrix, "Damerau-Levenstein algorithm (matrix implementation)"),
             (algo_Damerau_Levenstein_recursion, "Damerau-Levenstein algorithm (recursive implementation)"),
             (algo_Damerau_Levenstein_recursion_matrix, "Damerau-Levenshtein algorithm (recursively-matrix implementation)")]



# Генерация двух случайных строк
def generate_random_two_str(length: int):
    letters = "abcdefghijklmnopqrstuvwxyz"
    str1 = ''.join(random.choice(letters) for _ in range(length))
    str2 = ''.join(random.choice(letters) for _ in range(length))
    return str1, str2

# Функция для замера времени работы другой функции
def time_measurements(func_test, params, count_runs: int = DEF_TEST_COUNT_RUNS) -> float:
    start_time = ticks_ms()
    for i in range(count_runs):
        func_test(*params)
    total_time = ticks_diff(ticks_ms(), start_time) / count_runs  # Среднее время
    return total_time / 1000  # Возвращаем в секундах

# Запуск переданной функции с параметрами
def run_func_make_params(func_work, func_make_main_params, params = ()) -> any:
    main_params = func_make_main_params(*params)
    res = func_work(*main_params)
    return res

# Строим текстовый график и замеряем время работы одного алгоритма
def build_time_graph_one_algo(algo_test, start_len_str: int = DEF_TEST_START_LEN_STR, final_len_str: int = DEF_TEST_FINAL_LEN_STR, step_len_str: int = DEF_TEST_STEP_LEN_STR):
    print(f"Testing {algo_test[1]}...")
    for size_str in range(start_len_str, final_len_str + 1, step_len_str):
        res_time = time_measurements(run_func_make_params, (algo_test[0], generate_random_two_str, (size_str,)))
        res_time -= time_measurements(generate_random_two_str, (size_str,))
        print(f"Len string: {size_str}, Time: {res_time:.4f} sec")

# Запуск тестирования нескольких алгоритмов
def build_time_graph_all_algo(algo_list, start_len_str: int = DEF_TEST_START_LEN_STR, final_len_str: int = DEF_TEST_FINAL_LEN_STR, step_len_str: int = DEF_TEST_STEP_LEN_STR):
    for algo_test in algo_list:
        build_time_graph_one_algo(algo_test, start_len_str, final_len_str, step_len_str)

# Пример алгоритма для теста (замените на ваши алгоритмы)
def dummy_algorithm(str1: str, str2: str):
    return str1 == str2  # Простой алгоритм для примера

# Основная программа
if __name__ == "__main__":
    # Запуск тестирования
    build_time_graph_all_algo(algo_list)
