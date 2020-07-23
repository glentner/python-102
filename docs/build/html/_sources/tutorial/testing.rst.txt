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

   | "*Tests are the dental floss of development: everyone knows they should do it more,*
   | *but they don’t, and they feel guilty about it.*"
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

While we were developing this function, we would have likely started up an IPython console
and either copied the code snippet or imported the function and tested it on a
few simple cases to validate that it returns expected results.

.. code-block:: ipython

    In [1]: from python201.algorithms import cumulative_product

    In [2]: cumulative_product([1, 2, 3])
    Out[2]: [1, 2, 6]

    In [3]: cumulative_product([3, 2, 1])
    Out[3]: [3, 6, 6]

    In [4]: cumulative_product([1, 2, 3, 4])
    Out[4]: [1, 2, 6, 24]

While this kind of testing is better than not doing any testing at all, it leaves much
to be desired. First, it needs to be done each time ``cumulative_product`` is changed.
It also requires that we manually inspect the output from each test to decide if the
code "passes" or "fails" that test. Further, we need to remember all the tests we came
up with today if we want to test again tomorrow.


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

We want all of our tests to live under files that start with ``test`` and we need all of
our tests to be encapsulated by functions that also start with ``test``.

.. code-block:: python
    :caption: tests/test_algorithms.py

    from python201.algorithms import cumulative_product

    def test_cumulative_product():
        assert cumulative_product([1, 2, 3]) == [1, 2, 6]
        assert cumulative_product([3, 2, 1]) == [3, 6, 6]
        assert cumulative_product([1, 2, 3, 4]) == [1, 2, 6, 24]
        assert cumulative_product([1, 2, 3, 3]) == [1, 2, 6, 18]

To run our tests, we simple execute ``pytest`` at the command line at the top of our
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


Useful Tests
------------

...


Fixing the Code
---------------

...


Types of Testing
----------------

...


Test-Driven Development
-----------------------

...


Growing a Useful Test Suite
---------------------------

...

|
