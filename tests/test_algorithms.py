
import pytest
from python201.algorithms import cumulative_product


def test_cumulative_product_simple():
    assert cumulative_product([1, 2, 3]) == [1, 2, 6]
    assert cumulative_product([3, 2, 1]) == [3, 6, 6]
    assert cumulative_product([1, 2, 3, 4]) == [1, 2, 6, 24]
    assert cumulative_product([1, 2, 3, 3]) == [1, 2, 6, 18]

def test_cumulative_product_empty():
    assert cumulative_product([]) == []

def test_cumulative_product_starts_with_zero():
    assert cumulative_product([0] + list(range(100))) == [0] * 101