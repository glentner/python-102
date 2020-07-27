.. _performance:

Performance
===========

Typically it’s better to first get something correct (and tested) before scrutinizing performance
unnecessarily. As such, we've saved the matter of "performance" for last. That said, in
scientific/research computing, especially in HPC, it is rather common to encounter performance
bottlenecks.

We'll go through a natural progression. Here is a high-level summary of the topics:

1. **Benchmarking** - You cannot establish that you've made an improvement if you haven't
   benchmarked your code. This is the very first thing. You might even consider adding something
   like this to your automated testing. You're `regression` tests might be timed.
2. **Profiling** - Identify the bottleneck in your code by investigating how much time is spent on
   what line of the code. You might find that a simple fix gives you tremendous improvements. The
   procedure here is similar to debugging and the best way to proceed is with special tools.
3. **Do Not Reinvent the Wheel** - Using existing (possibly compiled) implementations that are
   faster. Pick a different algorithm that may be more efficient.
   Pick a more efficient storage format when handling data.
4. **Compiled Code** - Depending on your code, you might be able to use something like
   `numba <https://numba.pydata.org>`_ to JIT-compile your code and get tremendous performance
   improvements "for free". As a last resort, it is possible to write more efficient code in
   `C`/`C++` that you can link to Python. This is non-trivial.

.. note::

    This section does not offer an exhaustive guide, nor a particularly deep one.
    We merely touch on all the relevant areas. It is up to the developer to take
    each of these ideas and explore deeper.


Benchmarking
------------

Timing Your Code
^^^^^^^^^^^^^^^^

As a simple starting point, lets look at the
`time <https://docs.python.org/3/library/time.html#time.time>`_
function. We can time a section of code as follows:

.. code-block:: python

   import time
   import numpy as np

   t1 = time.time()
   a = np.random.rand(5000, 5000)
   t2 = time.time()
   print("Generating random array took {} seconds".format(t2-t1))

.. code-block:: none

   Generating random array took 0.44880104064941406 seconds

If we want to get both sophisticated and automated, we might consider
implementing a system in our tests to time function calls. We could even
use Python's fantastic
`decorator syntax <http://en.wikipedia.org/wiki/Python_syntax_and_semantics#Decorators>`_
to make it widely applicable.

Interactive Benchmarking with IPython
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``%timeit`` and ``%%timeit`` are
`magic statements <https://ipython.readthedocs.io/en/stable/interactive/magics.html>`_
that can be used in an IPython console or Jupyter notebook
for timing a single line of code or a block of code
conveniently.

.. code-block:: ipython

   In [1]: import numpy as np

   In [2]: %timeit np.random.rand(5000, 5000)
   410 ms ± 2.59 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

   In [3]: %%timeit
      ...: a = np.random.rand(5000, 5000)
      ...: b = np.random.rand(5000, 5000)
      ...: c = a * b
      ...:
   897 ms ± 10.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


Performance Profiling
---------------------

The ``time`` and ``timeit`` methods will get you pretty far in terms of measuring your code's
performance. A more delicate approach would be to apply a tool that can not just time the entire
block, but piece apart how much time is spent on each line so you can see the relative weight of
different parts of the routine.


Line Profiler
^^^^^^^^^^^^^

In IPython, you can use the `line_profiler <https://github.com/rkern/line_profiler>`_ against
a Python statement and tell it what functions to watch. Let's take a look at our function.

.. code-block:: none

    $ pip install line_profiler

