#include <stdio.h>
#include <stdlib.h>
#include <libpq-fe.h> // для работы с PostgreSQL

#include "const_struct.h"

// (при необходимости) создаём БД и таблицы
int init_db(void);

// запись 1 задачи в таблицы
int put_task_to_table(PGconn *conn, TaskDataTime *task);