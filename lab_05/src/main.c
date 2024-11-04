#include <pthread.h>
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <ctype.h>
#include <string.h>
#include <fcntl.h>    // Для открывания файлов
#include <sys/stat.h> // Для mkdir
#include <string.h>   // Для использования strstr и других функций
#include <libpq-fe.h> // для работы с PostgreSQL

#include "lib_list.h"

#define MAX_LINE_LENGTH 1000
#define INPUT_DATA_DIR "data"

int task_count = 0; // Глобальная переменная для общего количества задач

int task_count1, task_count2, task_count3;                         // сколько каждый поток обработал заявок
node_t Queue1 = NULL, Queue2 = NULL, Queue3 = NULL, Queue4 = NULL; // 4 очереди-списка заявок
pthread_mutex_t mutex_queue1, mutex_queue2, mutex_queue3;          // мьютекс для очередей

// Функция для получения текущего значения тактов процессора
static inline uint64_t rdtsc(void)
{
    unsigned int lo, hi;
    __asm__ volatile("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}

// Функция инициализирует новую заявку TaskDataTime (сам файл не читает)
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
    task->task_data.id = task_count;
    task->task_data.filename = strdup(filename);
    if (task->task_data.filename == NULL)
    {
        perror("Ошибка выделения памяти для имени файла при создании заявки");
        free(task);
        return NULL;
    }
    // Стартовая инициализация массивов
    task->task_data.ingredients = malloc(10 * sizeof(Ingredient));
    task->task_data.steps = malloc(10 * sizeof(char *));
    task->task_data.ingredient_count = 0;
    task->task_data.step_count = 0;
    task->task_data.issue_id = ISSUE_ID;
    task->task_data.url = NULL;
    task->task_data.title = NULL;
    task->task_data.image_url = NULL;
    memset(task->time_data, 0, sizeof(task->time_data));
    return task;
}

// Функция готовит заявки к обработке
int prepare_data(void)
{
    // генерирует заявки с именами файлов из папки data и записывает их в очередь Queue1
    DIR *dir;
    struct dirent *entry;

    // пытаемся открыть папку data
    if ((dir = opendir(INPUT_DATA_DIR)) == NULL)
    {
        perror("Ошибка при открытии папки " INPUT_DATA_DIR);
        return ERROR;
    }

    // проходимся по всем файлам в папке data
    while ((entry = readdir(dir)) != NULL && task_count < MAX_PAGES)
    {
        // игнорируются специальные файлы . и ..
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;

        // создание новой задачи
        TaskDataTime *task = initialize_task(entry->d_name);
        if (task == NULL)
        {
            closedir(dir);
            return ERROR;
        }

        // Защита доступа к очереди 1
        pthread_mutex_lock(&mutex_queue1);
        // кладём элемент в 1 очередь
        put_elem(&Queue1, *task);
        pthread_mutex_unlock(&mutex_queue1); // Освобождаем мьютекс

        task_count++;
    }

    closedir(dir);
    return OK;
}

// Функция, которую выполняет поток №1 (чтение данных из файла)
void *thread_function_read_file(void *arg)
{
    TaskDataTime task;
    while (task_count1 < task_count)
    {
        // берём элемент из первой очереди
        // Защита доступа к очереди 1
        pthread_mutex_lock(&mutex_queue1);
        // Пытаемся получить задачу из очрееди
        if (get_elem(&Queue1, &task) == OK)
        {
            pthread_mutex_unlock(&mutex_queue1); // Освобождаем мьютекс

            // фиксируем время в тиках
            task.time_data[0] = rdtsc();
            // читаем данные (основная работа потока)
            // ------------------------------------
            // Открытие файла
            FILE *file = fopen(task.task_data.filename, "r");
            if (file == NULL)
            {
                perror("Ошибка открытия файла рецепта");
                continue;
            }

            // Парсинг HTML файла
            while (fgets(line, MAX_LINE_LENGTH, file))
            {
                if (strstr(line, "<title>"))
                {
                    // достаём title из HTML
                    char *start = strstr(line, "<title>") + strlen("<title>");
                    char *end = strstr(start, "</title>");
                    if (start && end)
                    {
                        size_t length = end - start;
                        task.task_data.title = malloc(length + 1);
                        strncpy(task.task_data.title, start, length);
                        task.task_data.title[length] = '\0';
                    }
                }
                else if (strstr(line, "data-url=\""))
                {
                    // достаём URL
                    char *start = strstr(line, "data-url=\"") + strlen("data-url=\"");
                    char *end = strstr(start, "\"");
                    if (start && end)
                    {
                        size_t length = end - start;
                        task.task_data.url = malloc(length + 1);
                        strncpy(task.task_data.url, start, length);
                        task.task_data.url[length] = '\0';
                    }
                }
                else if (strstr(line, "<img src=\"") && strstr(line, "class=\"main-image\""))
                {
                    // достаём главное изображение страницы
                    char *start = strstr(line, "<img src=\"") + strlen("<img src=\"");
                    char *end = strstr(start, "\"");
                    if (start && end)
                    {
                        size_t length = end - start;
                        task.task_data.image_url = malloc(length + 1);
                        strncpy(task.task_data.image_url, start, length);
                        task.task_data.image_url[length] = '\0';
                    }
                }
                else if (strstr(line, "<ingredient>"))
                {
                    // достаём ингридиенты
                    char name[50], unit[20];
                    float quantity;
                    sscanf(line, "<ingredient name=\"%[^\"]\" unit=\"%[^\"]\" quantity=\"%f\"/>",
                           name, unit, &quantity);

                    // достаём данные об ингридиентах
                    Ingredient ingredient;
                    ingredient.name = strdup(name);
                    ingredient.unit = strdup(unit);
                    ingredient.count = quantity;

                    task.task_data.ingredients[task.task_data.ingredient_count++] = ingredient;
                }
                else if (strstr(line, "<step>"))
                {
                    // достаём шаги
                    char *start = strstr(line, "<step>") + strlen("<step>");
                    char *end = strstr(line, "</step>");
                    if (start && end)
                    {
                        size_t length = end - start;
                        task.task_data.steps[task.task_data.step_count] = malloc(length + 1);
                        strncpy(task.task_data.steps[task.task_data.step_count], start, length);
                        task.task_data.steps[task.task_data.step_count][length] = '\0';
                        task.task_data.step_count++;
                    }
                }
            }

            fclose(file);
            // ------------------------------------
            // фиксируем время в тиках
            task.time_data[1] = rdtsc();
            task_count1++;
            // кладём элемент во 2 очередь
            // Защита доступа к очереди 2
            pthread_mutex_lock(&mutex_queue2);
            put_elem(&Queue2, task);
            pthread_mutex_unlock(&mutex_queue2); // Освобождаем мьютекс
        }
        else
            pthread_mutex_unlock(&mutex_queue1); // Освобождаем мьютекс
    }
    return NULL;
}

// Функция очищает текст от HTML и лишних символов
void clean_text(char *text)
{
    char *write_ptr = text;
    for (char *read_ptr = text; *read_ptr; read_ptr++)
    {
        if (*read_ptr == '<')
            while (*read_ptr && *read_ptr != '>')
                read_ptr++;
        else if (isalnum(*read_ptr) || isspace(*read_ptr) || *read_ptr == ',' || *read_ptr == '.')
            *write_ptr++ = *read_ptr;
    }
    *write_ptr = '\0';
}

// Функция, которую выполняет поток №2 (извлечение необходимого подмножества данных)
void *thread_function_extract_data(void *arg)
{
    TaskDataTime task;
    while (task_count2 < task_count)
    {
        // берём элемент из 2 очереди
        // Защита доступа к очереди 2
        pthread_mutex_lock(&mutex_queue2);
        // Пытаемся получить задачу из очереди
        if (get_elem(&Queue2, &task) == OK)
        {
            pthread_mutex_unlock(&mutex_queue2); // Освобождаем мьютекс

            // фиксируем время в тиках
            task.time_data[2] = rdtsc();
            // очистка необходимого подмножества данных от HTML и лишних символов (основная работа потока)
            // ------------------------------------
            // Очистка текста от HTML и лишних символов
            clean_text(task.title);
            for (int i = 0; i < task.num_ingredients; i++)
            {
                clean_text(task.ingredients[i].name);
                clean_text(task.ingredients[i].unit);
            }
            for (int i = 0; i < task.num_steps; i++)
                clean_text(task.steps[i]);
            // ------------------------------------
            // фиксируем время в тиках
            task.time_data[3] = rdtsc();
            task_count2++;
            // кладём элемент в 3 очередь
            // Защита доступа к очереди 3
            pthread_mutex_lock(&mutex_queue3);
            put_elem(&Queue3, task);
            pthread_mutex_unlock(&mutex_queue3); // Освобождаем мьютекс
        }
        else
            pthread_mutex_unlock(&mutex_queue2); // Освобождаем мьютекс
    }
    return NULL;
}

// Функция, которую выполняет поток №3 (запись извлеченных данных в хранилище PostgreSQL)
void *thread_function_write_data_DB(void *arg)
{
    TaskDataTime task;
    PGconn *conn;
    const char *query;
    const char *params[5];
    PGresult *res;

    // подключаемся к PostgreSQL
    conn = PQconnectdb("user=postgres dbname=DB_Recipes password=280904");
    if (PQstatus(conn) != CONNECTION_OK)
    {
        fprintf(stderr, "Ошибка подключения к БД: %s", PQerrorMessage(conn));
        PQfinish(conn);
        return NULL;
    }

    while (task_count3 < task_count)
    {
        // берём элемент из 3 очереди
        // Защита доступа к очереди 3
        pthread_mutex_lock(&mutex_queue3);
        // Пытаемся получить задачу из очереди
        if (get_elem(&Queue3, &task) == OK)
        {
            pthread_mutex_unlock(&mutex_queue3); // Освобождаем мьютекс

            // фиксируем время в тиках
            task.time_data[4] = rdtsc();

            // излечение необходимого подмножества данных (основная работа потока)
            // ------------------------------------
            query = "INSERT INTO recipes (id, issue_id, url, title, image_url) VALUES ($1, $2, $3, $4, $5)";
            params[5] = {
                tasks[task_id].task_data.url,
                tasks[task_id].task_data.title,
                tasks[task_id].task_data.image_url};

            res = PQexecParams(conn, query, 5, NULL, params, NULL, NULL, 0);
            if (PQresultStatus(res) != PGRES_COMMAND_OK)
                fprintf(stderr, "Ошибка выполнения запроса: %s", PQerrorMessage(conn));
            PQclear(res);
            // ------------------------------------
            // фиксируем время в тиках
            task.time_data[5] = rdtsc();

            task_count3++;

            // кладём элемент в 4 очередь
            put_elem(&Queue4, task);
        }
        else
            pthread_mutex_unlock(&mutex_queue3); // Освобождаем мьютекс
    }

    PQfinish(conn);
    return NULL;
}

// Функция сравнения для сортировки
int compare(const uint64_t *a, const uint64_t *b)
{
    return (*a > *b) - (*a < *b);
}

// Функция вычисляет
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

    // Сортируем массив и ищем tmed
    qsort(time_stat.arr, task_count, sizeof(uint64_t), (int (*)(const void *, const void *))compare);
    if (task_count % 2 == 0)
        time_stat.tmed = (time_stat.arr[task_count / 2 - 1] + time_stat.arr[task_count / 2]) / 2;
    else
        time_stat.tmed = time_stat.arr[task_count / 2];

    // Запись вычисленного результата в файл
    fprintf(file, "%s: tмин = %lu, tмакс = %lu, tсред = %lu, tмед = %lu\n", help_str, time_stat.tmin,
            time_stat.tmax, time_stat.tavg, time_stat.tmed);
}

