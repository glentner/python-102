import sys
from typing import List
from argparse import ArgumentParser, FileType

from .core.logging import getLogger, DEBUG
log = getLogger(__name__)

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
    sample = '[]' if not result else f'[..., {result[-1]:g}]'
    log.debug(f'cumulative_product: length-{len(result)} array {sample}')
    return result


def main() -> int:
    """Command line entry-point for `cumulative_product`."""

    # command line interface
    description = 'Compute the cumulative product of an array of numbers.'
    parser = ArgumentParser(prog='cumprod', description=description)
    parser.add_argument('-v', '--version', action='version', version='0.0.1')
    parser.add_argument('infile', metavar='FILE', type=FileType(mode='r'),
                        default=sys.stdin,
                        help='input file path (default <stdin>)')
    parser.add_argument('-o', '--output', dest='outfile', metavar='FILE',
                        default=sys.stdout, type=FileType(mode='w'),
                        help='output file path (default <stdout>)')
    parser.add_argument('-l', '--last-only', action='store_true',
                        help='only keep the last value')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='show debugging messages')
    cmdline = parser.parse_args()

    if cmdline.debug:
        log.setLevel(DEBUG)

    values = map(float, cmdline.infile)
    result = cumulative_product(list(values))

    # '%g' formatting automatically pretty-prints
    start = -1 if cmdline.last_only else 0
    print('\n'.join([f'{value:g}' for value in result[start:]]), file=cmdline.outfile)
    return 0
