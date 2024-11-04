import os
import matplotlib.pyplot as plt

# Словарь для перевода заголовков
translation_dict = {
    "Levenshtein algorithm (matrix implementation)": "Алгоритм Левенштейна\n(матричная реализация)",
    "Levenshtein algorithm (recursive implementation)": "Алгоритм Левенштейна\n(рекурсивная реализация)",
    "Levenshtein algorithm (recursive matrix implementation)": "Алгоритм Левенштейна\n(рекурсивно-матричная реализация)",
    "Damerau-Levenstein algorithm (matrix implementation)": "Алгоритм Дамерау-Левенштейна\n(матричная реализация)",
    "Damerau-Levenstein algorithm (recursive implementation)": "Алгоритм Дамерау-Левенштейна\n(рекурсивная реализация)",
    "Damerau-Levenshtein algorithm (recursively-matrix implementation)": "Алгоритм Дамерау-Левенштейна\n(рекурсивно-матричная реализация)"
}

# Функция для считывания и парсинга данных
def parse_data(file_path):
    algorithms_data = {}
    with open(file_path, 'r') as f:
        current_algorithm = ""
        for line in f:
            # Проверка строки с названием алгоритма
            if "Testing" in line:
                current_algorithm = line.strip().replace("Testing ", "").replace("...", "")
                algorithms_data[current_algorithm] = {"lengths": [], "times": []}
            elif "Len string" in line:
                parts = line.strip().split(', ')
                length = int(parts[0].split(': ')[1])
                time = float(parts[1].split(': ')[1].split()[0])
                algorithms_data[current_algorithm]["lengths"].append(length)
                algorithms_data[current_algorithm]["times"].append(time)
    return algorithms_data

# Функция для построения и сохранения графика
def plot_and_save_graph(algorithms_data, output_filename):
    plt.figure(figsize=(10, 6))
    # Список цветов для графиков
    colors = ['r', 'b', 'k', 'c', 'g', 'm']
    # Индекс для цветов
    color_index = 0
    for algo, data in algorithms_data.items():
        # Перевод названия алгоритма
        translated_algo = translation_dict[algo]
        plt.plot(data["lengths"], data["times"], label=translated_algo, color=colors[color_index], marker='o')
        # Переход к следующему цвету
        color_index = (color_index + 1) % len(colors)
    # Настройки графика
    plt.xlabel("Длина строки (сим)")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение времени работы алгоритмов")
    plt.legend()
    plt.grid(True)
    # Сохранение графика в файл
    plt.savefig(output_filename)
    plt.close()
    

# Папка с исходными файлами
input_folder = 'time_calc_data'

# Проход по всем файлам в папке
for filename in os.listdir(input_folder):
    if filename.endswith('.txt') and "err" not in filename:  # обрабатываем только текстовые файлы, не содержащие ошибок
        file_path = os.path.join(input_folder, filename)
        output_filename = input_folder + "/" + os.path.splitext(filename)[0] + '.png'  # меняем расширение на .png
        # Парсим данные из файла и строим график
        algorithms_data = parse_data(file_path)
        plot_and_save_graph(algorithms_data, output_filename)

print("Графики сохранены.")
