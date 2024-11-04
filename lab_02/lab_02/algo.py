from typing import List, Tuple

OK = True
ERROR = False

# стандартный алгоритм умножения матриц (строка на столбец)
def algo_matrix_mult_standard(A: List[List[int]], B: List[List[int]]) -> Tuple[List[List[int]], bool]:
    rows1, cols1 = len(A), len(A[0])
    rows2, cols2 = len(B), len(B[0])
    C = [[0 for _ in range(cols2)] for _ in range(rows1)]
    if (cols1 != rows2):
        err_code = ERROR
    else:
        for i in range(rows1):
            for j in range(cols2):
                C[i][j] = 0
                for k in range(cols1):
                    C[i][j] = C[i][j] + A[i][k] * B[k][j]
        err_code = OK
    return C, err_code

# алгоритм Винограда умножения матриц
def algo_matrix_mult_Vinograd(A: List[List[int]], B: List[List[int]]) -> Tuple[List[List[int]], bool]:
    rows1, cols1 = len(A), len(A[0])
    rows2, cols2 = len(B), len(B[0])
    C = [[0 for _ in range(cols2)] for _ in range(rows1)]
    if (cols1 != rows2):
        err_code = ERROR
    else:
        # заполнение массива MulH
        MulH = [0 for _ in range(rows1)]
        for i in range(rows1):
            for k in range(int(cols1 / 2)):
                MulH[i] = MulH[i] + A[i][2*k] * A[i][2*k+1]
        # заполнение массива MulV
        MulV = [0 for _ in range(cols2)]
        for j in range(cols2):
            for k in range(int(cols1 / 2)):
                MulV[j] = MulV[j] + B[2*k][j] * B[2*k+1][j]
        # само заполнение матрицы C
        for i in range(rows1):
            for j in range(cols2):
                C[i][j] = - MulH[i] - MulV[j]
                for k in range(int(cols1 / 2)):
                    C[i][j] = C[i][j] + (A[i][2*k] + B[2*k+1][j]) * (A[i][2*k+1] + B[2*k][j])
        # если cols1 нечётно (поправка)
        if cols1 % 2 == 1:
            for i in range(rows1):
                for j in range(cols2):
                    C[i][j] = C[i][j] +  A[i][cols1-1] * B[cols1-1][j]
        err_code = OK
    return C, err_code

# оптимизированный алгоритм Винограда умножения матриц (пока заглушка)
def algo_matrix_mult_Vinograd_better(A: List[List[int]], B: List[List[int]]) -> Tuple[List[List[int]], bool]:
    rows1, cols1 = len(A), len(A[0])
    rows2, cols2 = len(B), len(B[0])
    C = [[0 for _ in range(cols2)] for _ in range(rows1)]
    if (cols1 != rows2):
        err_code = ERROR
    else:
        max_k = int(cols1 / 2)
        # заполнение массива MulH
        MulH = [0 for _ in range(rows1)]
        for i in range(rows1):
            if max_k != 0:
                MulH[i] = A[i][0] * A[i][1]
            for k in range(1, max_k):
                MulH[i] = MulH[i] + A[i][k << 1] * A[i][(k << 1) + 1]
        # заполнение массива MulV
        MulV = [0 for _ in range(cols2)]
        for j in range(cols2):
            if max_k != 0:
                MulV[j] = B[0][j] * B[1][j]
            for k in range(1, max_k):
                MulV[j] = MulV[j] + B[k << 1][j] * B[(k << 1) + 1][j]
        # само заполнение матрицы C
        for i in range(rows1):
            for j in range(cols2):
                C[i][j] = - MulH[i] - MulV[j]
                if cols1 != 1:
                    C[i][j] = C[i][j] + (A[i][0] + B[1][j]) * (A[i][1] + B[0][j])
                # если cols1 нечётно (поправка)
                if cols1 % 2 == 1:
                    C[i][j] = C[i][j] +  A[i][cols1-1] * B[cols1-1][j]
                for k in range(1, max_k):
                    C[i][j] = C[i][j] + (A[i][k << 1] + B[(k << 1) + 1][j]) * (A[i][(k << 1) + 1] + B[k << 1][j])
        err_code = OK
    return C, err_code
    

algo_list = [(algo_matrix_mult_standard, "r", "Стандартный алгоритм"),
             (algo_matrix_mult_Vinograd, "g", "Алгоритм Винограда"),
             (algo_matrix_mult_Vinograd_better, "b", "Алгоритм Винограда\n(оптимизированный)")]


# Пример работы
if __name__ == "__main__":

    mat1 = [[1, 2],
            [3, 4]]

    mat2 = [[0, -1],
            [5, -2]]

    print(algo_matrix_mult_Vinograd(mat1, mat2))
    print(algo_matrix_mult_standard(mat1, mat2))
    print(algo_matrix_mult_Vinograd_better(mat1, mat2))