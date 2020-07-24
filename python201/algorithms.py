
def cumulative_product(array):
    result = array.copy()
    for i, value in enumerate(array[1:]):
        result[i+1] = result[i] * value
    return result