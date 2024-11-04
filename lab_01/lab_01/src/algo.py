from prettytable import PrettyTable
from typing import List


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
    if output:
        table = PrettyTable()
        table.header = False
        table.hrules = True  # Включаем горизонтальные линии
        table.add_row(["", ""] + [i for i in str2])
    old_str = [i for i in range(len2)]
    cur_str = [0 for _ in range(len2)]
    if output:
        table.add_row([""] + old_str)
    for i in range(1, len1):
        cur_str[0] = i
        for j in range(1, len2):
            cur_str[j] = min(cur_str[j - 1] + 1, # удаление (вес операции = 1)
                            old_str[j] + 1, # вставка (вес операции = 1)
                            old_str[j - 1] + (str1[i - 1] != str2[j - 1])) # замена (вес операции = 1)
        old_str = cur_str.copy()
        if output:
            table.add_row([str1[i - 1]] + cur_str)
    if output:
        print(table)
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
    def recursion_part(str1: str, str2: str, mat: List[float] = []) -> int:
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
    if output:
        table = PrettyTable()
        table.header = False
        table.hrules = True  # Включаем горизонтальные линии
        table.add_row(["", ""] + [i for i in str2])
    old_str = [i for i in range(len2)]
    cur_str = [0 for _ in range(len2)]
    if output:
        table.add_row([""] + old_str)
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
        if output:
            table.add_row([str1[i - 1]] + cur_str)
    if output:
        print(table)
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
    def recursion_part(str1: str, str2: str, mat: List[float] = []) -> int:
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
    

algo_list = [(algo_Levenstein_matrix, "r", "Алгоритм Левенштейна\n(матричная реализация)"),
             (algo_Levenstein_recursion, "g", "Алгоритм Левенштейна\n(рекурсивная реализация)"),
             (algo_Levenstein_recursion_matrix, "b", "Алгоритм Левенштейна\n(рекурсивно-матричная реализация)"),
             (algo_Damerau_Levenstein_matrix, "k", "Алгоритм Дамерау-Левенштейна\n(матричная реализация)"),
             (algo_Damerau_Levenstein_recursion, "m", "Алгоритм Дамерау-Левенштейна\n(рекурсивная реализация)"),
             (algo_Damerau_Levenstein_recursion_matrix, "c", "Алгоритм Дамерау-Левенштейна\n(рекурсивно-матричная реализация)")]