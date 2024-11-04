#include "lib_list.h"


void free_node(node_t **node1)
{
    if (*node1 != NULL)
    {
        free(*node1);
        *node1 = NULL;
    }
}

void free_list(node_t **Head)
{
    while (*Head != NULL)
    {
        node_t *tmp = *Head;
        *Head = (*Head)->next;
        free_node(&tmp);
    }
}

int create_node(node_t **new_node, TaskDataTime data)
{
    int rc = OK;
    *new_node = (node_t *)calloc(1, sizeof(node_t));
    if (*new_node == NULL)
        rc = ERR_MEM;
    else
    {
        (*new_node)->data = data;
        (*new_node)->next = NULL;
    }
    return rc;
}

void put_elem(node_t **Head, TaskDataTime data)
{
    node_t *new_node = NULL;
    if (create_node(&new_node, data) == OK)
    {
        // очередь пуста
        if (*Head == NULL)
            *Head = new_node;
        else
        {
            node_t cur = *Head;
            while (cur->next != NULL)
                cur = cur->next;
            new_node->next = cur->next;
            cur->next = new_node;
        }
    }
}

int get_elem(node_t **Head, TaskDataTime *data)
{
    // очередь пуста
    if (*Head == NULL)
        return ERROR;
    node_t *tmp = *Head;
    *data = tmp->data;
    *Head = (*Head)->next;
    free(tmp);
    return OK;
}
