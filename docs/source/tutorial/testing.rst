.. _testing:

Testing
=======

Now that we've encapsulated our code in a well structured and installable package,
how can we validate that our code is robust and works as expected?

`We want to address the following ...`

* How can you write modular, extensible, and reusable code?
* After making changes to a program, how do you ensure that it will still give
  the same answers as before?
* How can we make finding and fixing bugs an easy, fun, and rewarding experience?

These seemingly unrelated questions all have the same answer, and it is
`automated testing`.

.. note::

   This section was originally based on Ned Batchelder's
   excellent article and PyCon 2014 talk
   `Getting Started Testing <https://nedbatchelder.com/text/test0.html>`_.

   | "*Tests are the dental floss of development: everyone knows they should do it more, but they don’t, and they feel guilty about it.*"
   | - Ned Batchelder

   | "*Code without tests should be approached with a 10-foot pole.*"
   | - Ashwin Srinath


Testing Interactively
---------------------

Let's look at our initial bit of code.

.. code-block:: python
    :caption: python201/algorithms.py

    def cumulative_product(array):
        result = array[:1]
        last_value = array[-1]
        for value in array[1:]:
            result.append(result[-1] * value)
            if value == last_value:
                break
        return result

While we were developing this function, we would have likely started up an IPython console and
either copied the code snippet or imported the function and tested it on a few simple cases to
validate that it returns expected results.

.. code-block:: ipython

    In [1]: from python201.algorithms import cumulative_product

    In [2]: cumulative_product([1, 2, 3])
    Out[2]: [1, 2, 6]

    In [3]: cumulative_product([3, 2, 1])
    Out[3]: [3, 6, 6]

    In [4]: cumulative_product([1, 2, 3, 4])
    Out[4]: [1, 2, 6, 24]

While this kind of testing is better than not doing any testing at all, it leaves much to be
desired. First, it needs to be done each time ``cumulative_product`` is changed. It also requires
that we manually inspect the output from each test to decide if the code "passes" or "fails" that
test. Further, we need to remember all the tests we came up with today if we want to test again
tomorrow.


Test Scripts
------------

A `much` better way to write tests is to put them in a script.

.. code-block:: python
    :caption: tests/test_algorithms.py

    from python201.algorithms import cumulative_product

    array = [1, 2, 3]
    print(f'cumulative_product({array}) ==', cumulative_product(array))

    array = [3, 2, 1]
    print(f'cumulative_product({array}) ==', cumulative_product(array))

    array = [1, 2, 3, 4]
    print(f'cumulative_product({array}) ==', cumulative_product(array))

Now, running and re-running our tests is very easy - we just run the script.

.. code-block:: none

    $ python tests/test_algorithms.py
    cumulative_product([1, 2, 3]) == [1, 2, 6]
    cumulative_product([3, 2, 1]) == [3, 6, 6]
    cumulative_product([1, 2, 3, 4]) == [1, 2, 6, 24]

It’s also easy to add new tests, and there’s no need to remember all the tests we come up with.

Assertions
----------

One problem with the method above is that
we *still* need to manually inspect the results of our tests.

Assertions can help with this. The ``assert`` statement in Python is very simple: Given a
condition, like ``1 == 2``, it checks to see if the condition is true or false. If it is true,
then ``assert`` does nothing, and if it false, it raises an ``AssertionError``.

.. code-block:: ipython

    In [1]: assert 1 == 1

    In [2]: assert 1 < 2

    In [3]: assert 1 > 2
    ---------------------------------------------------------------------------
    AssertionError                            Traceback (most recent call last)
    <ipython-input-3-f53b9196f459> in <module>
    ----> 1 assert 1 > 2

    AssertionError:

We can re-write our script as follows.

.. code-block:: python
    :caption: tests/test_algorithms.py

    from python201.algorithms import cumulative_product

    assert cumulative_product([1, 2, 3]) == [1, 2, 6]
    assert cumulative_product([3, 2, 1]) == [3, 6, 6]
    assert cumulative_product([1, 2, 3, 4]) == [1, 2, 6, 24]

And we still run our tests the same way.

.. code-block:: none

    $ python tests/test_algorithms.py

This time, there's no need to inspect the test results. If we get an ``AssertionError``,
then we had a test fail; and if not, all our tests passed.

That said, there's no way to know if `more` than one test failed. The script stops executing
after the first ``AssertionError`` is encountered. Let's add another test to our test script and
re-run it.

.. code-block:: python
    :caption: tests/test_algorithms.py

    from python201.algorithms import cumulative_product

    assert cumulative_product([1, 2, 3]) == [1, 2, 6]
    assert cumulative_product([3, 2, 1]) == [3, 6, 6]
    assert cumulative_product([1, 2, 3, 4]) == [1, 2, 6, 24]
    assert cumulative_product([1, 2, 3, 3]) == [1, 2, 6, 18]

.. code-block:: none

    $ python tests/test_algorithms.py
    Traceback (most recent call last):
      File "tests/test_algorithms.py", line 8, in <module>
        assert cumulative_product([1, 2, 3, 3]) == [1, 2, 6, 18]
    AssertionError

