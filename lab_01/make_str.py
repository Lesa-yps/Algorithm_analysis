import random
import string
from typing import Tuple


# чтение 2 строк, введённых пользователем
# (True показывает, что пользователь ввёл строки сам -> надо ему вывести табличку в матричном способе)
def read_two_str() -> Tuple[str]:
    str1 = input("Введите первую строку: ")
    str2 = input("Введите вторую строку: ")
    return str1, str2, True

# генерация рандомной строки из алглийских букв заданной длины
def generate_random_str(size: int) -> str:
    # Создаем строку, содержащую все английские буквы (и строчные, и прописные)
    letters = string.ascii_letters
    # Генерируем случайную строку заданной длины
    random_str = ''.join(random.choice(letters) for _ in range(size))
    return random_str

# генерация двух рандомных строк из алглийских букв заданной длины
# (False показывает, что это сгенерированные строки -> не надо ему выводить табличку в матричном способе)
def generate_random_two_str(size: int) -> Tuple[str]:
    str1 = generate_random_str(size)
    str2 = generate_random_str(size)
    return str1, str2, False