.. code-block:: ipython

    In [4]: %load_ext line_profiler

    In [5]: from python201.algorithms import cumulative_product

    In [6]: %lprun -f cumulative_product cumulative_product(list(range(100)))
    Timer unit: 1e-06 s

    Total time: 0.000167 s
    File: /home/glentner/code/github.com/glentner/python201/python201/algorithms.py
    Function: cumulative_product at line 8

    Line #      Hits         Time  Per Hit   % Time  Line Contents
    ==============================================================
         8                                           def cumulative_product(array: List[float]) -> List[float]:
         9                                               """
        10                                               Compute the cumulative product of an array of numbers.
        11
        12                                               Parameters:
        13                                                   array (list): An array of numeric values.
        14
        15                                               Returns:
        16                                                   result (list): A list of the same shape as `array`.
        17
        18                                               Example:
        19                                                   >>> cumulative_product([1, 2, 3, 4, 5])
        20                                                   [1, 2, 6, 24, 120]
        21                                               """
        22         1          3.0      3.0      1.8      result = list(array)
        23       100         70.0      0.7     41.9      for i, value in enumerate(array[1:]):
        24        99         73.0      0.7     43.7          result[i+1] = result[i] * value
        25         1          5.0      5.0      3.0      sample = '[]' if not result else f'[..., {result[-1]:g}]'
        26         1         16.0     16.0      9.6      log.debug(f'cumulative_product: length-{len(result)} array {sample}')
        27         1          0.0      0.0      0.0      return result


There's a wealth of information provided, including the total percent of time spent on each line.
As expected, most of the time is spent around the for-loop with list-accesses. Before we move on
to actually changing the code, let's check out another type of profiling that might be relevant to
scientific software development.

Memory Profiler
^^^^^^^^^^^^^^^

Quite often, it's not necessarily the amount of `time` spent on a piece of code that is problematic;
it could be that too much memory is being used. In Python you can profile the memory consumption of
your code as it is running in a similar way to how we used the ``line_profiler``.

The `memory_profiler <https://github.com/pythonprofilers/memory_profiler>`_ provides a line-by-line
breakdown of a function and the `memory difference` it contributed.

.. code-block:: none

    $ pip install memory_profiler

In order to see this, lets
do something really silly to our code, like add a useless memory accumulator.

.. code-block:: python
    :caption: python201/algorithms.py
    :emphasize-lines: 6,9

    # collapsed for space  ...

    def cumulative_product(array: List[float]) -> List[float]:
        """..."""
        result = list(array)
        big_list = list()
        for i, value in enumerate(array[1:]):
            result[i+1] = result[i] * value
            big_list.append(list(range(10_000_000)))
        sample = '[]' if not result else f'[..., {result[-1]:g}]'
        log.debug(f'cumulative_product: length-{len(result)} array {sample}')
        return result

    # collapsed for space  ...

.. warning::

    Be careful if you do something like this, you might accidentally run your machine
    out of memory and freeze your session. And do not forget to remove these lines when
    you're done!

|

The syntax is similar to before.

.. code-block:: ipython

    In [1]: %load_ext memory_profiler

    In [2]: from python201.algorithms import cumulative_product

    In [3]: %mprun -f cumulative_product cumulative_product(list(range(10)))
    Filename: /home/glentner/code/github.com/glentner/python201/python201/algorithms.py

    Line #    Mem usage    Increment   Line Contents
    ================================================
         8     43.9 MiB     43.9 MiB   def cumulative_product(array: List[float]) -> List[float]:
         9                                 """
        10                                 Compute the cumulative product of an array of numbers.
        11
        12                                 Parameters:
        13                                     array (list): An array of numeric values.
        14
        15                                 Returns:
        16                                     result (list): A list of the same shape as `array`.
        17
        18                                 Example:
        19                                     >>> cumulative_product([1, 2, 3, 4, 5])
        20                                     [1, 2, 6, 24, 120]
        21                                 """
        22     43.9 MiB      0.0 MiB       result = list(array)
        23     43.9 MiB      0.0 MiB       big_list = list()
        24   3520.5 MiB      0.0 MiB       for i, value in enumerate(array[1:]):
        25   3134.2 MiB      0.0 MiB           result[i+1] = result[i] * value
        26   3520.5 MiB    386.7 MiB           big_list.append(list(range(10_000_000)))
        27   3520.5 MiB      0.0 MiB       sample = '[]' if not result else f'[..., {result[-1]:g}]'
        28   3520.5 MiB      0.0 MiB       log.debug(f'cumulative_product: length-{len(result)} array {sample}')
        29   3520.5 MiB      0.0 MiB       return result

