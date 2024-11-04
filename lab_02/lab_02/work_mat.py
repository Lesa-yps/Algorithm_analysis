import random
from typing import Tuple, List
from prettytable import PrettyTable

class My_Error(Exception):
    pass

def check_array(arr_str: str, size: int) -> bool:
    arr = list(map(int, arr_str.strip().split()))
    return len(arr) != size

def check_size(x: str) -> bool:
    return not x.isdigit() or int(x) <= 0

# Функция для проверки ввода с помощью функции проверки
def input_check(input_str: str, check_func, params_check_funk = ()) -> any:
    while True:
        try:
            x = input(input_str)
            if check_func(x, *params_check_funk):
                raise My_Error  # вызов собственного исключения
            break           
        except Exception as exc:  # обработка всех исключений
            print("Ошибка ввода. Повторите попытку:")
    return x

# чтение матрицы, введённой пользователем
def read_mat(input_str: str) -> List[List[int]]:
    print(input_str)
    n = int(input_check("Введите количество строк: ", check_size))
    m = int(input_check("Введите количество столбцов: ", check_size))
    mat = list()
    print("Введите элементы матрицы по строкам:")
    for _ in range(n):
        arr_str = input_check("", check_array, (m,))
        arr = list(map(int, arr_str.strip().split()))
        mat.append(arr)
    return mat

# чтение 2 матриц, введённых пользователем
def read_two_mat() -> Tuple[List[List[int]]]:
    mat1 = read_mat("Введите первую матрицу:")
    mat2 = read_mat("Введите вторую матрицу:")
    return mat1, mat2


# генерация рандомной матрицы целых чисел от -10 до 10
def generate_random_mat(size: int) -> List[List[int]]:
    random_mat = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            random_mat[i][j] = random.randint(-10, 10)
    return random_mat

# генерация двух рандомных матриц из целых чисел от -10 до 10
def generate_random_two_mat(size: int) -> Tuple[str]:
    mat1 = generate_random_mat(size)
    mat2 = generate_random_mat(size)
    return mat1, mat2,


# красивый вывод матрицы
def output_mat(mat: List[List[int]]) -> None:
    table = PrettyTable()
    table.header = False
    table.hrules = True  # Включаем горизонтальные линии
    # Добавляем строки матрицы в таблицу
    for row in mat:
        table.add_row(row)
    print(table)
