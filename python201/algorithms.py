def cumulative_product(array):
    result = array[:1]
    last_value = array[-1]
    for value in array[1:]:
        result.append(result[-1] * value)
        if value == last_value:
            break
    return result