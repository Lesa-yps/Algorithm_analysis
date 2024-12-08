import os
from Const import DEF_FILENAME, DEF_DIR, SUMMER, WINTER
from Algo_full_search_paths import Algo_full_search_paths
from Algo_ant_search_paths import Algo_ant_search_paths

# чтение матрицы расстояний, направлений рек и текущего сезона из файла с разделителями "---"
def read_data_from_file(filename = DEF_FILENAME):
    matrix = []
    river_directions = []
    season = SUMMER
    # чтение и дробление на части файла
    with open(filename, "r") as file:
        sections = file.read().strip().split("---")
    # формирование матрицы расстояний
    matrix_lines = sections[0].strip().splitlines()
    for line in matrix_lines:
        row = [int(i) for i in line.split()]
        matrix.append(row)
    # формирование массива направлений рек
    river_lines = sections[1].strip().splitlines()
    for line in river_lines:
        river = tuple(map(int, line.split()))
        river_directions.append(river)
    # формирование флага сезона
    season = int(sections[2].strip())
    return matrix, river_directions, season
 
# чтение матрицы целых чисел из файла + запрос названия файла
def read_data_from_file_asc_filename(data_dir = DEF_DIR):
    print()
    try:
        # проверка существования папки
        if not os.path.exists(data_dir):
            print(f"Папка '{data_dir}' не найдена.")
            raise ValueError
        # получение списка файлов в папке
        files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
        if not files:
            print(f"В папке '{data_dir}' нет доступных файлов.")
            raise ValueError
        # отображение списка файлов с номерами
        print("Выберите файл из списка:")
        for idx, file in enumerate(files, start=1):
            print(f"{idx} - {file}")
        # пользователь выбирает номер файла из списка по номеру
        choice = int(input("Введите номер файла: ")) - 1
        if choice < 0 or choice >= len(files):
            print("Номер файла выходит за границы доступного диапазона.")
            raise ValueError
        filename = os.path.join(data_dir, files[choice])
    except ValueError:
        print("Ошибка ввода! Взят файл по-умолчанию.")
        filename = DEF_FILENAME
    print()
    # чтение данных из выбранного файла
    params = read_data_from_file(filename)
    return params

# чтение параметров для Муравьиного алгоритма
# alpha - параметр влияния длины пути
# beta - параметр влияния феромона
# koef_evap - коэффициент испарения феромона
# days - количество дней гуляния муравьёв
def read_ant_koeffs():
    print("\nВведите параметры для Муравьиного алгоритма.")
    try:
        alpha = float(input("Введите коэффициент влияния длины пути: " ))
        beta = 1 - alpha
        koef_evap = float(input("Введите коэффициент испарения феромона: " ))
        days = int(input("Введите количество дней: " ))
    except:
        print("Ошибка ввода! Взяты параметры по-умолчанию.")
        alpha, beta, koef_evap, days = 0, 1, 0.5, 10
    return alpha, beta, koef_evap, days

# запуск алгоритма поиска пути полным перебором с подготовительными действиями
def func_run_full_algo(params = None):
    if params is None:
        params = read_data_from_file_asc_filename()
    len_path, path = Algo_full_search_paths(*params)
    print(f"\nПолный перебор: кратчайший путь = {path} длиной = {len_path}.")

# запуск алгоритма поиска пути Муравьиным алгоритмом с подготовительными действиями
def func_run_ant_algo(params = None):
    if params is None:
        params = read_data_from_file_asc_filename()
    koeffs = read_ant_koeffs()
    len_path, path = Algo_ant_search_paths(*params, *koeffs)
    print(f"\nМуравьиный алгоритм: кратчайший путь = {path} длиной = {len_path}.")

# запуск обоих алгоритмов поиска пути с подготовительными действиями
def func_run_all_algos():
    params = read_data_from_file_asc_filename()
    func_run_ant_algo(params)
    func_run_full_algo(params)    