// Функция обрабатывает (и очищает) итоговую очередь, обрабатывая замеры времени и выводя результаты в файл measure.txt
int calc_time(void)
{
    typedef struct
    {
        uint64_t arr[task_count];
        uint64_t tmin = -1, tmax = -1, tavg = -1, tmed = -1;
    } TimeStatisticData;

    TimeStatisticData tw1, tw2, tw3, tq2, tq3;

    FILE *file = fopen("measure.txt", "w");
    if (file == NULL)
    {
        perror("Ошибка открытия файла measure.txt");
        return ERROR;
    }

    int n = 0;
    // вычисление массивов времён для последующей обработки (в тиках)
    while (get_elem(&Queue4, &task) == OK)
    {
        // вычисляется {tmin, tmax, tavg, tmed}
        // 1) затраченное i-м обрабатывающим устройством на обработку одной заявки
        tw1.arr[n] = task.time_data[1] - task.time_data[0];
        tw2.arr[n] = task.time_data[3] - task.time_data[2];
        tw3.arr[n] = task.time_data[5] - task.time_data[4];
        // 2) время проведённое заявкой в очередях 2 и 3
        tq2.arr[n] = task.time_data[2] - task.time_data[1];
        tq3.arr[n] = task.time_data[4] - task.time_data[3];
        n++;
    }

    // вычисление искомых значений
    calc_print_time_res(tw1, file, "время обработки устройством №1 ");
    calc_print_time_res(tw2, file, "время обработки устройством №2 ");
    calc_print_time_res(tw3, file, "время обработки устройством №3 ");
    calc_print_time_res(tq2, file, "время, проведённое в очереди №2");
    calc_print_time_res(tq3, file, "время, проведённое в очереди №3");

    fclose(file);
    return OK;
}

// главная функция
int main(void)
{
    pthread_t thread1, thread2, thread3;

    // инициализация мьютексов
    pthread_mutex_init(&mutex_queue1, NULL);
    pthread_mutex_init(&mutex_queue2, NULL);
    pthread_mutex_init(&mutex_queue3, NULL);

    // создание заявок и помещение их в очередь №1
    if (prepare_data() != OK)
        return ERROR;

    // создаём потоки
    // Стадии обработки:
    // - чтение данных из файла;
    pthread_create(&thread1, NULL, thread_function_read_file, NULL);
    // - извлечение необходимого подмножества данных;
    pthread_create(&thread2, NULL, thread_function_extract_data, NULL);
    // - запись извлеченных данных в хранилище.
    pthread_create(&thread3, NULL, thread_function_write_data_DB, NULL);

    // ждём завершения потоков
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    pthread_join(thread3, NULL);

    // вычисляем и выводим статистику по времени
    calc_time();

    // освобождение мьютексов
    pthread_mutex_destroy(&mutex_queue1);
    pthread_mutex_destroy(&mutex_queue2);
    pthread_mutex_destroy(&mutex_queue3);

    return OK;
}