Again, all we can measure is the difference in the memory footprint of our program after a given
line executes. It is `very` difficult to actually speak precisely about memory usage. Especially
with container types, if you ask how much space it's using with built-in Python tools (e.g., like
``sys.getsizeof``) you may not be seeing the memory usage of the data the elements of that
container are pointing to.


Do Not Reinvent the Wheel
-------------------------

Writing correct, fast code can be hard. In 2020, if you've come across a problem, chances are that
others have already run across the same challenge. There is likely an existing (possibly even
optimized) implementation for Python.

Use Existing Libraries
^^^^^^^^^^^^^^^^^^^^^^

In our case, you might have already realized if you're familiar with the popular numerical
computing library for Python, `numpy <https://numpy.org>`_, that it already has a fast,
compiled version of the algorithm we're looking for,
`numpy.cumprod <https://numpy.org/doc/stable/reference/generated/numpy.cumprod.html>`_.

Not only is the data stored in a fast data structure in contiguous memory, the for-loop exists
in the C-layer beneath the Python interpreter.

.. code-block:: ipython

    In [1]: from python201.algorithms import cumulative_product as cumprod

    In [2]: import numpy as np

    In [3]: data = np.random.rand(10_000_000)

    In [4]: %timeit result = cumprod(data)
    3.56 s ± 40.8 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

    In [5]: %timeit result = np.cumprod(data)
    33.6 ms ± 287 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

Use Better Algorithms
^^^^^^^^^^^^^^^^^^^^^

This is one of the most effective ways to improve the performance of a program.

When choosing a function from a library or writing your own, ensure that you understand how it
will perform for the type and size of data you have, and what options there may be to boost its
performance. Always benchmark to compare with other functions and libraries.

For example, if you are doing linear algebra, you may benefit from the use of
`sparse <https://en.wikipedia.org/wiki/Sparse_matrix>`_ matrices and algorithms if you are
dealing with very large matrices with relatively few non-zeros.

As another example, many kinds of algorithms are iterative and require an initial "guess" for the
solution. Typically, the closer this initial guess is to the actual solution, the faster the
algorithm performs.

Use Better Data Formats
^^^^^^^^^^^^^^^^^^^^^^^

Familiarize yourself with
the various data formats available for the type of data you are dealing with,
and the performance considerations for each.
For example,
`this page <https://pandas.pydata.org/pandas-docs/stable/io.html>`_
provides a good overview of various data formats for
tabular data supported by the Pandas library.
Performance for each is reported
`here <https://pandas.pydata.org/pandas-docs/stable/io.html#performance-considerations>`_.

Coding Practices and Memory Efficiency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For a better illustration, lets consider another example.

Lets say we want to compute the average ``hindfooth_length`` for
all species in ``plot_id`` 13 in the following dataset:

.. code-block:: ipython

    In [1]: import pandas

    In [2]: data = pandas.read_csv('feet.csv')

    In [3]: data.head()
    Out[3]:
       plot_id species_id  hindfoot_length
    0        2         NL             32.0
    1        3         NL             33.0
    2        2         DM             37.0
    3        7         DM             36.0
    4        3         DM             35.0

Benchmark, benchmark, benchmark!
++++++++++++++++++++++++++++++++

If there are two ways of doing the same thing, *benchmark* to see which is faster for different
problem sizes. For example, one way to do this would be to group by the ``plot_id``, compute the
mean hindfoot length for each group, and extract the result for the group with ``plot_id`` 13:

.. code-block:: ipython

    In [4]: data.groupby('plot_id')['hindfoot_length'].mean()[13]
    Out[4]: 27.570887035633056

Another way would be to filter the data first, keeping only records with ``plot_id`` 13, and then
computing the mean of the ``hindfoot_length`` column:

.. code-block:: ipython

    In [5]: data[data['plot_id'] == 13]['hindfoot_length'].mean()
    Out[5]: 27.570887035633056

