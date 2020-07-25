
def cumulative_product(array):
    """
    Compute the cumulative product of an array of numbers.

    Parameters
    ----------
    array : list (of numbers)
        An array (list) of numeric values to compute the cumulative
        product for.

    Returns
    -------
    result : list (of numbers)
        A list of the same shape as `array`.

    Example
    -------
    >>> cumulative_product([1, 2, 3, 4, 5])
    [1, 2, 6, 24, 120]
    """
    result = list(array).copy()
    for i, value in enumerate(array[1:]):
        result[i+1] = result[i] * value
    return result
