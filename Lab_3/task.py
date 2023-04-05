"""External excercise for lab_2."""

from typing import List
import pytest


def is_matrix_square(mat: List[List[int]]) -> bool:
    outerLen = len(mat)

    if (outerLen > 0):
        for innerList in mat:
            if (len(innerList)!=outerLen):
                return False
    else:
        return False
    return True


def get_minor_matrix(mat: List[List[int]], i: int, j: int) -> List[List[int]]:
    minorMat = []

    for index, innerList in enumerate(mat):
        if not(index==i):
            minorRow = [elem for innerIndex, elem in enumerate(innerList) if innerIndex != j]
            minorMat.append(minorRow)

    return minorMat


def matrix_determinant(mat: List[List[int]]) -> int:
    if not(is_matrix_square(mat)):
        raise ValueError("Matrix is not square!")
    
    def matrix_det_inner(matrix: List[List[int]]) -> int:
        if (len(matrix)==1):
            return matrix[0][0]
        sum = 0
        for index, elem in enumerate(matrix[0]):
            sum += ((-1)**index) * elem * matrix_det_inner(get_minor_matrix(matrix,0,index))
        return sum
    
    return matrix_det_inner(mat)


@pytest.mark.parametrize(
    "input_matrix, expected_result",
    [
        ([[2, 4, 2], [3, 1, 1], [1, 2, 0]], True),
        ([[5]], True),
        ([[2, 4], [1, 8], [2, 5]], False)
    ]
)
def test_is_matrix_square(input_matrix, expected_result):
    assert expected_result == is_matrix_square(input_matrix)


@pytest.mark.parametrize(
    "input_matrix, row, col, expected_result",
    [
        ([[3, 0, -1], [-1, -1, 0], [1, -1, 2]], 0, 0, [[-1, 0], [-1, 2]]),
        ([[3, 0, -1], [-1, -1, 0], [1, -1, 2]], 1, 1, [[3, -1], [1, 2]]),
        (
            [
                [2, 5, 3, 6, 3],
                [17, 5, 7, 4, 2],
                [7, 8, 5, 3, 2],
                [9, 4, -6, 8, 3],
                [2, -5, 7, 4, 2]
            ],
            2,
            3,
            [
                [2, 5, 3, 3],
                [17, 5, 7, 2],
                [9, 4, -6, 3],
                [2, -5, 7, 2]
            ],
        ),
    ]
)
def test_get_minor_matrix(input_matrix, row, col, expected_result):
    assert expected_result == get_minor_matrix(input_matrix, row, col)


@pytest.mark.parametrize(
    "matrix, expected_determinant",
    [
        ([[5]], 5),
        ([[4, 6], [3, 8]], 14),
        ([[2, 4, 2], [3, 1, 1], [1, 2, 0]], 10),
        ([[6, 1, 1], [4, -2, 5], [2, 8, 7]], -306),
        ([[2, 4, -3], [1, 8, 7], [2, 3, 5]], 113),
        ([[1, 2, 3, 4], [5, 0, 2, 8], [3, 5, 6, 7], [2, 5, 3, 1]], 24),
        (
            [
                [2, 5, 3, 6, 3],
                [17, 5, 7, 4, 2],
                [7, 8, 5, 3, 2],
                [9, 4, -6, 8, 3],
                [2, -5, 7, 4, 2],
            ],
            2060,
        ),
        (
            [
                [1, 2, 4, 0, 9],
                [2, 3, 4, 1, 1],
                [6, 7, 3, 9, 3],
                [2, 0, 3, 0, 2],
                [4, 5, 2, 3, 1],
            ],
            1328,
        ),
        (
            [
                [2, 4, 5, 3, 1, 2],
                [2, 4, 7, 5, 3, 2],
                [1, 1, 0, 2, 3, 1],
                [1, 3, 9, 0, 3, 2],
                [1, 1, 2, 2, 4, 1],
                [0, 0, 4, 1, 2, 3],
            ],
            88,
        ),
        (
            [
                [3, 2, 1, 4, 0, 1],
                [1, 2, 3, 1, 9, 1],
                [0, 2, 1, 1, 9, 0],
                [8, 2, 1, 0, 2, 3],
                [2, 3, 4, 0, 1, 2],
                [2, 1, 0, 0, 1, 1],
            ],
            -536,
        ),
    ],
)
def test_matrix_determinant_correct(matrix, expected_determinant):
    assert expected_determinant == matrix_determinant(
        matrix
    ), "Incorrect result!"


@pytest.mark.parametrize(
    "incorrect_matrix",
    [
        ([[]]),
        ([[4, 6]]),
        ([[2, 4, -3], [1, 8, 7], [2, 5]]),
        ([[1, 2, 3, 4], [0, 2, 8], [3, 5, 6, 7], [2, 3, 1]]),
        (
            [
                [2, 5, 3, 6, 3],
                [17, 5, 7, 4, 2],
                [7, 8, 5, 3, 2],
                [9, 4, -6, 8, 3],
                [2, -5, 7, 4, 2],
                [2, -5, 7, 4, 2],
            ]
        ),
        ([[1, 2, 4, 0, 9], [2, 3, 4, 1], [6, 7, 3], [2, 0], [4]]),
    ],
)
def test_matrix_determinant_incorrect(incorrect_matrix):
    with pytest.raises(ValueError) as excinfo:
        matrix_determinant(incorrect_matrix)
    assert "Matrix is not square!" in str(excinfo.value)