This time we get a failed test, because -- as we said -- our code is "bad". Before adding
more tests to investigate, we'll discuss one more method for running tests.


Automated Testing
-----------------

A test runner takes a bunch of tests, executes them all, and then reports which of them passed
and which of them failed. A very popular test runner for Python is
`pytest <https://docs.pytest.org/en/latest/>`_.

Like many testing frameworks, ``pytest`` can be quite sophisticated. For the purposes of
this tutorial, we'll stick to the basics. Essentially, if you place all of your tests within
the appropriate layout, ``pytest`` will automatically find and execute all your tests.

We want all of our tests to live under files that start with ``test`` and we need all of our tests
to be encapsulated by functions that also start with ``test``. A nice approach is to have a top
level ``tests`` folder in your project with a structure that mirrors your python package,
including a ``tests_X.py`` partner for every module in your package.

In our case, we would have ``tests/test_algorithms.py``.

.. code-block:: python
    :caption: tests/test_algorithms.py

    from python201.algorithms import cumulative_product

    def test_cumulative_product():
        assert cumulative_product([1, 2, 3]) == [1, 2, 6]
        assert cumulative_product([3, 2, 1]) == [3, 6, 6]
        assert cumulative_product([1, 2, 3, 4]) == [1, 2, 6, 24]
        assert cumulative_product([1, 2, 3, 3]) == [1, 2, 6, 18]

To run our tests, we simply execute ``pytest`` at the command line at the top of our
project.

.. code-block:: none

    $ pytest
    =================================== test session starts ====================================
    platform linux -- Python 3.8.3, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
    rootdir: /home/glentner/code/github.com/glentner/python201
    plugins: hypothesis-5.20.3
    collected 1 item

    tests/test_algorithms.py F                                                           [100%]

    ========================================= FAILURES =========================================
    _________________________________ test_cumulative_product __________________________________

        def test_cumulative_product():
            assert cumulative_product([1, 2, 3]) == [1, 2, 6]
            assert cumulative_product([3, 2, 1]) == [3, 6, 6]
            assert cumulative_product([1, 2, 3, 4]) == [1, 2, 6, 24]
    >       assert cumulative_product([1, 2, 3, 3]) == [1, 2, 6, 18]
    E       assert [1, 2, 6] == [1, 2, 6, 18]
    E         Right contains one more item: 18
    E         Use -v to get the full diff

    tests/test_algorithms.py:9: AssertionError
    ================================= short test summary info ==================================
    FAILED tests/test_algorithms.py::test_cumulative_product - assert [1, 2, 6] == [1, 2, 6, 18]
    ==================================== 1 failed in 0.21s =====================================


Pytest has found our test modules and run all our tests. Each module will be reported on its own
line. A `dot` will appear while it is running each test. An ``F`` is printed when a test fails
with a summary of what happened. Here we see that our final comparison failed and we are told
precisely what the problem is.


Useful Tests
------------

Now that we know how to write and run tests, what kind of tests should we write?
Testing ``cumulative_product`` for arbitrary choices of inputs like ``[1, 2, 3]``
might not tell us much about where the problem might be.

Instead, we should choose tests that exercise specific functionality of the code we are testing,
or represent different conditions that the code may be exposed to.

For example:

* An array of length 0 or 1.
* An array of mixed signs or precisions.
* An array containing NaN values.

In our case, it was even simpler than that; the existence of a value equal to that of the final
value prematurely truncates the sequence.

.. note::

    Handling edge cases like those listed above are of course important, but even simple tests
    that may seem silly are equally important sanity checks that will exercise your code when you
    make changes.


Fixing the Code
---------------

Let's rewrite our function to be a bit more `Pythonic` and without that troublesome bug.


.. code-block:: python
    :caption: python201/algorithms.py

    def cumulative_product(array):
        result = list(array).copy()
        for i, value in enumerate(array[1:]):
            result[i+1] = result[i] * value
        return result

Not necessarily perfect, but clean and concise. Our intent is better expressed by the code
and we've become a bit more flexible with the possible input data types.
And we've eliminated the bug!

.. code-block:: python
    :caption: tests/test_algorithms.py

    from python201.algorithms import cumulative_product

    def test_cumulative_product_simple():
        assert cumulative_product([1, 2, 3]) == [1, 2, 6]
        assert cumulative_product([3, 2, 1]) == [3, 6, 6]
        assert cumulative_product([1, 2, 3, 4]) == [1, 2, 6, 24]
        assert cumulative_product([1, 2, 3, 3]) == [1, 2, 6, 18]

    def test_cumulative_product_empty():
        assert cumulative_product([]) == []

    def test_cumulative_product_starts_with_zero():
        assert cumulative_product([0] + list(range(100))) == [0] * 101

Let's run our tests again.

