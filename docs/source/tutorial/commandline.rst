.. _commandline_interfaces:

Command-line Interfaces
=======================

In addition to including routines in a package that yourself and others can import within other
projects, typically it is a good idea to expose those elements that can stand alone as a command
line utility (e.g., a high level function whose parameters might map in a straightforward way to
command-line arguments). Often such command-line functionality may even be the primary driving force behind initial development of a program (*"I need a script that does X"*), and only later it may evolve into *"I need to incorporate capability X into a higher-level process"*.  Structuring your project so that it can manifest as both a library and a
command-line tool lets others not only execute that routine easily and repeatedly, but also allows
for that routine to be integrated into other workflows.


Conventions
-----------

There are several elements to a good command-line interface that are common to most CLI tools.
Keeping with this common design language makes it easier for others to intuit their way through
the use of your tool; e.g., usage/help statements, command-line arguments, input/output behavior,
exit status.

These design elements can and should be implemented regardless of the language or platform used
to create the application. For many users, it is simply not important what language the tools
was created in, all they see is the command-line interface.

.. note::

    Most everything in this section could be said of a CLI on Windows; however, some aspects of
    the conventions discussed here are particular to Unix/Linux. These days, even on Windows,
    these are the prevailing conventions.


Command-line Arguments
^^^^^^^^^^^^^^^^^^^^^^

The distinguishing characteristic of a "real" command-line tool and `merely` a script is the
presence of what could be a rich set of arguments and options passable to the command.

As with functions in Python, there are both positional arguments and named parameters. Positional
arguments are precisely what they sound like, any and all unqualified arguments that occur on the
command line. If you think of a command line as a sentence, the primary position argument(s) would
be the object of the sentence.

In the following command, ``docs`` is the positional argument of the ``ls`` command.

.. code-block:: bash

    $ ls docs

Named parameters, or `options`, are any qualified argument, typically not necessarily required to
execute the command. That is, `options` usually have default values and you are providing an
alternative.

The convention is that `options` are signaled as such using hyphens. There are `short` form
options and `long` form options. All `short` form options are prefixed with a single hyphen, e.g.,
``-l``. All `long` form options are prefixed with two hyphens and multiple words joined with a
hyphen, e.g., ``--output-directory``.

Options may take zero, one, or more arguments. Sometimes, an option that takes no arguments is
referred to as a `switch`. This is because it's like a true/false setting, e.g., ``--debug``.
Short form options that take no argument can be stacked together, e.g., ``-lh``. Options that take
a single argument can have that argument specified as:

* immediately adjacent, e.g., ``-N8``.
* with a space, e.g., ``-o build``
* with an equal sign, e.g., ``--output-directory=build``.

Finally, a single naked hyphen, ``-``, taken as an option usually is reserved to refer to standard
IO (see next section). And a double hyphen, ``--``, is ignored as a positional argument. It can
generally serve two purposes. Any argument that follows it is forced to be a positional argument
regardless of syntax, e.g., ``-- --output-directory`` if you really mean ``--output-directory`` as
a positional argument (madness!). Also, typically the lack of any argument should signal that you
want to have a usage statement printed (see section below). Passing a ``--`` should allow the user
to execute a command that requires no positional arguments.

File IO
^^^^^^^

In conventional Unix style, commands should read data from standard input (stdin) and publish data
to standard output (stdout). These are special file descriptors whose access can be managed by
your shell. The idea is that you might chain multiple commands into a pipeline, with their inputs
and outputs linked together. This is a powerful concept worth exploring. To the extent possible,
you should allow the user to provide input and output in this way.

That said, in the context of scientific/research computing, especially in high performance
computing (HPC), you would expect files to typically contain data in an efficient binary format,
e.g., HDF5. This is not easily compatible with the above notion. However, there are still some
scenarios to consider.

On all platforms, there is a single input channel (stdin) but `two` output channels (stdout and
stderr). The idea is that data should be written to stdout such that other commands might consume
that data. But stderr should be reserved for messages (e.g., logging, see next section). This way
all commands in a pipeline can have their messages printed in sync while data flows down the
pipeline.

For a CLI tool, it's convention to have the object (primary positional argument) of the command
line refer to input and the lack of that input argument result in data being taken from stdin.
E.g.,