Both methods give identical results, but the difference in performance is significant:

.. code-block:: ipython

    In [6]: %timeit data.groupby('plot_id')['hindfoot_length'].mean()[13]
    1.34 ms ± 24.5 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

    In [7]: %timeit data[data['plot_id'] == 13]['hindfoot_length'].mean()
    750 µs ± 506 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)

Why do you think the first method is slower?

Avoid explicit loops
++++++++++++++++++++

Very often, you need to operate on multiple elements of a collection such as a NumPy array or
Pandas DataFrame.

In such cases, it is almost always a bad idea to write an explicit ``for`` loop over the elements.

For instance, looping over the rows (a.k.a, *indices* or *records*) of a Pandas DataFrame is
considered poor practice, and is very slow. Consider replacing values in a column of a dataframe:

.. code-block:: ipython

   In [8]: %%timeit
      ...: for i in range(len(data['species_id'])):
      ...:     if data.loc[i, 'species_id'] == 'NL':
      ...:         data.loc[i, 'species_id'] = 'NZ'
      ...:
   308 ms ± 4.49 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

A better way to do this is simply to use the ``replace()`` method:

.. code-block:: ipython

    In [9]: %time data['species_id'].replace('NL', 'NZ', inplace=True)
    CPU times: user 3.1 ms, sys: 652 µs, total: 3.75 ms
    Wall time: 3.34 ms

In addition to being faster, this also leads to more readable code.

Of course, loops are unavoidable in many situations; but look for alternatives before you write a
``for`` loop over the elements of an array, DataFrame, or similar data structure.

Avoid repeatedly allocating, copying and rearranging data
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Repeatedly creating and destroying new data can be very expensive especially if you are working
with very large arrays or data frames. So avoid, for instance, creating a new array each time
inside a loop. When operating on NumPy arrays, memory is allocated for intermediate results.
Packages like `numexpr <https://github.com/pydata/numexpr>`_ aim to help with this.

Understand when data needs to be copied v/s when data can be operated "in-place". It also helps to
know *when* copies are made. For example, do you think the following code results in two copies of
the same array?

.. code-block:: python

   import numpy as np

   a = np.random.rand(50, 50)
   b = a

`This article <https://nedbatchelder.com/text/names.html>`_
clears up a lot of confusion
about how names and values work in Python
and when copies are made v/s when they are not.

Access data from memory efficiently
+++++++++++++++++++++++++++++++++++

Accessing data in the "wrong order": it is always more efficient to access values that are "closer
together" in memory than values that are farther apart. For example, looping over the elements
along the rows of a 2-d NumPy array is *much* more efficient than looping over the elements along
its columns. Similarly, looping over the columns of a DataFrame in Pandas will be faster than
looping over its rows.

* Redundant computations / computing "too much":
  if you only need to compute on a subset of your data,
  filter *before* doing the computation
  rather than after.

Compiled Code
-------------

Just-in-Time Compilation
^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes there just is not an existing implementation of the algorithm you need. And there
may not be a way of easily `vectorizing` the algorithm, resigning you to "slow" for-loops and
array accesses.

Fortunately these days there is more hope for an easy fix than in the past. If you can write your
code in a rudimentary, line-by-line, `Fortran`-style, there's a chance you might be able to get
tremendous performance improvements without needing to write a "real" C-extension.

`Numba <https://numba.pydata.org/>`_ is a library that lets you compile code written in Python
using a very convenient "decorator" syntax. Lets re-implement our function with some slight
modifications using Numba.

.. code-block:: ipython

    In [6]: from numba import njit

    In [7]: @njit
       ...: def cumprod(array: np.ndarray) -> np.ndarray:
       ...:     result = array.copy()
       ...:     for i, value in enumerate(array[1:]):
       ...:         result[i+1] = result[i] * value
       ...:     return result
       ...:

    In [8]: assert (cumprod(data) == np.cumprod(data)).all()

    In [9]: %timeit result = cumprod(data)
    32.2 ms ± 239 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)

