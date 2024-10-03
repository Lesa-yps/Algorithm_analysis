import random
from typing import Tuple, List
from prettytable import PrettyTable

class My_Error(Exception):
    pass

def check_array(arr_str: str) -> bool:
    arr = list(map(int, arr_str.strip().split()))
    return False

def check_num(x: str) -> bool:
    return not x.isdigit()

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

# чтение массива и х введённых пользователем
def read_arr_x() -> Tuple[any]:
    arr_str = input_check("Введите массив: ", check_array)
    arr = list(map(int, arr_str.strip().split()))
    x = int(input_check("Введите искомый элемент: ", check_num))
    return arr, x


# генерация рандомного числа
def generate_random_num(start, finish, step) -> int:
    # Создаем список возможных значений
    numbers = list(range(start, finish + 1, step))
    # Возвращаем случайное число из списка
    return random.choice(numbers)

# генерация рандомного массива целых чисел
def generate_random_arr(size: int, start, finish, step) -> List[int]:
    random_arr = [0 for _ in range(size)]
    for i in range(size):
        random_arr[i] = generate_random_num(start, finish, step)
    return random_arr

# генерация рандомных массива и х из целых чисел0
def generate_random_arr_x(size: int) -> Tuple[any]:
    arr = generate_random_arr(size, -1000, 1000, 2)
    x = generate_random_num(-9, 9, 2)
    ind = generate_random_num(-100, 100, 1)
    arr[ind] = x
    return arr, x