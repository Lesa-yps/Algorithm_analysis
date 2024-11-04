import re
import matplotlib.pyplot as plt

FILE_MEASURE = "measure"

# проходится по файлу и вытаскивает из него данные
def parse_benchmark_results(filename):
    threads = []
    times = []
    with open(filename, 'r') as file:
        for line in file:
            # Ищем строки с информацией о времени выполнения
            match_main_thread = re.search(r'Запуск на основном потоке\s+Время выполнения: ([\d\.]+)', line)
            match_thread = re.search(r'Число потоков: (\d+)\s+Время выполнения: ([\d\.]+)', line)
            if match_main_thread:
                # Если это основная нить (без указания количества потоков)
                threads.append(0)  # Основной поток обозначаем как 0
                times.append(float(match_main_thread.group(1)))
            elif match_thread:
                # Если это строка с указанием количества потоков
                threads.append(int(match_thread.group(1)))
                times.append(float(match_thread.group(2)))
    return threads, times

# рисует график по данным из файла
def plot_benchmark_results(threads, times, output_file):
    plt.figure(figsize=(10, 6))
    plt.plot(threads, times, marker='o')
    plt.xlabel('Число потоков')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Зависимость времени выполнения от количества потоков')
    plt.grid(True)
    plt.xticks(threads)  # Устанавливаем тики на оси X соответствующими количеству потоков
    plt.savefig(output_file)  # Сохраняем график в файл
    print(f"График сохранён как {output_file}")

if __name__ == "__main__":
    filename = FILE_MEASURE + ".txt"
    threads, times = parse_benchmark_results(filename)
    plot_benchmark_results(threads, times, FILE_MEASURE + ".png")
