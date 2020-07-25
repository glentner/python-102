from typing import List

def cumulative_product(array: List[float]) -> List[float]:
    """
    Compute the cumulative product of an array of numbers.

    Parameters:
        array (list): An array of numeric values.

    Returns:
        result (list): A list of the same shape as `array`.

    Example:
        >>> cumulative_product([1, 2, 3, 4, 5])
        [1, 2, 6, 24, 120]
    """
    result = list(array).copy()
    for i, value in enumerate(array[1:]):
        result[i+1] = result[i] * value
    return result
