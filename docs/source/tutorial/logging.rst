.. _logging_section:

Logging
=======

In scientific/research computing, especially in high-performance computing when you are running
many jobs with a batch system, it's a good idea to include logging in your libraries and tools. If
you're running many tasks that are meant to occur in a particular sequence, especially if multiple
such workflows are occurring asynchronously across more than one machine, having detailed logs to
review (manually or automatically by another tool) is a powerful way of managing workloads.


Print Statements
----------------

You can print out either a message or the value of some variable, etc., while your code is
running. This is quite common and is usually accomplished with a simple call to the ``print``
function.

.. code-block:: ipython

    In [1]: x = 1.234

    In [2]: print(f'x is {x:.4f}')
    x is 1.234

Doing this is a good idea to keep track of milestones in your code. That way, both when you are
developing your code but also when other users are running the code, they can be notified of an
event, progress, or value.

It’s also typical for novice programmers to attempt a simple form of debugging where print
statements are inserted throughout the program to track behavior or data to verify things are
working as they should. The issue is that these statements are hastily inserted when things aren’t
as they should be and then just as hastily removed afterward. A better approach would be to have a
mechanism by which messages could be included programmatically upon request but suppressed
otherwise.


Conventions
-----------

A `log` is a record of some event or action. In software, logging is the act of keeping a record
of the events and actions done by a program. There are two defining characteristics that
distinguish logging from simple print statements. Messages emitted by the logger can automatically
have additional metadata attached. Further, messages should be filterable based on severity such
that messages below a given level of severity can be suppressed.

Several common attributes (metadata) are typically included in logging messages. Which ones you
should include in your logging setup is a matter of use-case and preference. The following are
things you should consider.

Logging Level
^^^^^^^^^^^^^

As stated, one of the core features of logging is that you should be able to control which
messages are printed as a matter of category. These categories are usually a reference to the
level of severity of the message. There is always a numeric value and a name for a
`logging level <https://docs.python.org/3/howto/logging.html>`_.

Conventionally you have a subset or a superset of the following levels.

1. **DEBUG**    - Detailed information typically used when diagnosing problems.
2. **INFO**     - General purposes messages for tracking progress.
3. **WARNING**  - Something unexpected has occurred and may be important.
4. **ERROR**    - A problem has occurred and a task cannot be completed.
5. **CRITICAL** - The code or application must halt.

