#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <ctype.h>
#include <string.h>
#include <fcntl.h> // Для открывания файлов
#include <sys/stat.h> // Для mkdir
#include <string.h>   // Для использования strstr и других функций

#define CPU_FREQUENCY_GHZ 2.6 // частота процессора
#define CPU_COUT_LOGIC_CORE 16 // количество логических ядер
#define MAX_PAGES 1000 // Максимальное количество страниц для выгрузки
#define MAX_URL_LENGTH 256 // Максимальная длина URL
#define COUNT_RUN 5 // Число запусков
#define FILE_LINKS "links.txt" // имя файла со ссылками
#define FILE_MEASURE "measure.txt" // имя файла для вывода замеров

// Ошибки
#define ERR_READ_FILE_LINKS 1
#define OK 0

char** urls; // Глобальная переменная для хранения списка URL из файла
int url_count; // Глобальная переменная для общего количества URL

int current_page_index = 0; // Текущий индекс для обработки URL (чтоб контролировать, что потоки не обрабатывают одну страницу)
pthread_mutex_t mutex; // мьютекс для одиночного доступа к переменной current_page_index

typedef struct
{
    char* url;
    int thread_id;
} ThreadData;

// Функция для получения текущего значения тактов процессора
static inline uint64_t rdtsc(void)
{
    unsigned int lo, hi;
    __asm__ volatile("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}

// читает ссылки из файла
char** read_links_from_file(const char* filename)
{
    // открытие файла и проверка успешности открытия
    FILE *file = fopen(filename, "r");
    if (! file)
    {
        perror("Не удалось открыть файл");
        return NULL;
    }
    // выделение памяти и зануление начального числа урлов
    char **urls = malloc(MAX_PAGES * sizeof(char*));
    char buffer[MAX_URL_LENGTH];
    url_count = 0;
    // считываем строки из файла и записываем в массив урлов, при этом выделяя память
    while (fgets(buffer, sizeof(buffer), file) != NULL && url_count < MAX_PAGES)
    {
        // Удаляем символ новой строки
        buffer[strcspn(buffer, "\n")] = 0;
        urls[url_count] = malloc(strlen(buffer) + 1);
        strcpy(urls[url_count], buffer);
        url_count++;
    }
    // закрываем файл и возвращаем урлы
    fclose(file);
    return urls;
}

// Функция для генерации имени файла из URL
void generate_filename_from_url(const char* url, char* filename, size_t size)
{
    // Убираем протокол из URL (http:// или https://)
    const char* start = strstr(url, "://");
    if (start)
        start += 3; // Пропускаем "://"
    else
        start = url; // Если протокол не найден, используем весь URL

    // Заменяем недопустимые символы на '_'
    size_t i = 0;
    for (const char* p = start; *p != '\0' && i < (size - 1); p++)
        if (*p == '/' || *p == ':' || *p == '?' || *p == '&' || *p == '=')
            filename[i++] = '_'; // Заменяем на '_'
        else
            filename[i++] = *p; // Оставляем текущий символ
    filename[i] = '\0'; // Завершаем строку
}

// Функция для записи данных напрямую в файл
size_t WriteDataToFile(void *contents, size_t size, size_t nmemb, FILE *file)
{
    size_t written = fwrite(contents, size, nmemb, file);
    return written;
}

// Функция для загрузки страницы и записи в файл
void* download_page(void* arg)
{
    ThreadData* data = (ThreadData*) arg;

    // Создаем папку "data", если она не существует
    mkdir("data", 0777); // Игнорируем ошибку, если директория уже существует

    // Генерируем имя файла на основе URL для хранения содержимого страницы
    char filename[256];
    generate_filename_from_url(data->url, filename, sizeof(filename));

    // Создаем полный путь к файлу, в который будет сохранена страница
    char filepath[300];
    snprintf(filepath, sizeof(filepath), "data/%s.html", filename); // Папка "data" + сгенерированное имя файла

    // Формируем команду для вызова системного curl
    char curl_command[1024];
    snprintf(curl_command, sizeof(curl_command),
             "curl -s -A 'Mozilla/5.0' -o '%s' '%s'", filepath, data->url);

    // Выполняем команду curl для загрузки страницы
    int result = system(curl_command);
    if (result != 0) {
        fprintf(stderr, "curl command failed for URL: %s\n", data->url);
        return NULL;
    }

    if (DEBUG)
    {
        char filename[50];
        snprintf(filename, sizeof(filename), "debug/%d.txt", data->thread_id);
        FILE *file = fopen(filename, "a");
        if (file != NULL)
        {
            fprintf(file, "Поток %d загрузил страницу: %s и сохранил в %s.\n", data->thread_id, data->url, filepath);
            fclose(file);
        }
        else
            fprintf(stderr, "Ошибка открытия файла %s для дозаписи потоком %d.\n", filename, data->thread_id);
    }  

    return NULL;
}

// Функция, которую выполняет поток
void* thread_function(void* arg)
{
    int thread_id = *((int*)arg);
    ThreadData data;
    // цикл проходится по всем урлам
    while (1)
    {
        // Защита доступа к общему индексу
        pthread_mutex_lock(&mutex);
        // Завершение, если все URL обработаны
        if (current_page_index >= url_count)
        {
            pthread_mutex_unlock(&mutex);
            break;
        }
        // Получаем URL для обработки
        data.url = urls[current_page_index];
        data.thread_id = thread_id;
        current_page_index++; // Увеличиваем индекс для следующего потока
        pthread_mutex_unlock(&mutex); // Освобождаем мьютекс
        // Обработка URL (сама работа потока)
        download_page((void*) &data);
    }
    return NULL;
}

// Функция для замеров тактов процессора и перевода в секунды (запуск на главном потоке)
double measure_execution_time_main_threat(int print_time)
{
    ThreadData data;
    // запуск подсчёта тиков процессора
    uint64_t start_ticks = rdtsc();
    // Пробегаем по всем URL и загружаем страницы на основном потоке
    for (int i = 0; i < url_count; i++) {
        data.url = urls[i]; // Получаем текущий URL
        data.thread_id = -1; // Для основного потока можно использовать thread_id = -1
        download_page((void*) &data); // Загружаем страницу
    }
    // завершение подсчёта тиков процессора
    uint64_t end_ticks = rdtsc();
    if (print_time)
        printf("Все страницы загружены на основном потоке.\n");
    // рассчитываем и возвращаем время
    uint64_t elapsed_ticks = end_ticks - start_ticks;
    if (DEBUG)
        printf("Затраченные такты : %llu\n", (unsigned long long)elapsed_ticks);
    double elapsed_time_sec = (double)elapsed_ticks / (CPU_FREQUENCY_GHZ * 1e6) / 1000.0;
    if (print_time)
        printf("Время выполнения: %.6f сек\n", elapsed_time_sec);
    current_page_index = 0;
    return elapsed_time_sec;
}

// Функция для замеров тактов процессора и перевода в секунды (запуск на переданном числе доп-потоков)
double measure_execution_time(int num_threads, int print_time)
{
    pthread_t threads[num_threads]; // Массив самих потоков
    int thread_id[MAX_PAGES]; // Массив для хранения идентификаторов потоков
    // Инициализация мьютекса
    pthread_mutex_init(&mutex, NULL);
    // запуск подсчёта тиков процессора
    uint64_t start_ticks = rdtsc();
    // Запуск потоков
    for (int i = 0; i < num_threads; i++)
    {
        thread_id[i] = i; // Присваиваем идентификатор потока
        pthread_create(&threads[i], NULL, thread_function, (void*)&thread_id[i]); // запуск потока
    }
    // Ждем завершения потоков
    for (int i = 0; i < num_threads; i++)
        pthread_join(threads[i], NULL);
    // завершение подсчёта тиков процессора
    uint64_t end_ticks = rdtsc();
     // Освобождаем ресурсы мьютекса
    pthread_mutex_destroy(&mutex);
    // рассчитываем и возвращаем время
    uint64_t elapsed_ticks = end_ticks - start_ticks;
    if (DEBUG)
        printf("Затраченные такты для %d потоков: %llu\n", num_threads, (unsigned long long)elapsed_ticks);
    double elapsed_time_sec = (double)elapsed_ticks / (CPU_FREQUENCY_GHZ * 1e6) / 1000.0;
    if (print_time)
        printf("Время выполнения: %.6f сек\n", elapsed_time_sec);
    current_page_index = 0;
    return elapsed_time_sec;
}

// Проверка корректности ввода целого числа в заданном диапазоне
int input_int_with_validation(int min_value, int max_value)
{
    int choice; 
    char input[10];
    int is_correct = 0;
    while (! is_correct)
    {
        fgets(input, sizeof(input), stdin);
        if (sscanf(input, "%d", &choice) != 1 || choice < min_value || choice > max_value)
            printf("Неверный ввод. Введите число от %d до %d: ", min_value, max_value);
        else
            is_correct = 1;
    }
    return choice;
}

// Функция, проводящая замеры времени на нескольких потоках (разное количество) и на основном и выводящая результаты в файл
void measurements(char* filename)
{
    FILE* file = fopen(filename, "w");
    fprintf(file, "Проведение замеров (число логических ядер = %d, число ссылок = %d):\n", CPU_COUT_LOGIC_CORE, url_count);
    int num_threads = 1; // число потоков
    for (int i = -1; num_threads <= 4 * CPU_COUT_LOGIC_CORE && num_threads <= url_count; i++)
    {
        double sum_time = 0;
        // запуск на основном потоке
        if (i == -1)
        {
            fprintf(file, "Запуск на основном потоке         ");
            for (int j = 0; j < COUNT_RUN; j++)
                sum_time += measure_execution_time_main_threat(0);
        }
        else // запуск на разном числе доп-потоков
        {
            fprintf(file, "Число потоков: %d                 ", num_threads);
            for (int j = 0; j < COUNT_RUN; j++)
                sum_time += measure_execution_time(num_threads, 0);
            num_threads *= 2;
        }
        fprintf(file, "Время выполнения: %.6f сек\n", sum_time / COUNT_RUN);
    }
    fclose(file);
}

// главная функция
int main(void)
{
    int choice = 0; // выбранный пользователем пункт меню
    int num_threads; // число потоков
    // Считываем URL из файла
    urls = read_links_from_file(FILE_LINKS);
    // Завершаем, если чтение не удалось
    if (! urls)
        return ERR_READ_FILE_LINKS;
    // бесконечный цикл с меню
    while (choice != 4)
    {
        printf("\nМеню:\n"
               "1) Запустить на основном потоке\n"
               "2) Запустить на нескольких потоках\n"
               "3) Провести замеры\n"
               "4) Выход\n"
               "Выберите действие (1-4): ");
        choice = input_int_with_validation(1, 4);
        switch (choice)
        {
            case 1:
                if (url_count > 0)
                {
                    printf("\nЗапуск на основном потоке:\n");
                    measure_execution_time_main_threat(1);
                }
                else
                    printf("Нет доступных URL для обработки.\n");
                break;

            case 2:
                printf("\nВведите количество потоков (максимум %d): ", url_count);
                num_threads = input_int_with_validation(1, url_count);
                printf("\nЗапуск на %d потоках:\n", num_threads);
                measure_execution_time(num_threads, 1);
                break;

            case 3:
                printf("\nПроведение замеров (число логических ядер = %d, число ссылок = %d)...\n\n", CPU_COUT_LOGIC_CORE, url_count);
                measurements(FILE_MEASURE);
                break;

            case 4:
                printf("Выход из программы.\n");
                break;

            default:
                printf("Неверная пункт меню. Попробуйте снова.\n");
        }
    }

    // Освобождаем память из-под списка урлов
    for (int i = 0; i < url_count; i++)
        free(urls[i]);
    free(urls);

    return OK;
}