.. code-block:: none

    $ pytest
    ================================== test session starts ===================================
    platform linux -- Python 3.8.3, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
    rootdir: /home/glentner/code/github.com/glentner/python201
    plugins: hypothesis-5.20.3
    collected 3 items

    tests/test_algorithms.py ...                                                       [100%]

    =================================== 3 passed in 0.09s ====================================


Types of Testing
----------------

Software testing is a vast topic and there are
`many levels and types <https://en.wikipedia.org/wiki/Software_testing>`_
of software testing. For scientific and
research software, the focus of testing efforts is primarily:

1. **Unit tests**: Unit tests aim to test small, independent sections of code
   (a function or parts of a function),
   so that when a test fails,
   the failure can easily be associated with that section of code.
   This is the kind of testing that we have been doing so far.

2. **Regression tests**: Regression tests aim to check whether
   changes to the program result in it producing
   different results from before.
   Regression tests can test
   larger sections of code
   than unit tests.
   As an example, if you are writing a machine learning application,
   you may want to run your model on small data
   in an automated way
   each time your software undergoes changes,
   and make sure that the same (or a better) result is produced.


Test-Driven Development
-----------------------

`Test-driven development (TDD) <https://en.wikipedia.org/wiki/Test-driven_development>`_
is the practice of writing tests for a function or method
*before* actually writing any code for that function or method.
The TDD process is to:

1. Write a test for a function or method
2. Write just enough code that the function or method passes that test
3. Ensure that all tests written so far pass
4. Repeat the above steps until you are satisfied with the code

Proponents of TDD suggest that this results in better code.
Whether or not TDD sounds appealing to you,
writing tests should be *part* of your development process,
and never an afterthought.
In the process of writing tests,
you often come up with new corner cases for your code,
and realize better ways to organize it.
The result is usually code that is
more modular,
more reusable
and of course,
more testable,
than if you didn't do any testing.

.. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/TDD_Global_Lifecycle.png/1920px-TDD_Global_Lifecycle.png
    :target: https://en.wikipedia.org/wiki/Test-driven_development
    :alt: Test-Driven Development



Growing a Useful Test Suite
---------------------------

More tests are always better than less,
and your code should have as many tests as you are willing to write.
That being said,
some tests are more useful than others.
Designing a useful suite of tests is a challenge in itself,
and it helps to keep the following in mind when growing tests:

1. **Tests should run quickly**: testing is meant to be done as often as possible.
   Your entire test suite should complete in no more than a few seconds,
   otherwise you won't run your tests often enough for them to be useful.
   Always test your functions or algorithms on very small and simple data;
   even if in practice they will be dealing with more complex and large datasets.

2. **Tests should be focused**: each test should exercise a small part of your code.
   When a test fails,
   it should be easy for you to
   figure out which part of your program you need to focus debugging efforts on.
   This can be difficult if your code isn't modular,
   i.e., if different parts of your code depend heavily on each other.
   This is one of the reasons TDD is said to produce more modular code.

3. **Tests should cover all possible code paths**: if your function has multiple code paths
   (e.g., an *if-else* statement),
   write tests that execute both the "if" part
   and the "else" part.
   Otherwise, you might have bugs in your code and still have all tests pass.

4. **Test data should include difficult and edge cases**: it's easy to
   write code that only handles cases with well-defined inputs and outputs.
   In practice however, your code may have to deal with
   input data for which it isn't clear what the behavior should be.
   For example, what should ``cumulative_product([])`` return?
   Make sure you write tests for such cases,
   so that you force your code to handle them.

|

Extras
------

Hypothesis
^^^^^^^^^^

Like many such frameworks, ``pytest`` has a plugin system that allows its functionality to be
extended by design. A notable package that works as a plugin for ``pytest`` is
`Hypothesis <https://hypothesis.readthedocs.io/en/latest/index.html>`_.

``Hypothesis`` implements `property-based testing` that allows you to write unit tests in a way
that isn't hard-coded. You define strategies for given inputs and ``hypothesis`` automatically generates
entire ensembles of tests for a given definition including edge cases you would want to cover.

For our `zero` test, if the initial value of the array is zero, it simply doesn't matter what the
remaining values of the array are, the result will be an array of the same length and all zeros.
So our test could use ``hypothesis`` to define a strategy that will test many cases without us
hard coding them.

.. code-block:: python
    :caption: tests/test_algorithms.py

    from hypothesis.strategies import lists, integers
    from hypothesis import given

    from python201.algorithms import cumulative_product


    def test_cumulative_product_simple():
        assert cumulative_product([1, 2, 3]) == [1, 2, 6]
        assert cumulative_product([3, 2, 1]) == [3, 6, 6]
        assert cumulative_product([1, 2, 3, 4]) == [1, 2, 6, 24]
        assert cumulative_product([1, 2, 3, 3]) == [1, 2, 6, 18]


    def test_cumulative_product_empty():
        assert cumulative_product([]) == []


    @given(lists(integers()))
    def test_cumulative_product_starts_with_zero(values):
        array = [0] + list(values)
        assert cumulative_product(array) == [0] * len(array)

|
