#include "work_db.h"

// (при необходимости) создаём БД и таблицы
int init_db(void)
{
    int rc = OK;
    int result = system("PGPASSWORD='280904' psql -U olesya -d db_recipes -f create.sql");
    if (result != 0)
    {
        printf("Ошибка выполнения скрипта create.sql\n");
        rc = ERROR;
    }
    return rc;
}

// запись 1 задачи в таблицы
int put_task_to_table(PGconn *conn, TaskDataTime *task)
{
    // запись рецепта в таблицу Recipes
    const char *recipe_query = "INSERT INTO Recipes (id, issue_id, url, title, image_url) VALUES ($1, $2, $3, $4, $5) RETURNING id;";
    char id[10], issue_id[10];
    snprintf(id, sizeof(id), "%d ", task->task_data.id);
    snprintf(issue_id, sizeof(issue_id), "%d ", task->task_data.issue_id);
    const char *recipe_params[5] = {
        id,
        issue_id,
        task->task_data.url,
        task->task_data.title,
        task->task_data.image_url
    };
    PGresult *res = PQexecParams(conn, recipe_query, 5, NULL, recipe_params, NULL, NULL, 0);
    if (PQresultStatus(res) != PGRES_TUPLES_OK)
    {
        printf("Ошибка записи рецепта: %s\n", PQerrorMessage(conn));
        PQclear(res);
        return ERROR;
    }
    PQclear(res);
    // запись ингредиентов рецепта в таблицу Ingredients
    for (int i = 0; i < task->task_data.ingredient_count; i++)
    {
        const char *ing_query = "INSERT INTO Ingredients (rec_id, title, count) VALUES ($1, $2, $3);";
        const char *ing_params[4] = {
            id,
            task->task_data.ingredients[i].name,
            task->task_data.ingredients[i].count,
        };
        res = PQexecParams(conn, ing_query, 3, NULL, ing_params, NULL, NULL, 0);
        if (PQresultStatus(res) != PGRES_COMMAND_OK)
        {
            printf("Ошибка записи ингредиента: %s\n", PQerrorMessage(conn));
            PQclear(res);
            return ERROR;
        }
        PQclear(res);
    }
    // запись шагов рецепта в таблицу Steps
    for (int i = 0; i < task->task_data.step_count; i++)
    {
        const char *step_query = "INSERT INTO Steps (rec_id, step, step_num) VALUES ($1, $2, $3);";
        char step_num[12];
        snprintf(step_num, sizeof(step_num) - 1, "%d", i + 1);
        const char *step_params[3] = {id, task->task_data.steps[i], step_num};
        res = PQexecParams(conn, step_query, 3, NULL, step_params, NULL, NULL, 0);
        if (PQresultStatus(res) != PGRES_COMMAND_OK)
        {
            printf("Ошибка записи шага: %s\n", PQerrorMessage(conn));
            PQclear(res);
            return ERROR;
        }
        PQclear(res);
    }
    return OK;
}

/*
int put_task_to_table(FILE *log_file, TaskDataTime *task)
{
    setbuf(stdout, NULL);
    //printf("START WRITE TO DB.\n");
    // запись в файл информации о рецепте
    fprintf(log_file, "Recipe ID: %d, Issue ID: %d\nURL: %s\nTitle: %s\nImage URL: %s\n\n",
            task->task_data.id,
            task->task_data.issue_id,
            task->task_data.url,
            task->task_data.title,
            task->task_data.image_url);

    // запись ингредиентов рецепта
    fprintf(log_file, "Ingredients:\n");
    for (int i = 0; i < task->task_data.ingredient_count; i++)
    {
        fprintf(log_file, "- Name: %s, Count: %s\n",
                task->task_data.ingredients[i].name,
                task->task_data.ingredients[i].count);
    }
    fprintf(log_file, "\n");

    // запись шагов рецепта
    fprintf(log_file, "Steps:\n");
    for (int i = 0; i < task->task_data.step_count; i++)
    {
        fprintf(log_file, "Step %d: %s\n", i + 1, task->task_data.steps[i]);
    }
    fprintf(log_file, "\n-----------------------------------\n");
    //printf("FINAL WRITE TO DB.\n");

    return OK;
}*/