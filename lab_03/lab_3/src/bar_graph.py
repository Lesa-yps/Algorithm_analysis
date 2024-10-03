import matplotlib.pyplot as plt
from typing import Tuple, List
from sort import selection_sort


def linear_search(arr: List[int], target: int) -> Tuple[int, int]:
    comparisons = 0
    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            return i, comparisons
    return -1, comparisons


def binary_search(arr: List[int], target: int) -> Tuple[int, int]:
    left, right = 0, len(arr) - 1
    comparisons = 0
    while left <= right:
        comparisons += 1
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1, comparisons



def build_linear_search_histogram(arr: List[int], step: int) -> None:
    comparisons_list = []
    for i in range(0, len(arr), step):
        _, comparisons = linear_search(arr, arr[i])
        comparisons_list.append((i, comparisons))    
    plt.bar([str(i[0]) for i in comparisons_list], [i[1] for i in comparisons_list], color='blue', width=0.9)
    plt.xlabel('Индекс элемента')
    plt.ylabel('Число сравнений')
    plt.title('Линейный поиск: число сравнений в зависимости от индекса')
    plt.show()


def build_binary_search_histogram(arr: List[int], step: int) -> None:
    arr = selection_sort(arr)  # Бинарный поиск работает только с отсортированными массивами
    comparisons_list = []
    for i in range(0, len(arr), step):
        _, comparisons = binary_search(arr, arr[i])
        comparisons_list.append((i, comparisons))
    plt.bar([str(i[0]) for i in comparisons_list], [i[1] for i in comparisons_list], color='green', width=0.9)
    plt.xlabel('Индекс элемента')
    plt.ylabel('Число сравнений')
    plt.title('Бинарный поиск: число сравнений в зависимости от индекса')
    plt.show()


def build_binary_search_sorted_by_comparisons(arr: List[int], step: int) -> None:
    arr = selection_sort(arr)  # Бинарный поиск работает только с отсортированными массивами
    comparisons_list = []
    for i in range(0, len(arr), step):
        _, comparisons = binary_search(arr, arr[i])
        comparisons_list.append((i, comparisons))
    # Сортировка по второму элементу кортежа (по числу сравнений)
    sorted_comparisons = sorted(comparisons_list, key=lambda x: x[1])
    plt.bar([str(i[0]) for i in sorted_comparisons], [i[1] for i in sorted_comparisons], color='red', width=0.9)
    plt.xlabel('Элементы (отсортированы по числу сравнений)')
    plt.ylabel('Число сравнений')
    plt.title('Бинарный поиск: сортировка по числу сравнений')
    plt.show()
