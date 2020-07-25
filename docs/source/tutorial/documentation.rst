.. _documentation:

Documentation
=============

Most people think of writing documentation as an unpleasant, but necessary task, done for the
benefit of other people with no real benefit to themselves. So they choose not to do it, or they
do it with little care.

But even if you are the only person who will ever use your code, it's still a good idea to
document it well. Being able to document your own code gives you confidence that you understand it
yourself, and a sign of well-written code is that it can be easily documented. Code you wrote a
few weeks ago may as well have been written by someone else, and you will be glad that you
documented it.

The good news is that writing documentation can be fun, and you really don't need to write a lot
of it.


Docstrings and Comments
-----------------------

Documentation is *not* comments.

A *docstring* in Python is a string literal that appears at the beginning of a module, function,
class, or method.

.. code-block:: python

   """
   A docstring in Python that appears
   at the beginning of a module, function, class or method.
   """

Let's add a trivial docstring to our code.

.. code-block:: python
    :caption: python201/algorithms.py

    def cumulative_product(array):
        """
        Compute the cumulative product of an array of numbers.
        """
        result = list(array).copy()
        for i, value in enumerate(array[1:]):
            result[i+1] = result[i] * value
        return result

The *docstring* of a module, function, class or method becomes the ``__doc__`` attribute of that
object, and is printed if you type ``help(object)``:

.. code-block:: ipython

    In [1]: from python201.algorithms import cumulative_product

    In [2]: help(cumulative_product)

    Help on function cumulative_product in module python201.algorithms:

    cumulative_product(array)
        Compute the cumulative product of an array of numbers.

A *comment* in Python is any line that begins with a ``#``:

.. code-block:: python

   # a comment.

The purpose of a docstring is to document a module, function, class, or method.
The purpose of a comment is to explain a very difficult piece of code,
or to justify a choice that was made while writing it.

Docstrings should not be used in place of comments, or vice versa.
**Don't do the following**:

.. code-block:: python
    :caption: python201/algorithms.py

    def cumulative_product(array):
        # Compute the cumulative product of an array of numbers.
        result = list(array).copy()
        for i, value in enumerate(array[1:]):
            result[i+1] = result[i] * value
        return result


Deleting code
^^^^^^^^^^^^^

Incidentally, many people use comments and string literals
as a way of "deleting" code - also known as *commenting out* code.
See `this article <https://nedbatchelder.com/text/deleting-code.html>`_
on a better way to delete code.


What to document?
-----------------

So what goes in a docstring?

At minimum, the docstring for a function or method should consist of the following:

1. A **Summary** section that describes in a sentence or two
   what the function does.
2. A **Parameters** section that provides a
   description of the parameters to the function,
   their types,
   and default values (in the case of optional arguments).
3. A **Returns** section that similarly describes the return values.
4. Optionally,
   a **Notes** section that describes the implementation,
   and includes references.

Let's add some more information to our docstring.

.. code-block:: python
    :caption: python201/algorithms.py

    def cumulative_product(array):
        """
        Compute the cumulative product of an array of numbers.

        Parameters:
            array (list): An array of numeric values.

        Returns:
            result (list): A list of the same shape as `array`.
        """
        result = list(array).copy()
        for i, value in enumerate(array[1:]):
            result[i+1] = result[i] * value
        return result

Here we've followed a particular style guide; Sphinx uses `Google's documentation guidelines
<https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html>`_ by default to parse
your docstrings, more on this later! NumPy's `documentation guidelines
<https://numpydoc.readthedocs.io/en/latest/>`_ are also a great reference for more information
about what and how to document your code. There are other style guides you might prefer.


Doctests
--------

In addition to the sections above, your documentation can also contain runnable tests. This is
possible using the `doctest <https://docs.python.org/3/library/doctest.html>`_ module. Include a
section of examples in the following format and ``pytest`` will discover and validate that the
expected output is indeed generated.

.. code-block:: python
    :caption: python201/algorithms.py

    def cumulative_product(array):
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
        result = list(array).copy()
        for i, value in enumerate(array[1:]):
            result[i+1] = result[i] * value
        return result

You can tell ``pytest`` to run doctests as well as other tests
using the ``--doctest-modules`` switch:

.. code-block:: none

    $ pytest --doctest-modules python201/algorithms.py
    ================================== test session starts ===================================
    platform linux -- Python 3.8.3, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
    rootdir: /home/glentner/code/github.com/glentner/python201
    plugins: hypothesis-5.20.3
    collected 1 item

    python201/algorithms.py .                                                          [100%]

    =================================== 1 passed in 0.02s ====================================

.. note::

    *Doctests* are great because they double up as documentation as well as tests. But they
    shouldn't be the *only* kind of tests you write.


Documentation-Driven Development
--------------------------------

In a similar manner in which `Test-driven Development` (TDD) forces you to think clearly about how
the feature you intend to develop should behave, so to does `Documentation-driven Development`
(DDD).

The idea is as follows, you must first be able to describe what the thing does before you can
build the thing that does it. In this way, documentation-driven development `precedes` test-driven
development. Think of writing your docstrings first as a sort of planning phase. Once you've
sorted out the documentation, write the tests that it should pass; then and only then, write the
implementation.

.. note::

    We have of course gone in precisely the wrong order in this tutorial, but its a
    tutorial so we'll make an exception for the our sake.


Extras
------

Automatic Documentation Generation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Finally, you can turn your documentation into a beautiful website (like this one!),
a PDF manual, and various other formats, using a document generator such as `Sphinx
<http://www.sphinx-doc.org/en/master/>`_.

