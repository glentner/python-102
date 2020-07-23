

from python201.algorithms import cumulative_product

def test_cumulative_product():
    assert cumulative_product([1, 2, 3]) == [1, 2, 6]
    assert cumulative_product([3, 2, 1]) == [3, 6, 6]
    assert cumulative_product([1, 2, 3, 4]) == [1, 2, 6, 24]
    assert cumulative_product([1, 2, 3, 3]) == [1, 2, 6, 18]