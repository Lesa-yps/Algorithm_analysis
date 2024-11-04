from sort import selection_sort

# алгоритм поиска по порядку
def algo_search_order(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1  # Возвращаем -1, если элемент не найден

# алгоритм бинарного поиска
def algo_search_bin(arr, x):
    arr = selection_sort(arr)
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2  # Определение среднего индекса
        # Проверка, равен ли средний элемент искомому
        if arr[mid] == x:
            return mid  # Если найден, возвращаем индекс
        # Если искомый элемент больше, игнорируем левую половину
        elif arr[mid] < x:
            left = mid + 1
        # Если искомый элемент меньше, игнорируем правую половину
        else:
            right = mid - 1
    return -1  # Возвращаем -1, если элемент не найден
    

algo_list = [(algo_search_order, "r", "Поиск по порядку"),
             (algo_search_bin, "g", "Бинарный поиск")]