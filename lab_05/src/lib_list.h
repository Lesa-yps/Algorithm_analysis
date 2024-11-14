#ifndef LIB_LIST_H
#define LIB_LIST_H

#include <stdio.h>
#include <stdlib.h>

#include "const_struct.h"

// определение структуры элемента списка
typedef struct Node
{
    TaskDataTime data;
    struct Node *next;
} node_t;

void free_list(node_t **Head);
void put_elem(node_t **Head, TaskDataTime data);
int get_elem(node_t **Head, TaskDataTime *data);

#endif // LIB_LIST_H