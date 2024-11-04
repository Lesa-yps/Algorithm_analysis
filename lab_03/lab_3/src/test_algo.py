import pytest
from algo import algo_search_order, algo_search_bin


test_arr = [
        pytest.param([], 1, -1, id="neg_empty_arr"),
        pytest.param([1, 2, 3], 4, -1, id="neg_not_find"),
        pytest.param([1, 2, 3], 1, 0, id="pos_sort_find_first"),
        pytest.param([1, 2, 3], 2, 1, id="pos_sort_find_middle"),
        pytest.param([1, 2, 3], 3, 2, id="pos_sort_find_last"),
    ]

test_arr_order = [
        pytest.param([3, 2, 1], 1, 2, id="pos_not_sort_find_last"),
    ]

test_arr_bin = [
        pytest.param([3, 2, 1], 1, 0, id="pos_not_sort_find_first"),
    ]


# алгоритм поиска по порядку
@pytest.mark.parametrize(
    "arr, x, ind",
    test_arr + test_arr_order
)
def test_algo_search_order(arr, x, ind) -> None:
     assert ind == algo_search_order(arr, x)


# алгоритм бинарного поиска
@pytest.mark.parametrize(
    "arr, x, ind",
    test_arr + test_arr_bin
)
def test_algo_search_bin(arr, x, ind) -> None:
     assert ind == algo_search_bin(arr, x)
   