.. code-block:: bash

    $ grep 'def' python201/algorithms.py
    $ cat python201/algorithms.py | grep 'def'


Exit Status
^^^^^^^^^^^

Command-line programs have what's called an `exit status`. This is an integer value reported when
a command exits that is meant to provide some signal regarding the state of the program. Python
will provide an exit status, it's up to you as a developer to make that exit status meaningful.

The idea is that other programs (e.g., a shell script you are writing) should be able to refer to
a previously executed program's exit status in order to take some action. The convention is that
an exit status of zero, ``0``, means everything went as expected, "success". Anything else, any
`non-zero` exit status, means something went wrong. The particular value should have meaning. Many
programs publish the meaning of different exit status values in their documentation.

We will demonstrate how to manage this in your code below.


Usage and Help Text
^^^^^^^^^^^^^^^^^^^

A good CLI tool should print its own usage and help information to standard output upon request.
The convention is that the lack of any arguments (positional or otherwise) is a request to see a
`usage` statement (exceptions exist, the ``python`` command among them).

::

    $ rm
    usage: rm [-f | -i] [-dPRrvW] file ...
       unlink file

To show a more comprehensive statement, a ``-h`` or ``--help`` option should print a longer
message and exit.

::

    $ gzip --help
    usage: gzip [-123456789acdfhklLNnqrtVv] [-S .suffix] [<file> [<file> ...]]
    -1 --fast            fastest (worst) compression
    -2 .. -8             set compression level
    -9 --best            best (slowest) compression
    -c --stdout          write to stdout, keep original files
    --to-stdout
    -d --decompress      uncompress files
    --uncompress
    -f --force           force overwriting & compress links
    -h --help            display this help
    -k --keep            don't delete input files during operation
    -l --list            list compressed file contents
    -N --name            save or restore original file name and time stamp
    -n --no-name         don't save original file name or time stamp
    -q --quiet           output no warnings
    -r --recursive       recursively compress files in directories
    -S .suf              use suffix .suf instead of .gz
    --suffix .suf
    -t --test            test compressed file
    -V --version         display program version
    -v --verbose         print extra statistics

Another convention (as seen with `gzip`) is to allow for the version number of the tool to be
readily printed to stdout upon request with a ``--version`` switch. The short form may be either
``-v`` or ``-V`` depending on if the lower-case ``-v`` is used to mean something else, typically
enabling `verbose` mode (meaning copious output) as seen here.

::

    $ python --version
    Python 3.8.5

.. note::

    Some tools will print the name of the application with the version number. This is not always
    the case and either way is fine.

There are many aspects to the convention regarding the styling of usage and help statements, and
there are as many examples of tools violating the convention as there are conforming to them.
Generally, the following few elements are universal.

* The usage statement begins with the word "usage", ``usage: program ...``.
* The usage statement is listed on a single line if possible, with a one sentence description.
* Options are wrapped in square brackets, e.g., ``[-abc]`` or ``[-o PATH]``.
* Positional arguments are named with either angle brackets or in all capital letters,
  e.g., ``<file>`` or ``FILE``.
* The help text includes the usage statement at the top.
* Positional arguments are listed before optional arguments.


Parsing Command-line Arguments in Python
----------------------------------------

The good news is that in Python you don't need to worry about implementing this convention in
terms of parsing these command-line arguments. We have a built-in module in Python, `argparse
<https://docs.python.org/3/library/argparse.html>`_, that makes it simple to implement interfaces
compliant with these conventions.

Create an ``ArgumentParser`` instance with the name of the program and a brief description,
then use the ``add_argument`` function to add arguments to your interface. Special behavior
is enabled using the ``action`` keyword argument.

.. code-block:: ipython

    In [1]: from argparse import ArgumentParser

    In [2]: parser = ArgumentParser(prog='cumprod',
       ...:                         description='Compute the cumulative product.')

Positional arguments can be specified with just the name. A `metavar` is how it will be referred to
in the usage/help statements. The `type` keyword argument can be anything that is callable as a function.

