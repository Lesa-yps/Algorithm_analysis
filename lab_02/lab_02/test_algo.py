import pytest
from algo import algo_matrix_mult_standard, algo_matrix_mult_Vinograd, algo_matrix_mult_Vinograd_better, ERROR, OK


test_arr = [
        pytest.param([[]],[[]], [[]], ERROR, id="neg_empty_both"),
        pytest.param([[]],[[1]], [[]], ERROR, id="neg_one_both"),
        pytest.param([[2]],[[3]], [[6]], OK, id="one_both"),
        pytest.param([[2]],[[1], [2]], [[]], ERROR, id="neg_1"),
        pytest.param([[3], [4]],[[2, 1], [3, 4]], [[]], ERROR, id="neg_2"),
        pytest.param([[1, 2], [3, 4]],[[0, -1], [5, -2]], [[10, -5], [20, -11]], OK, id="same_size_1"),
        pytest.param([[0, -1], [5, -2]], [[1, 2], [3, 4]], [[-3, -4], [-1, 2]], OK, id="same_size_2"),
        pytest.param([[1, 2], [3, 4], [5, 6]],[[-1, 3, 1], [7, 2, 0]], [[13, 7, 1], [25, 17, 3], [37, 27, 5]], OK, id="diff_size"),
    ]


# стандартный алгоритм умножения матриц
@pytest.mark.parametrize(
    "mat1, mat2, res_c, res_err",
    test_arr
)
def test_algo_matrix_mult_standard(mat1, mat2, res_c, res_err) -> None:
    C, err = algo_matrix_mult_standard(mat1, mat2)
    print(C, err, res_c, res_err)
    assert (err == res_err) and (C == res_c or err == ERROR)

# алгоритм Винограда умножения матриц
@pytest.mark.parametrize(
    "mat1, mat2, res_c, res_err",
    test_arr
)
def test_algo_matrix_mult_Vinograd(mat1, mat2, res_c, res_err) -> None:
    C, err = algo_matrix_mult_Vinograd(mat1, mat2)
    assert err == res_err and (C == res_c or err == ERROR)

# алгоритм Винограда (оптимизированный) умножения матриц
@pytest.mark.parametrize(
    "mat1, mat2, res_c, res_err",
    test_arr
)
def test_algo_matrix_mult_Vinograd_better(mat1, mat2, res_c, res_err) -> None:
    C, err = algo_matrix_mult_Vinograd_better(mat1, mat2)
    assert err == res_err and (C == res_c or err == ERROR)