Our JIT-compiled function was `FASTER` than the ``numpy.cumprod`` implementation?!

`Cython <http://cython.org/>`_ is another option for interfacing with compiled code.
It performs about the same as Numba but requires much more effort;
although it can do many things that Numba cannot,
such as generating C code, and
interface with C/C++ libraries.

C-Extensions
^^^^^^^^^^^^

If what you're doing is not amenable to tools like Numba, you can in fact create a native
C-extension yourself. Python has
`documentation <https://docs.python.org/3.8/extending/extending.html>`_ for extending Python,
and there are some pretty good
`tutorials <http://madrury.github.io/jekyll/update/programming/2016/06/20/python-extension-modules.html>`_
online as well.


Extras
------

Parallel and Distributed Computing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your computer has multiple cores, or if you have access to a bigger computer (e.g., a
high-performance computing cluster), parallelizing your code may be an option.

First and foremost, know what layer is appropriate to parallelize at! If the challenge is
that you have a large number of independent tasks to compute and each task is larger than a
few seconds, the optimal approach is to not try to parallelize `within` your code. Instead,
try to expose that part of your code as an executable workflow and use existing tools.
Consider applications like
`GNU Parallel <https://www.gnu.org/software/parallel/>`_ or
`hyper-shell <https://hyper-shell.readthedocs.io>`_ to scale out your workflow. Alternatively,
if your tasks are large enough and you have access to a high-performance computing (HPC)
cluster, use the available scheduler to your advantage and simple schedule all the tasks!

We won't cover the entirety of parallelism here. Below is a list of references you
might consider for parallel and distributed computing in Python.

* `IPython Parallel <https://ipyparallel.readthedocs.io/en/latest/>`_ - A general purpose
  framework using the same infrastructure that makes Jupyter possible. You can create a cluster
  of "headless" IPython engines and connect to them from your main program.

* `Dask <https://dask.pydata.org/en/latest/>`_ - A great library for parallelizing computations
  and operating on large datasets that don't fit in RAM. It implements many similar concepts
  to IPython Parallel but also offers a more data-centric out-of-core computing system.

* `Parsl <http://parsl-project.org>`_ - A newer framework offering some similar concepts to
  Dask and IPython Parallel. Parsl's goal is to offer scalability to the largest super computers
  in the world and integrates with HPC scheduling software.

* Note that many libraries support parallelization without any effort on your part.
  Libraries like Numba and `Tensorflow <https://www.tensorflow.org/>`_
  can use all the cores on your CPU,
  and even your GPU for accelerating computations.



* The `multiprocessing <https://docs.python.org/3/library/multiprocessing.html>`_ package
  is useful when you have several independent tasks that can all be done concurrently.
  `joblib <https://pythonhosted.org/joblib/>`_ is another popular library for this.

Shared-memory Programming
^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes the bottleneck is a hybrid between performance and memory. Many data analysis tasks
require a computation against a large-ish dataset. The challenge is that there are many
"embarrassingly parallel" tasks to compute against the same data, but there isn't enough memory on
the system for every worker to have their own copy, and it's a non-started to have the data
serialized and de-serialized continuously between the workers.

What to do then?

In Python, for a long time this was a tall mountain to summit, getting into some fairly advanced
techniques. Now, thanks to incredible work by the `Apache Arrow <https://arrow.apache.org>`_
project, we can easily share data in-memory between entirely separate processes (even non-Python
processes).

Using the `Plasma In-Memory Object Store <https://arrow.apache.org/docs/python/plasma.html>`_ we
can easily `put` and `get` data structures (e.g., a ``numpy.ndarray``, ``pandas.DataFrame``) to
and from the in-memory store. Another program that `gets` the data only ever gets a reference.
Using one of the above parallelism frameworks, create a pool of workers that all map to the shared
data structure and operate on it as if they each had their own copy.

:download:`See here <../_static/htc_with_plasma.pdf>`.


|