.. code-block:: ipython

    In [3]: import sys

    In [4]: from argparse import FileType

    In [5]: parser.add_argument('infile', metavar='FILE', type=FileType(mode='r'),
       ...:                     default=sys.stdin, help='input file path (default <stdin>)')
    Out[5]: _StoreAction(option_strings=[], dest='infile', nargs=None, const=None,
    default=<_io.TextIOWrapper name='<stdin>' mode='r' encoding='utf-8'>, type=FileType('r'),
    choices=None, help='input file path (default <stdin>)', metavar='FILE')

You can override what the variable will be referred to as in your code with ``dest``
(short for `destination`). By default, it will take the name of the option, stripped
of its two leading hyphens and any joining hyphens replaced with an underscore,
e.g., ``'--tmp-dir`` would become ``tmp_dir``).

.. code-block:: ipython

    In [6]: parser.add_argument('-o', '--output', dest='outfile', metavar='FILE',
       ...:                     default=sys.stdout, type=FileType(mode='w'),
       ...:                     help='output file path (default <stdout>)')
    Out[6]: _StoreAction(option_strings=['-o', '--output'], dest='outfile', nargs=None, const=None,
    default=<_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>, type=FileType('w'),
    choices=None, help='output file path (default <stdout>)', metavar='FILE')

Switches meant to be true/false are enabled with the ``action`` parameter.

.. code-block:: ipython

    In [7]: parser.add_argument('-l', '--last-only', action='store_true',
       ...:                     help='only keep the last value')
    Out[7]: _StoreTrueAction(option_strings=['-l', '--last-only'], dest='last_only', nargs=0,
    const=True, default=False, type=None, choices=None, help='only keep the last value', metavar=None)

When you've finished adding all of your acceptable options, you can actually `parse` a set
of inputs by calling the ``parse_args`` method with a list of strings. Be default, if nothing
is given it will check ``sys.argv`` to get the "real" arguments to your program.


.. code-block:: ipython

    In [8]: parser.parse_args(['data.txt', '-l'])
    Out[8]: Namespace(infile=<_io.TextIOWrapper name='data.txt' mode='r' encoding='UTF-8'>,
    last_only=True, outfile=<_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>)

Assign the result of this method call to a variable to access these options in your program.

.. code-block:: ipython

    In [9]: cmdline = parser.parse_args(['data.txt', '-l'])

    In [10]: cmdline.outfile
    Out[10]: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>

The `argparse` module implements the full set of conventions outlined above. The usage/help
statements are automatically generated for you (including ``-h`` and ``--help``) and the
convention regarding ``-`` and ``--`` are present as well.

Let's move on to the next section to see how to include this in our project and we'll
see what the usage and help statements look.


Entry-points
------------

