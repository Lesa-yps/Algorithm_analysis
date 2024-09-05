import pytest
from algo import algo_Levenstein_matrix, algo_Levenstein_recursion, algo_Damerau_Levenstein_matrix, algo_Damerau_Levenstein_recursion,\
      algo_Levenstein_recursion_matrix, algo_Damerau_Levenstein_recursion_matrix


test_arr = [
        pytest.param("", "", 0, id="pos_1"),
        pytest.param("a", "a", 0, id="pos_2"),
        pytest.param("abc", "abc", 0, id="pos_3"),
        pytest.param("", "a", 1, id="neg_1"),
        pytest.param("a", "", 1, id="neg_2"),
        pytest.param("a", "b", 1, id="neg_3"),
        pytest.param("abc", "abs", 1, id="neg_4"),
        pytest.param("odc", "abc", 2, id="neg_5"),
        pytest.param("ods", "abc", 3, id="neg_6"),
        pytest.param("absc", "abc", 1, id="neg_7"),
        pytest.param("bc", "abc", 1, id="neg_8"),
    ]

test_arr_Levenstein = [pytest.param("bac", "abc", 2, id="exstrim")]

test_arr_Damerau_Levenstein = [pytest.param("bac", "abc", 1, id="exstrim")]


# алгоритм Левенштейна (матричная реализация, хранит только текущую и предыдущую строки матрицы)
@pytest.mark.parametrize(
    "str1, str2, res",
    test_arr + test_arr_Levenstein
)
def test_algo_Levenstein_matrix(str1: str, str2: str, res: int) -> None:
    assert algo_Levenstein_matrix(str1, str2) == res

# алгоритм Левенштейна (рекурсивная реализация)
@pytest.mark.parametrize(
    "str1, str2, res",
    test_arr + test_arr_Levenstein
)
def test_algo_Levenstein_recursion(str1: str, str2: str, res: int) -> None:
    assert algo_Levenstein_recursion(str1, str2) == res

# алгоритм Левенштейна (рекурсивно-матричная реализация)
@pytest.mark.parametrize(
    "str1, str2, res",
    test_arr + test_arr_Levenstein
)
def test_algo_Levenstein_recursion_matrix(str1: str, str2: str, res: int) -> None:
    assert algo_Levenstein_recursion_matrix(str1, str2) == res



# алгоритм Дамерау-Левенштейна (матричная реализация)
@pytest.mark.parametrize(
    "str1, str2, res",
    test_arr + test_arr_Damerau_Levenstein
)
def test_algo_Damerau_Levenstein_matrix(str1: str, str2: str, res: int) -> None:
    assert algo_Damerau_Levenstein_matrix(str1, str2) == res

# алгоритм Дамерау-Левенштейна (рекурсивная реализация)
@pytest.mark.parametrize(
    "str1, str2, res",
    test_arr + test_arr_Damerau_Levenstein
)
def test_algo_Damerau_Levenstein_recursion(str1: str, str2: str, res: int) -> None:
   assert algo_Damerau_Levenstein_recursion(str1, str2) == res

# алгоритм Дамерау-Левенштейна (рекурсивно-матричная реализация)
@pytest.mark.parametrize(
    "str1, str2, res",
    test_arr + test_arr_Damerau_Levenstein
)
def test_algo_Damerau_Levenstein_recursion_matrix(str1: str, str2: str, res: int) -> None:
   assert algo_Damerau_Levenstein_recursion_matrix(str1, str2) == res
