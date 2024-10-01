# сортировка выбором
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        # Предполагаем, что текущий элемент - это минимум
        min_index = i
        # Находим минимальный элемент в оставшейся части массива
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        # Меняем местами найденный минимальный элемент с текущим элементом
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

# Пример использования
if __name__ == "__main__":
    arr = [5, 3, 2, 4, 1, 6]
    sorted_arr = selection_sort(arr)
    print("Отсортированный массив: ", sorted_arr)