In order to expose some part of our package as a command-line tool, we need to create something
called an `entry-point`. Instead of writing a script manually (as a ``.py`` file) and trying to
include it as an executable part of the package, we can actually tell ``setup.py`` to do it for
us automatically (and in a way that's cross-platform!).

We need to add an argument to our ``setup`` function that points to a function in our package
and specify how we want to invoke it at the command-line.

.. code-block:: python
    :caption: setup.py
    :emphasize-lines: 31-33

    from setuptools import setup, find_packages

    with open('README.rst', mode='r') as readme:
        long_description = readme.read()

    setup(
        name             = 'python201',
        version          = '0.0.1',
        author           = 'Geoffrey Lentner',
        author_email     = 'glentner@purdue.edu',
        description      = 'A Python package for numerical algorithms.',
        license          = 'Apache Software License',
        keywords         = 'tutorial packaging example',
        url              = 'https://github.com/glentner/python201',
        packages         = find_packages(),
        include_package_data = True,
        long_description = long_description,
        long_description_content_type = 'text/x-rst',
        classifiers      = ['Development Status :: 4 - Beta',
                            'Programming Language :: Python :: 3.7',
                            'Programming Language :: Python :: 3.8',
                            'Operating System :: POSIX :: Linux',
                            'Operating System :: MacOS',
                            'Operating System :: Microsoft :: Windows',
                            'License :: OSI Approved :: Apache Software License', ],
        install_requires = ['numpy', 'numba', ],
        extras_require   = {
            'dev': ['ipython', 'pytest', 'hypothesis', 'pylint', 'sphinx',
                    'pydata_sphinx_theme'],
        },
        entry_points = {
            'console_scripts': ['cumprod=python201.algorithms:main']
        }
    )

What we've said here is that we want to be able to invoke a command, ``cumprod``, and that we want
it to execute a function, ``python201.algorithms:main``. That is, we need to define a function,
``main`` (the name is arbitrary in fact), within our ``python201.algorithms`` module. This
function will be called for us `without arguments` and it should return an integer. That integer
value will be the exit status of the command.

If we install our package using Pip, this will automatically generate the necessary script and
place it within the ``bin`` folder (or ``Scripts`` on Windows) of our Python prefix. I'm using
a virtual environment on Linux, so I'll have something like the following.

.. code-block:: python
    :caption: /home/glentner/.local/share/virtualenvs/python201-StrqALMO/bin/cumprod

    #!/home/glentner/.local/share/virtualenvs/python201-StrqALMO/bin/python
    # EASY-INSTALL-ENTRY-SCRIPT: 'python201','console_scripts','cumprod'
    import re
    import sys
    from importlib.metadata import distribution

    if __name__ == '__main__':
        sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
        for entry_point in distribution('python201').entry_points:
            if entry_point.group == 'console_scripts' and entry_point.name == 'cumprod':
                sys.exit(entry_point.load()())

.. note::

    The contents of this script will be slightly different for you depending on what platform you
    are on and what (version of) Python you invoked Pip with. On Windows, this will actually
    generate a batch file, ``.bat``, the suffix of which need not be given at the CMD prompt.

Now, there are many ways that you might organize or layout your interface in Python within your
package. There are a few patterns that have become commonplace these days. This tutorial is not
focussed on code style though. Here is what that entry-point might look like in the simplest case.


.. code-block:: python
    :caption: python201/algorithms.py

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


    def main() -> int:
        """command-line entry-point for `cumulative_product`."""

        # command-line interface
        description='Compute the cumulative product of an array of numbers.'
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
        cmdline = parser.parse_args(argv)

        values = map(float, cmdline.infile)
        result = cumulative_product(list(values))

        # '%g' formatting automatically pretty-prints
        start = -1 if cmdline.last_only else 0
        print('\n'.join([f'{value:g}' for value in result[start:]]), file=cmdline.outfile)
        return 0

If we re-install our package we can try it out.

::

    $ pip install . --upgrade

::

    $ cumprod
    usage: cumprod [-h] [-v] [-o FILE] [-l] FILE
    cumprod: error: the following arguments are required: FILE

::

    $ cumprod -h
    usage: cumprod [-h] [-v] [-o FILE] [-l] FILE

    Compute the cumulative product of an array of numbers.

    positional arguments:
      FILE                  input file path (default <stdin>)

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -o FILE, --output FILE
                            output file path (default <stdout>)
      -l, --last-only       only keep the last value

::

    $ cumprod -v
    0.0.1

In Unix-like environments, the ``seq`` command simply produces a sequence of integer values
in a range. Let's use it to compute the cumulative product of a sequence.

::

    $ seq 5
    1
    2
    3
    4
    5

::

    $ seq 5 | cumprod -
    1
    2
    6
    24
    120

::

    $ seq 10 | cumprod -
    1
    2
    6
    24
    120
    720
    5040
    40320
    362880
    3.6288e+06

::

    $ seq 10 > data.txt
    $ cumprod -l < data.txt > result.txt
    $ cat result.txt
    3.6288e+06


Extras
------

Manual Pages
^^^^^^^^^^^^

In addition to having a usage and help statement printable from the command line, if your tool has
a lot of features, it might be a good idea to also include a manual page (or `manpage` for short).
This is in fact particular to Unix-like platforms, but typically in research computing this is the
case anyways.

Manual pages are provided by files stored in directories on your ``MANPATH``. The ``man`` command
looks for these files and parses their special syntax to present nicely formatted page-able output
at the command line. Writing one of these files can be a challenge because of this particular
syntax.

Fortunately, Sphinx makes creating manual pages for your project much easier! We can create
another page in our documentation source tree, say ``manpage.rst``. Sphinx understands what manual
pages are and what sections to expect. A simple example in our case might be something like the
following.


.. code-block:: rst
    :caption: docs/source/manpage.rst

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

We can then edit our configuration file to specify that this page is a manual page and how it
should be treated. Here we have the name of the file, the name of the manual page, the
description, copyright info, and the manual page section to save it under.

.. code-block:: python
    :caption: docs/source/conf.py

    man_pages = [(
        'manpage',
        'cumprod',
        'Compute cumulative product of a sequence of numbers.',
        'Geoffrey Lentner <glentner@purdue.edu>.',
        '1'
    ),
    ]

You can then build your manual page by using the same Makefile as we did for the html website.

::

    $ cd docs
    $ make man

.. note::

    It might complain because your `manpage.rst` wasn't included in the page index for the
    website. This is only a warning and is fine.

In order for you to include your now constructed manual page as part of the Python package, you
need to place it somewhere that your ``setup.py`` file can access and include as an installable
asset. If you are committing your build folder to version control, then you just need to point
there; otherwise, we should copy our new manual page out of the build folder to somewhere we will
commit to version control.

From the top-level of our project folder, we might do something like the following.

::

    $ mkdir -p man/man1
    $ cp docs/build/man/cumprod.1 man/man1/

Then, in our ``setup.py`` file, you can point to our committed copy of the manual page using the
``data_files`` parameter.

.. code-block:: python
    :caption: setup.py
    :emphasize-lines: 34-36

    from setuptools import setup, find_packages

    with open('README.rst', mode='r') as readme:
        long_description = readme.read()

    setup(
        name             = 'python201',
        version          = '0.0.1',
        author           = 'Geoffrey Lentner',
        author_email     = 'glentner@purdue.edu',
        description      = 'A Python package for numerical algorithms.',
        license          = 'Apache Software License',
        keywords         = 'tutorial packaging example',
        url              = 'https://github.com/glentner/python201',
        packages         = find_packages(),
        include_package_data = True,
        long_description = long_description,
        long_description_content_type = 'text/x-rst',
        classifiers      = ['Development Status :: 4 - Beta',
                            'Programming Language :: Python :: 3.7',
                            'Programming Language :: Python :: 3.8',
                            'Operating System :: POSIX :: Linux',
                            'Operating System :: MacOS',
                            'Operating System :: Microsoft :: Windows',
                            'License :: OSI Approved :: Apache Software License', ],
        install_requires = ['numpy', 'numba', ],
        extras_require   = {
            'dev': ['ipython', 'pytest', 'hypothesis', 'pylint', 'sphinx',
                    'pydata_sphinx_theme'],
        },
        entry_points = {
            'console_scripts': ['cumprod=python201.algorithms:main']
        },
        data_files = [
            ('share/man/man1', ['man/man1/cumprod.1', ]),
        ],
    )

This option lets you explicitly list files that you want to include with the package and where you
want them to be installed. Here, the ``share/man/man1`` is a relative path `adjacent` to the
``bin`` folder of our Python installation (where Pip is being executed from as well). This is good
practice and makes it so that your manual page is part of your environment, so when the user
activates the environment they have access to it.

Let's reinstall our package so it includes the command-line entry-point and the manual page.

::

    $ pip install . --upgrade

You can access manual pages with the ``man`` command.

::

    $ man cumprod

::

    CUMPROD(1)                          python201                          CUMPROD(1)



    NAME
           cumprod - Compute cumulative product of a sequence of numbers.

    SYNOPSIS
           cumprod [-h] [-v] [-o FILE] [-l] FILE

    DESCRIPTION
           Compute the cumulative product of a sequence of numbers.

    USAGE
           FILE   input file path (default <stdin>)

           -h, --help
                  show this help message and exit

           -v, --version
                  show program's version number and exit

           -o FILE, --output FILE
                  output file path (default <stdout>)

           -l, --last-only
                  only keep the last value

    EXAMPLE
              $ seq 5 | cumprod -
              1
              2
              6
              24
              120

    AUTHOR
           Geoffrey Lentner <glentner@purdue.edu>.

    COPYRIGHT
           2019-2020 Geoffrey Lentner, 2018 Ashwin Srinath



    0.0.1                              Jul 26, 2020                        CUMPROD(1)

|
