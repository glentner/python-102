Manual Page for CUMPROD
=======================

Synopsis
--------

cumprod [-h] [-v] [-o FILE] [-l] FILE


Description
-----------

Compute the cumulative product of a sequence of numbers.


Usage
-----

FILE
    input file path (default <stdin>)


-h, --help
    show this help message and exit

-v, --version
    show program's version number and exit

-o FILE, --output FILE
    output file path (default <stdout>)

-l, --last-only
    only keep the last value

Example
-------

::

    $ seq 5 | cumprod -
    1
    2
    6
    24
    120