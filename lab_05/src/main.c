#include <pthread.h>
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <ctype.h>
#include <string.h>
#include <fcntl.h>    // для открытия файлов
#include <sys/stat.h> // для mkdir
#include <string.h>
#include <libpq-fe.h> // для работы с PostgreSQL
#include <unistd.h>

#include "lib_list.h"
#include "work_db.h"

#define MAX_LINE_LENGTH 1000
#define BUF_SIZE 512
#define INPUT_DATA_DIR "data"

// общее количество задач
int task_count = 0;
// сколько каждый поток обработал заявок
int task_count0 = 0, task_count1 = 0, task_count2 = 0, task_count3 = 0, task_count4 = 0;              
node_t *Queue1 = NULL, *Queue2 = NULL, *Queue3 = NULL, *Queue4 = NULL; // 4 очереди-списка заявок
pthread_mutex_t mutex_queue1, mutex_queue2, mutex_queue3, mutex_queue4; // мьютексы для очередей

// функция для получения текущего значения тактов процессора
static inline uint64_t rdtsc(void)
{
    unsigned int lo, hi;
    __asm__ volatile("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}

// освобождение памяти из-под задачи
void free_mem_task(TaskDataTime *task)
{
    free(task->task_data.filename);
    free(task->task_data.url);
    free(task->task_data.title);
    for (int i = 0; i < task->task_data.ingredient_count; i++)
    {
        free(task->task_data.ingredients[i].name);
        free(task->task_data.ingredients[i].count);
    }
    for (int i = 0; i < task->task_data.step_count; i++)
        free(task->task_data.steps[i]);
    free(task->task_data.image_url);
}

// функция инициализирует новую заявку TaskDataTime (сам файл не читает)
TaskDataTime *initialize_task(const char *filename)
{
    // попытка выделить память под новую заявку
    TaskDataTime *task = malloc(sizeof(TaskDataTime));
    if (task == NULL)
    {
        perror("Ошибка выделения памяти для заявки");
        return NULL;
    }
    // инициализируются данные заявки
    task->task_data.id = task_count0;
    task->task_data.filename = strdup(filename);
    if (task->task_data.filename == NULL)
    {
        perror("Ошибка выделения памяти для имени файла при создании заявки");
        free(task);
        return NULL;
    }
    // Стартовая инициализация массивов
    task->task_data.ingredients = malloc(50 * sizeof(Ingredient));
    task->task_data.steps = malloc(50 * sizeof(char *));
    task->task_data.ingredient_count = 0;
    task->task_data.step_count = 0;
    task->task_data.issue_id = ISSUE_ID;
    task->task_data.url = NULL;
    task->task_data.title = NULL;
    task->task_data.image_url = NULL;
    memset(task->time_data, 0, sizeof(task->time_data));
    return task;
}

// функция, которую выполняет поток №0 (готовит заявки к обработке)
// генерирует заявки с именами файлов из папки data и записывает их в очередь Queue1
void *thread_function_prepare_data(void *arg)
{
    DIR *dir;
    struct dirent *entry;

    // пытаемся открыть папку data
    if ((dir = opendir(INPUT_DATA_DIR)) == NULL)
    {
        perror("Ошибка при открытии папки " INPUT_DATA_DIR);
        return NULL;
    }

    // проходимся по всем файлам в папке data
    while ((entry = readdir(dir)) != NULL && task_count0 < task_count)
    {
        // игнорируются специальные файлы . и ..
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;

        // буфер для полного пути
        char full_path[BUF_SIZE];
        snprintf(full_path, sizeof(full_path), "%s/%s", INPUT_DATA_DIR, entry->d_name);

        // создание новой задачи
        TaskDataTime *task = initialize_task(full_path);
        if (task == NULL)
        {
            closedir(dir);
            return NULL;
        }

        // защита доступа к очереди 1
        pthread_mutex_lock(&mutex_queue1);
        // кладём элемент в 1 очередь
        put_elem(&Queue1, *task);
        // освобождение мьютекса первой очереди
        pthread_mutex_unlock(&mutex_queue1);
        task_count0 ++;
    }

    closedir(dir);
    return NULL;
}

// функция, которую выполняет поток №1 (чтение данных из файла)
void *thread_function_read_file(void *arg)
{
    setbuf(stdout, NULL);
    TaskDataTime task;
    while (task_count1 < task_count)
    {
        // берём элемент из первой очереди
        // защита доступа к очереди 1
        pthread_mutex_lock(&mutex_queue1);
        // пытаемся получить задачу из очрееди
        if (get_elem(&Queue1, &task) == OK)
        {
            // освобождаем мьютекс первой очереди
            pthread_mutex_unlock(&mutex_queue1);
            // фиксируем время в тиках
            task.time_data[0] = rdtsc();
            // читаем данные (основная работа потока)
            // ------------------------------------
            // открытие файла
            FILE *file = fopen(task.task_data.filename, "r");
            if (file == NULL)
            {
                perror("Ошибка открытия файла рецепта");
                continue;
            }
            char line[MAX_LINE_LENGTH];
            // парсинг HTML файла
            while (fgets(line, MAX_LINE_LENGTH, file))
            {
                // достаём title из HTML
                if (strstr(line, "<title>"))
                {
                    char *start = strstr(line, "<title>") + strlen("<title>");
                    char *end = strstr(start, "</title>");
                    if (start && end)
                    {
                        size_t length = end - start;
                        task.task_data.title = malloc(length + 1);
                        if (task.task_data.title)
                        {
                            strncpy(task.task_data.title, start, length);
                            task.task_data.title[length] = '\0';
                        } else
                            perror("Ошибка выделения памяти для title");
                    }
                }
                // достаём URL
                else if (strstr(line, "<meta property=\"og:url\""))
                {
                    char *start = strstr(line, "content=\"") + strlen("content=\"");
                    char *end = strstr(start, "\"");
                    if (start && end && end > start)
                    {
                        size_t length = end - start;
                        task.task_data.url = malloc(length + 1);
                        if (task.task_data.url)
                        {
                            strncpy(task.task_data.url, start, length);
                            task.task_data.url[length] = '\0';
                        } else
                            perror("Ошибка выделения памяти для url");
                    }
                }
                // достаём URL изображения
                else if (strstr(line, "<meta property=\"og:image\""))
                {
                    char *start = strstr(line, "content=\"") + strlen("content=\"");
                    char *end = strstr(start, "\"");
                    if (start && end && end > start)
                    {
                        size_t length = end - start;
                        task.task_data.image_url = malloc(length + 1);
                        if (task.task_data.image_url)
                        {
                            strncpy(task.task_data.image_url, start, length);
                            task.task_data.image_url[length] = '\0';
                        } else
                            perror("Ошибка выделения памяти для image_url");
                    }
                }
                // достаём текст ингредиента 
                else if (strstr(line, "itemprop=\"recipeIngredient\""))
                {
                    // название ингредиента
                    char *name_start = strstr(line, "-left:5px;\">") + strlen("-left:5px;\">");
                    char *name_end = strstr(name_start, "<");
                    if (name_start && name_end && name_end > name_start)
                    {
                        size_t name_length = name_end - name_start;
                        task.task_data.ingredients[task.task_data.ingredient_count].name = malloc(name_length + 1);
                        strncpy(task.task_data.ingredients[task.task_data.ingredient_count].name, name_start, name_length);
                        task.task_data.ingredients[task.task_data.ingredient_count].name[name_length] = '\0';
                    }

                    // количество и единица измерения ингредиента
                    char *qty_start = strstr(line, "float:right");
                    if (qty_start)
                    {
                        qty_start = strstr(qty_start, ">") + 1;
                        char *qty_end = strstr(qty_start, "<");
                        if (qty_start && qty_end && qty_end > qty_start)
                        {
                            size_t qty_length = qty_end - qty_start;
                            task.task_data.ingredients[task.task_data.ingredient_count].count = malloc(qty_length + 1);
                            strncpy(task.task_data.ingredients[task.task_data.ingredient_count].count, qty_start, qty_length);
                            task.task_data.ingredients[task.task_data.ingredient_count].count[qty_length] = '\0';
                        }
                    }
                    // количество ингредиентов
                    task.task_data.ingredient_count++;
                }
                // достаём шаги приготовления
                else if (strstr(line, "itemprop=\"recipeInstructions\""))
                {
                    char *start = strstr(line, "alt=\"");
                    if (! start)
                        continue;
                    start += strlen("alt=\"");
                    char *end = strstr(start, "\"");
                    if (start && end && end > start)
                    {
                        size_t length = end - start;
                        task.task_data.steps[task.task_data.step_count] = malloc(length + 1);
                        if (task.task_data.steps[task.task_data.step_count])
                        {
                            strncpy(task.task_data.steps[task.task_data.step_count], start, length);
                            task.task_data.steps[task.task_data.step_count][length] = '\0';
                            task.task_data.step_count++;
                        } else
                            perror("Ошибка выделения памяти для step");
                    }
                }
            }
            fclose(file);
            // ------------------------------------
            // фиксируем время в тиках
            task.time_data[1] = rdtsc();
            task_count1++;
            // кладём элемент во 2 очередь
            // защита доступа к очереди 2
            pthread_mutex_lock(&mutex_queue2);
            put_elem(&Queue2, task);
            // освобождаем мьютекс второй очереди
            pthread_mutex_unlock(&mutex_queue2);
        }
        else
            // освобождаем мьютекс первой очереди
            pthread_mutex_unlock(&mutex_queue1);
    }
    return NULL;
}

// функция очищает текст от HTML и лишних символов
void clean_text(char *text) {
    // проверка на NULL или пустую строку
    if (text == NULL || *text == '\0')
        return;
    char *write_ptr = text;
    for (char *read_ptr = text; *read_ptr; read_ptr++)
    {
        // пропуск символов внутри HTML тегов
        if (*read_ptr == '<')
        {
            while (*read_ptr && *read_ptr != '>')
                read_ptr++;
        } else
            *write_ptr++ = *read_ptr;
    }
    *write_ptr = '\0';
    // если строка пустая или состоит только из пробелов, то заменяем на "-"
    char *check_ptr = text;
    while (*check_ptr)
    {
        if (!isspace((unsigned char)*check_ptr))
            return;
        check_ptr++;
    }
    strcpy(text, "-");
}

// функция, которую выполняет поток №2 (извлечение необходимого подмножества данных)
void *thread_function_extract_data(void *arg)
{
    TaskDataTime task;
    while (task_count2 < task_count)
    {
        // берём элемент из 2 очереди
        // защита доступа к очереди 2
        pthread_mutex_lock(&mutex_queue2);
        // пытаемся получить задачу из очереди
        if (get_elem(&Queue2, &task) == OK)
        {
            // освобождаем мьютекс второй очереди
            pthread_mutex_unlock(&mutex_queue2);
            // фиксируем время в тиках
            task.time_data[2] = rdtsc();
            // очистка необходимого подмножества данных от HTML и лишних символов (основная работа потока)
            // ------------------------------------
            // очистка текста от HTML и лишних символов
            clean_text(task.task_data.title);
            for (int i = 0; i < task.task_data.ingredient_count; i++)
            {
                clean_text(task.task_data.ingredients[i].name);
                clean_text(task.task_data.ingredients[i].count);
            }
            for (int i = 0; i < task.task_data.step_count; i++)
            {
                clean_text(task.task_data.steps[i]);
            }
            // ------------------------------------
            // фиксируем время в тиках
            task.time_data[3] = rdtsc();
            task_count2++;
            // кладём элемент в 3 очередь
            // защита доступа к очереди 3
            pthread_mutex_lock(&mutex_queue3);
            put_elem(&Queue3, task);
            // освобождаем мьютекс третьей очереди
            pthread_mutex_unlock(&mutex_queue3);
        }
        else
            // освобождаем мьютекс второй очереди
            pthread_mutex_unlock(&mutex_queue2);
    }
    return NULL;
}

// функция, которую выполняет поток №3 (запись извлеченных данных в хранилище PostgreSQL)
void *thread_function_write_data_DB(void *arg)
{
    TaskDataTime task;
    PGconn *conn;
    const char *query;
    // (при необходимости) создаём БД и таблицы
    if (init_db() == ERROR)
        return NULL;
    // подключаемся к PostgreSQL
    conn = PQconnectdb("user=olesya dbname=db_recipes password=280904");
    if (PQstatus(conn) != CONNECTION_OK)
    {
        fprintf(stderr, "Ошибка подключения к БД: %s", PQerrorMessage(conn));
        PQfinish(conn);
        return NULL;
    }
    //FILE *file = fopen("log_file.txt", "w");
    while (task_count3 < task_count)
    {
        // берём элемент из 3 очереди
        // защита доступа к очереди 3
        pthread_mutex_lock(&mutex_queue3);
        // пытаемся получить задачу из очереди 3
        if (get_elem(&Queue3, &task) == OK)
        {
            // освобождаем мьютекс очереди 3
            pthread_mutex_unlock(&mutex_queue3);
            // фиксируем время в тиках
            task.time_data[4] = rdtsc();
            // запись 1 задачи в таблицы (основная работа потока)
            // ------------------------------------
            if (put_task_to_table(conn, &task) == ERROR)
                break;
            // ------------------------------------
            // фиксируем время в тиках
            task.time_data[5] = rdtsc();
            task_count3++;
            // кладём элемент в 4 очередь
            // защита доступа к очереди 4n
            pthread_mutex_lock(&mutex_queue4);
            put_elem(&Queue4, task);
            // освобождаем мьютекс очереди 4
            pthread_mutex_unlock(&mutex_queue4);
        }
        else
            // освобождаем мьютекс очереди 3
            pthread_mutex_unlock(&mutex_queue3);
    }
    PQfinish(conn);
    return NULL;
}

// функция сравнения для сортировки
int comparator(const uint64_t *a, const uint64_t *b)
{
    return (*a > *b) - (*a < *b);
}

// функция вычисляет времена tmin_ms, tmax_ms, tavg_ms, tmed_ms
void calc_print_time_res(TimeStatisticData time_stat, FILE *file, const char *help_str)
{
    uint64_t tsum = 0;
    time_stat.tmin = UINT64_MAX;
    time_stat.tmax = 0;
    // поиск tmin, tmax, и tsum
    for (int i = 0; i < task_count; i++)
    {
        uint64_t value = time_stat.arr[i];
        if (value < time_stat.tmin)
            time_stat.tmin = value;
        if (value > time_stat.tmax)
            time_stat.tmax = value;
        tsum += value;
    }
    time_stat.tavg = tsum / task_count;
    // сортируем массив и ищем tmed
    qsort(time_stat.arr, task_count, sizeof(uint64_t), (int (*)(const void *, const void *))comparator);
    if (task_count % 2 == 0)
        time_stat.tmed = (time_stat.arr[task_count / 2 - 1] + time_stat.arr[task_count / 2]) / 2;
    else
        time_stat.tmed = time_stat.arr[task_count / 2];
    // такты -> миллисекунды
    double tmin_ms = (double)time_stat.tmin / CPU_FREQUENCY_HZ * 1000;
    double tmax_ms = (double)time_stat.tmax / CPU_FREQUENCY_HZ * 1000;
    double tavg_ms = (double)time_stat.tavg / CPU_FREQUENCY_HZ * 1000;
    double tmed_ms = (double)time_stat.tmed / CPU_FREQUENCY_HZ * 1000;
    // запись результата в файл в миллисекундах
    fprintf(file, "%s   tмин = %.6f мс, tмакс = %.6f мс, tсред = %.6f мс, tмед = %.6f мс\n\n",
            help_str, tmin_ms, tmax_ms, tavg_ms, tmed_ms);
}

// функция, которую выполняет поток №4 (обрабатывает (и очищает) итоговую очередь, обрабатывая замеры времени и выводя результаты в файл measure.txt)
void *thread_function_calc_time(void *arg)
{
    setbuf(stdout, NULL);
    TimeStatisticData tw1, tw2, tw3, tq2, tq3;
    tw1.arr = malloc(task_count * sizeof(uint64_t));
    tw2.arr = malloc(task_count * sizeof(uint64_t));
    tw3.arr = malloc(task_count * sizeof(uint64_t));
    tq2.arr = malloc(task_count * sizeof(uint64_t));
    tq3.arr = malloc(task_count * sizeof(uint64_t));
    FILE *file = fopen("measure.txt", "w");
    if (file == NULL)
    {
        perror("Ошибка открытия файла measure.txt");
        return NULL;
    }
    TaskDataTime task;
    while (task_count4 < task_count)
    {
        // защита доступа к очереди 4
        pthread_mutex_lock(&mutex_queue4);
        // вычисление массивов времён для последующей обработки (в тиках)
        if (get_elem(&Queue4, &task) == OK)
        {
            // освобождаем мьютекс очереди 4
            pthread_mutex_unlock(&mutex_queue4);
            // вычисляется {tmin, tmax, tavg, tmed}
            // 1) затраченное i-м обрабатывающим устройством на обработку одной заявки
            tw1.arr[task_count4] = task.time_data[1] - task.time_data[0];
            tw2.arr[task_count4] = task.time_data[3] - task.time_data[2];
            tw3.arr[task_count4] = task.time_data[5] - task.time_data[4];
            // 2) время проведённое заявкой в очередях 2 и 3
            tq2.arr[task_count4] = task.time_data[2] - task.time_data[1];
            tq3.arr[task_count4] = task.time_data[4] - task.time_data[3];
            task_count4 ++;
            // освобождение памяти из-под задачи
            free_mem_task(&task);
        }
        else
        {
            // освобождаем мьютекс очереди 4
            pthread_mutex_unlock(&mutex_queue4);
            sleep(1);
        }
    }
    // вычисление искомых значений и запись в файл
    calc_print_time_res(tw1, file, "Устройство №1\n");
    calc_print_time_res(tw2, file, "Устройство №2\n");
    calc_print_time_res(tw3, file, "Устройство №3\n");
    calc_print_time_res(tq2, file, "Очередь №2\n");
    calc_print_time_res(tq3, file, "Очередь №3\n");
    // осводождение памяти
    free(tw1.arr);
    free(tw2.arr);
    free(tw3.arr);
    free(tq2.arr);
    free(tq3.arr);
    fclose(file);
    return NULL;
}


// считает сколько файлов в папке
int count_files_in_directory(const char *dir_path)
{
    int file_count = 0;
    struct dirent *entry;
    struct stat file_stat;
    DIR *dir = opendir(dir_path);
    if (dir == NULL)
    {
        perror("Ошибка открытия папки");
        return -1;
    }
    while ((entry = readdir(dir)) != NULL)
    {
        // пропускаем "." и ".."
        if (entry->d_name[0] == '.' && (entry->d_name[1] == '\0' || (entry->d_name[1] == '.' && entry->d_name[2] == '\0')))
            continue;
        // путь к файлу = путь к директории / имя файла
        char full_path[BUF_SIZE];
        snprintf(full_path, sizeof(full_path), "%s/%s", dir_path, entry->d_name);
        // проверка: является ли элемент файлом?
        if (stat(full_path, &file_stat) == 0 && S_ISREG(file_stat.st_mode))
            file_count++;
    }
    closedir(dir);
    return file_count;
}


// главная функция
int main(void)
{
    pthread_t thread0, thread1, thread2, thread3, thread4;

    // считает сколько файлов в папке
    task_count = count_files_in_directory(INPUT_DATA_DIR);
    if (task_count < 0)
        return ERROR;

    // инициализация мьютексов
    pthread_mutex_init(&mutex_queue1, NULL);
    pthread_mutex_init(&mutex_queue2, NULL);
    pthread_mutex_init(&mutex_queue3, NULL);
    pthread_mutex_init(&mutex_queue4, NULL);


    // создаём потоки

    // создание заявок и помещение их в очередь №1
    pthread_create(&thread0, NULL, thread_function_prepare_data, NULL);

    // Стадии обработки:
    // - чтение данных из файла;
    pthread_create(&thread1, NULL, thread_function_read_file, NULL);
    // - извлечение необходимого подмножества данных;
    pthread_create(&thread2, NULL, thread_function_extract_data, NULL);
    // - запись извлеченных данных в хранилище.
    pthread_create(&thread3, NULL, thread_function_write_data_DB, NULL);

    // вычисляем и выводим в файл статистику по времени
    pthread_create(&thread4, NULL, thread_function_calc_time, NULL);


    // ждём завершения потоков
    pthread_join(thread0, NULL);
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    pthread_join(thread3, NULL);
    pthread_join(thread4, NULL);

    // освобождение мьютексов
    pthread_mutex_destroy(&mutex_queue1);
    pthread_mutex_destroy(&mutex_queue2);
    pthread_mutex_destroy(&mutex_queue3);
    pthread_mutex_destroy(&mutex_queue4);

    return OK;
}