These particular levels are not required, they are merely conventional. As we'll see in a moment,
Python automatically supports these levels as described. Some applications include additional
levels for more fine grained control. Completely different schemes are not unheard of either;
another common sort of approach for simple tools may be to just have **OK**/**ERR** messages
instead.

The important feature is that these levels are an ordered set. The numeric value of the level is
what is used to filter against. Setting a logging level of WARNING (i.e., 3) means that levels
below that (DEBUG and INFO) will be suppressed. This is meant to be a run-time option that lets
you include the statements in your code, but switch them off if not needed.

When printing statements, the name of the logging level (often in all-caps), is typically included
`before` the message.

.. code-block:: none

    INFO - all done


Logging Output
^^^^^^^^^^^^^^

There are many targets for outputting logs. Often, logs are simply printed (or redirected from)
the console, or written in plain text to a file. You might imagine having logs written to another
service over the network or maybe even a database. Sometimes, one doesn't preclude the other.

.. note::

    Many software engineers have very strong opinions about what to do with logging output, how it
    should be formatted, and where it should go. We'll stick to the basics and not worry about
    that too much for now.

We'll assume that our messages should be printed as text in some controllable fashion. As discussed in
the previous section on command-line interfaces, you should print messages to `stderr`. This is if the
messages are going to the console; you might allow the user to instead specify a file path to write
the messages to.

What to Include
^^^^^^^^^^^^^^^

In addition to the logging level, you might want to include a few other things. Some good ones include
the timestamp for the message, a topic, and a hostname.

You should include a **timestamp** for your message so you have a record of when the event
occurred. It also might be the case that you are running more than one workflow at a time from
more than one program and it helps if they are all logging timestamps so you can merge them to get
an order of events. In this regard, it's a good idea to include the timestamp at the very
beginning of the message so that you can combine output from multiple sources and sort it with
standard command-line tools.

You should include a **topic** in your message so that you can associate it with some part of your
library. It's not always the case, but often this is done by tagging all your messages by which
module and/or function it came from. This can be done manually in the messages themselves, or
automatically by the logging framework you are using. This can be very helpful in tracking down messages
pertaining to a particular part of your code.

You might want to include the **hostname** of the machine you are running on. This is not as common
as other attributes, but in scientific computing the chances are high that you are running your
workflow on many machines that are not your laptop. It might be useful to know what machine a
particular task ran on when analyzing your logs. This is easy to include automatically in most
logging frameworks.


Logging in Python
-----------------

We've covered a lot of details here, but as with the previous section on command-line interfaces,
Python has you covered with a module from the standard library.

Overview
^^^^^^^^

The `logging <https://docs.python.org/3/library/logging.html>`_ module is quite comprehensive and
allows the user to heavily customize many parts of the behavior. It is pretty straightforward to
implement your own logging functionality; unless you’re doing something special why not use the
standard library?

.. code-block:: ipython

    In [1]: import logging

    In [2]: log = logging.getLogger(__name__)

    In [3]: log
    Out[3]: <Logger __main__ (WARNING)>

Here we've started with a name (usable as a `topic`) and by default our logging level is WARNING.
Our filter works, but our formatting is simply the message for now.

.. code-block:: ipython

    In [4]: log.info('hello, world')

    In [5]: log.warning('uh oh')
    uh oh

We can alter the formatting of the messages that are written by creating a formatter object.
The formatter is an attribute of a `handler`. A logger object has zero or more handlers that
all are free to deal with messages in their own way. We'll setup a stream handler to write to
stderr and add it to our logger.

.. code-block:: ipython

    In [6]: handler = logging.StreamHandler()

    In [7]: handler
    Out[7]: <StreamHandler <stderr> (NOTSET)>

    In [8]: formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s] %(message)s')

    In [9]: handler.setFormatter(formatter)

    In [10]: log.addHandler(handler)

    In [11]: log.warning('oh my')
    2020-07-26 15:35:49,497 WARNING [__main__] oh my

We can change the level if we like to allow lower level message to come through.

.. code-block:: ipython

    In [12]: log.setLevel(logging.INFO)

    In [13]: log.info('hello')
    2020-07-26 15:41:33,491 INFO [__main__] hello

There is a way to have the logging library add an attribute so you can include the hostname in the
message as a named field, like ``%(hostname)s``. This is a bit cumbersome and makes things more
complicated than we'd like at this point. An easy hack though is to literally just code it in.

.. code-block:: ipython

    In [14]: import socket

    In [15]: HOST = socket.gethostname()

    In [16]: HOST
    Out[16]: 'my_machine.local'

    In [17]: formatter = logging.Formatter(f'%(asctime)s {HOST} %(levelname)s [%(name)s] %(message)s')

    In [18]: handler.setFormatter(formatter)

    In [19]: log.info('look at this')
    2020-07-26 15:46:09,422 my_machine.local INFO [__main__] look at this


Module Level Logging
^^^^^^^^^^^^^^^^^^^^

Let's update our code to include logging. When you are developing a Python package, you don't want
to duplicate code in each module. Instead, let's create some generic code in a `logging` module.
We could just add it right alongside our existing module, but it might be a good idea to create a
distinct `core` sub-package for generic code that is separate from our main business-logic. That
way, we can add things later (like configuration file handling) and not clutter our top-level API.

.. code-block:: none
    :emphasize-lines: 16,17,18

    $ tree .
    .
    ├── docs/
    │   ├── build/
    │   │   └── ...
    │   ├── source/
    │   │   ├── conf.py
    │   │   ├── manpage.rst
    │   │   └── index.rst
    │   ├── Makefile
    │   └── make.bat
    ├── LICENSE
    ├── python201/
    │   ├── __init__.py
    │   ├── algorithms.py
    │   └── core/
    │       ├── __init__.py
    │       └── logging.py
    ├── README.rst
    └── setup.py

Again, the ``__init__.py`` file is a signal that this folder is a package (or sub-package).
The ``find_packages`` function we used in our ``setup.py`` will automatically pick this up so
we don't need to worry about modifying any code there.

Our ``logging`` module might look something like this.

.. code-block:: python
    :caption: python201/core/logging.py

    import logging
    from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
    from socket import gethostname


    HOST = gethostname()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(f'%(asctime)s {HOST} %(levelname)s [%(name)s] %(message)s')
    handler.setFormatter(formatter)


    def getLogger(name: str, level: str = 'warning') -> logging.Logger:
        """
        Create a named logger.

        Parameters:
            name (str): name for the logger
            level (str): logging level (default='warning')

        Returns:
            logger (`logging.getLogger`): the created logger instance

        See Also:
            `logging.getLogger`
        """
        log = logging.getLogger(name)
        log.addHandler(handler)
        log.setLevel(getattr(logging, level.upper()))
        return log

We only need to create the handler once. But we want to allow each of the modules in our package
to create a new logger with a distinct name. So we've created a new function with the same name
as the underlying logging library to let us automatically add the handler.

Now let's modify the ``algorithms`` module to make use of our logging module.

.. code-block:: python
    :caption: python201/algorithms.py
    :emphasize-lines: 5,6,25,26,50,51

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


    def main(argv: List[str] = None) -> int:
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
        cmdline = parser.parse_args(argv)

        if cmdline.debug:
            log.setLevel(DEBUG)

        values = map(float, cmdline.infile)
        result = cumulative_product(list(values))

        # '%g' formatting automatically pretty-prints
        start = -1 if cmdline.last_only else 0
        print('\n'.join([f'{value:g}' for value in result[start:]]), file=cmdline.outfile)
        return 0

.. note::

    If you've not seen that syntax before, the import statement for our ``logging`` module is
    called a `relative` import. The leading dot means adjacent. If we had two leading dots it
    would signify one level up, and so on. This way, we need not hard code the name of our
    package.

Let's reinstall our package and try it out.

.. code-block:: none

    $ pip install . --upgrade

.. code-block:: none

    $ cumprod <(seq 10) --last-only
    3.6288e+06

.. code-block:: none

    $ cumprod <(seq 10) --last-only --debug >results.txt
    2020-07-26 20:21:22,340 my_machine.local DEBUG [python201.algorithms] cumulative_product: length-10 array [..., 3.6288e+06]

|
