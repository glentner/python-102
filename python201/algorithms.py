import sys
from typing import List
from argparse import ArgumentParser, FileType

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
    result = list(array)
    for i, value in enumerate(array[1:]):
        result[i+1] = result[i] * value
    return result


def main(argv: List[str] = None) -> int:
    """Command line entry-point for `cumulative_product`."""

    # command line interface
    parser = ArgumentParser(prog='cumprod',
                            description=cumulative_product.__doc__.strip().split('\n')[0])
    parser.add_argument('-v', '--version', action='version', version='0.0.1')
    parser.add_argument('infile', metavar='FILE', type=FileType(mode='r'), default=sys.stdin,
                        help='input file path (default <stdin>)')
    parser.add_argument('-o', '--output', dest='outfile', metavar='FILE',
                        default=sys.stdout, type=FileType(mode='w'),
                        help='output file path (default <stdout>)')
    parser.add_argument('-l', '--last-only', action='store_true',
                        help='only keep the last value')
    cmdline = parser.parse_args(argv)

    values = map(float, cmdline.infile)
    result = cumulative_product(list(values))

    # '%g' formatting automatically pretty-prints
    start = -1 if cmdline.last_only else 0
    print('\n'.join([f'{value:g}' for value in result[start:]]), file=cmdline.outfile)
    return 0
