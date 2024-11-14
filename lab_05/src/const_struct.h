#ifndef CONST_STRUCT_H
#define CONST_STRUCT_H

#include <stdint.h>

#define CPU_FREQUENCY_GHZ 2.6 // частота процессора
#define CPU_FREQUENCY_HZ (CPU_FREQUENCY_GHZ * 1e9) 
#define MAX_PAGES 1000 // Максимальное количество страниц для выгрузки
#define MAX_URL_LENGTH 256 // Максимальная длина URL
#define ISSUE_ID 9233 // из READMINE

// Коды ошибок
#define ERROR 1
#define OK 0

// Структура для одного ингредиента
typedef struct
{
    char *name;
    char *count;
} Ingredient;

// Структура данных рецепта для записи в БД
typedef struct
{
    char* filename;
    // - `id` --- уникальный идентификатор задачи (не из Redmine, см. задание к работе) на обработку рецепта;
    int id;
    // - `issue_id` --- номер задачи из Redmine;
    int issue_id;
    // - `url` --- URL страницы рецепта;
    char *url;
    // - `title` --- название рецепта, например, `"Пирог с малиной"`;
    char *title;
    // - `ingredients` --- массив ингредиентов;
    Ingredient *ingredients;
    int ingredient_count;
    // - `steps` --- шаги рецепта, массив строк, она строка - одно предложение;
    char **steps;
    int step_count;
    // - `image_url` --- URL основного изображения рецепта (если есть).
    char *image_url;
} TaskData;

// Структура, содержащая всю необходимую информацию о заявке
typedef struct
{
    // данные рецепта для записи в БД
    TaskData task_data;
    // данные о временах обработки заявки
    uint64_t time_data[6];
} TaskDataTime;

// Структура для статистики времени
typedef struct
{
    uint64_t *arr;
    uint64_t tmin, tmax, tavg, tmed;
} TimeStatisticData;

#endif // CONST_STRUCT_H