Sphinx
++++++

For a Python project like this, it is common practice to have a ``docs`` folder at the top level
of your project with the source to a Sphinx website. We won't include a complete guide to using
Sphinx here; there are many such guides online.

To get started, create the directory and run the ``sphinx-quickstart`` command from `inside`
the directory. There are a few options it will ask you about.

.. code-block:: none

    $ mkdir docs
    $ cd docs
    $ sphinx-quickstart

Depending on how you answered the prompts from the quickstart command you will have a new source
tree with an ``index.rst`` and ``conf.py`` file. The `build` directory will either be within this
same folder as ``_build`` or you will have explicit, adjacent ``source`` and ``build``
directories. Either setup is fine, I prefer to have them separate.

The ``conf.py`` file is your Sphinx configuration for the project and it contains essential,
high-level information (e.g., the name and version number for your project, copyright information,
etc.), as well as detailed options that may be specific to the `theme` you are using. Typically,
Sphinx themes are easily installable as Pip modules, and need merely to be assigned in
``conf.py``. We're using the
`pydata_sphinx_theme <https://github.com/pandas-dev/pydata-sphinx-theme>`_.

The pages for your documentation are `restructured text` files (kind of like `markdown`), and the
top-level ``index.rst`` (as well as within any folder) behave just as an ``index.html`` page
would.

To build your documentation, use the provided ``Makefile`` (or ``make.bat`` on Windows).

.. code-block:: none

    $ make html

Sphinx doesn't just create html. The whole point of Sphinx is that you create layers of content
files that you can build into multiple formats, include HTML, PDF, man pages, etc.

The nice thing about using Sphinx with Python is that it `knows` about Python docstrings.
We'll neglect a full exposition here, but to illustrate the point, documenting the API
for your project could quite literally be as simple as creating an ``api.rst`` page
with something like the following.

.. code-block:: rst
    :caption: docs/source/api.rst

    API
    ===

    .. automodule:: python201
        :members:

    :mod:`python201.algorithms`
    ---------------------------

    .. automodule:: python201.algorithms
        :members:

If we maintain a certain style in our docstrings as described here, now we only need to
manage a single copy of the documentation! Sphinx can pull out and format our docstrings
into a fully functioning website!

.. note::

    This kind of special functionality and other features like it are often provided as a builtin
    or third party `extension`, in this case we are using the builtin ``sphinx.ext.autodoc``
    extension. You can simple add these to the list of extensions activated in your ``conf.py``.


Hosting
+++++++

If you put your project under version control, typically using ``git``, and host it online using a
provider (such as `github.com <https://github.com>`_, you can use git `hooks` to automatically
trigger an update to a website. Basically, services can register themselves with your repository
and when a particular event occurs (like a `push` to the `master` branch), they'll take some
action (like `pull` to update the docs and update the website).

This tutorial is hosted using `Github Pages`. In the settings to the repository on GitHub I have
it pointing to my ``docs`` folder with some additional necessary bits to tell GitHub what lives
where. When I `push` changes to GitHub it automatically syncs the contents of my ``docs/build``
directory.

Many open-source projects like to use `readthedocs.org <https://readthedocs.org>`_, especially for
Python projects. You can create an account and authenticate with GitHub, point to your repository,
and follow some simple setup procedures. Not only will it host your Sphinx documentation, it will
`build` it for you!

Type Annotations
^^^^^^^^^^^^^^^^

A relatively new concept in Python,
`type annotations <https://docs.python.org/3/library/typing.html>`_ are a powerful new feature that
let you be more precise about your intentions with code. Many of the tools we rely on to develop
code have support for using type annotations to help you catch bugs before you even get
to your unit tests.

A trivial example might be as follows.

.. code-block:: python

    def greeting(name: str) -> str:
        return 'Hello ' + name

Here we're saying that ``name`` should be type ``str`` and that ``greeting`` also returns a
``str``. The topic of type annotations can unveil some deep philosophical questions about how to
write Python code, or even what it means for code to be `Pythonic`. We won't crack that `egg` (pun
intended) open here, but type annotations are an officially supported part of the language and
with tooling like we'll point out next, it let's you take the weight of type checking off of
run-time code and leave it to `development`-time(?) code.

The `mypy <http://mypy-lang.org>`_ project provides static type checking to your project using these
type annotations. Editors like `PyCharm` will alert you if you use a method in a way that doesn't
conform to the annotations provided.

Type annotations in Python, in a sense, are part of `documentation-driven development`. If you cannot
annotate your code, perhaps you should reconsider its design. And you will thank yourself later when
trying to use your own code.

.. note::

    Type annotations currently are not (and may never be) "real code". That is, it is not in fact
    an error to provide an argument that doesn't conform to the given type annotation.

We can add annotations to our code as follows.

.. code-block:: python
    :caption: python201/algorithms.py

    from typing import List

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
        result = list(array).copy()
        for i, value in enumerate(array[1:]):
            result[i+1] = result[i] * value
        return result

.. note::

    Using type ``float`` in this instance is actually sufficient to annotate as a generic numeric
    type.

    From `PEP 484 <https://www.python.org/dev/peps/pep-0484/#id27>`_:

    *Rather than requiring that users write import numbers and then use numbers.Float etc.,
    this PEP proposes a straightforward shortcut that is almost as effective: when an argument is
    annotated as having type float, an argument of type int is acceptable...*

|
