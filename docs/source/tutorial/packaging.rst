.. _packaging:

Packaging
=========

When developing code to accomplish some goal, researchers will typically work within a single
script or even something like a Jupyter notebook. Often, the code written here will be useful in
another situation, by the same person, a collaborator, or a student. Frequently, that script or
notebook gets copied from place to place and edited as a matter of course. This can be problematic
for a number of reasons. And it can be a challenge to keep track of which version of the script
was used for what task.

Learning how to properly package your code in a way that others (or even yourself) can install
into one or more environments and used everywhere is powerful. Not only will it be easier to track
which version is needed for which project, but having a centralized location to collaborate on
that code makes it easier to manage and deploy those changes.

This section introduces a simple code example. We will discuss the anatomy of a Python package and
how Python looks for and deals with installed assets. Version control (i.e., `Git` and `GitHub`) and
managing deployed assets (e.g., deploying to `PyPI` with `Twine`) are not covered.


Starting Point
--------------

The following code snippet will be the starting point of this tutorial and developed on
throughout. It is entirely contrived and purposefully made to be both simple and initially "bad"
as a teaching aid.

Here we have an example bit of code written to compute the cumulative product of an array of
numeric values.

.. code-block:: python
    :caption: cumulative_product.py

    # original data
    array = [3, 4, 6, 9]

    # compute cumulative product
    result = array[:1]
    last_value = array[-1]
    for value in array[1:]:
        result.append(result[-1] * value)
        if value == last_value:
            break

    print(result)

There are of course many things that could be improved about this bit of code. We will get to
those soon enough! Let's just say for the sake of argument that it meets the needs of our use-case
initially. We've written this bit of code in a file somewhere and can execute it to display our
result.

.. code-block:: none

    $ python cumulative_product.py
    [3, 12, 72, 648]

|

.. note::

    Different kinds of code snippets and examples will be shown throughout the tutorial. Anything
    that looks like Python code should be interpreted as residing in a file. If it includes
    ``In[1]`` style markings that is to be executed at the IPython console. If it includes a ``$``
    prompt it represents an unspecified, generic shell prompt; these lines should be executed at
    the command-line.

    Examples:

    .. ipython:: python

        print('Hello, world!')

    .. code-block:: bash

        $ echo 'Hello, world!'
        Hello, world!

|


Functions
---------

The first thing to tackle here is how to make this code re-usable. We've hard-coded the input
data, and if we wanted to compute the cumulative product on more than one set of data we would
need to duplicate those lines of code each time.

Functions facilitate code reuse. Whenever you see yourself typing the same code twice in the same
program or project, it is a clear indication that the code belongs in a function.

A good function:

* has a descriptive name. ``cumulative_product`` is a better name than ``alg32``.
* is small -- no more than a couple of dozen lines -- and does **one** thing.
  If a function is doing too much, then it should probably be broken into smaller functions.
* can be easily tested -- more on this soon.
* is well documented -- more on this later.

.. code-block:: python
    :caption: cumulative_product.py

    def cumulative_product(array):
        result = array[:1]
        last_value = array[-1]
        for value in array[1:]:
            result.append(result[-1] * value)
            if value == last_value:
                break
        return result

    print(cumulative_product([3, 4, 6, 9]))
    print(cumulative_product([1, 8, 2, 7]))

Now we can do more work without duplicating those lines of code. But we're still hard coding the
input data. We'll explore making this function better in the next section when we discuss
:ref:`testing <testing>`. For now, let's focus on making this code available as part of an
installable package.


Creating a Python Package
-------------------------

In order make this code broadly available to Python, it needs to be "packaged" in a particular way
and "installed" into a particular location that Python knows where to find it. There are many
different types of files Python can import from and there is more than one location Python can
look for packages.

.. note::

    Before diving into the mechanics of Python packaging it is helpful to talk about terminology.
    When not accepting input directly via an interactive console, Python needs to find code in a
    file somewhere. In the simplest case we are speaking of a ``.py`` file. If we execute such a
    file directly (as we did just now) it is referred to as a `script`. If instead we want to
    import some code (either in an interactive session or within another file) it is typically
    referred to as a `module`. Python files can in fact be both a `script` and a `module`
    simultaneously, depending on context; more on this soon! A folder containing a collection of
    Python `modules` is a `package`. In order for that folder to be understood by Python as a
    `package` there are a few criteria, more on that in a minute. A `package` can in fact be a
    nesting of such folders (or `sub-packages`).


How does Python Find Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

What we want to be able to do is import our function as library code to use somewhere else.

.. code-block:: ipython

    In [4]: from cumulative_product import cumulative_product

    In [5]: cumulative_product([1, 2, 3])
    Out[5]: [1, 2, 6]

In this case, the ``cumulative_product.py`` file is acting as a `module` and we've imported a
function from it. Python will complain that there is no module named "cumulative_product" if it's
not found on one of the designated `paths` it knows about.

.. code-block:: ipython

    In [6]: import cumulative_product
    ---------------------------------------------------------------------------
    ModuleNotFoundError                       Traceback (most recent call last)
    <ipython-input-6-7f58dd7fb72e> in <module>
    ----> 1 import cumulative_product

    ModuleNotFoundError: No module named 'cumulative_product'

The notion of a "path" (and environment variables that can supplement them) is ubiquitous on most
platforms (including Windows) and used by many systems and tools. In Python, there are a few
pre-defined values that will show up on your `Python path`. You can view and manipulate these
paths by accessing the ``sys.path`` `list` from within a Python session or module.

.. code-block:: ipython

    In [2]: import sys

    In [3]: sys.path
    Out[3]:
    ['/usr/local/lib/python38.zip',
     '/usr/local/lib/python3.8',
     '/usr/local/lib/python3.8/lib-dynload',
     '',
     '/home/glentner/.local/lib/python3.8/site-packages',
     '/usr/local/lib/python3.8/site-packages']

The exact values depend on both how Python was installed and what platform you are using (i.e.,
Windows, MacOS, Linux, etc.). But there are some common patterns to observe. Your `system`
libraries will occur first on your path; that's the ``.zip``, top-level library, and
``lib-dynload`` you see (this will be slightly different on Windows). These represent Python
`itself` and the built-ins. Discussion of these is beyond the scope of this tutorial.

The final three paths are what's important here. The empty string represents your
`current working directory`. Python can always import from a module or package that exists within
your current working directory. Next are two `site-packages` directories which are essentially
fixed and represent the target for installed packages. By default, your `user` site packages folder
is first which allows you to install extra packages without needing write permissions to the
`system` path.

.. note::

    When using the word `system` we don't necessarily mean the Python installation used by the
    operating system. We mean the location where the Python you are invoking resides. If your
    Python installation is in your home directory, that is the `system` location.

Technically, we could create a special folder somewhere on our system and populate it with
``.py`` files and be able to import code from them by adding it to our Python path.

.. code-block:: ipython

    In [7]: sys.path.append('/opt/lab/python/modules')

    In [8]: import cumulative_product
    Out[8]: <module 'cumulative_product' from '/opt/lab/python/modules/cumulative_product.py'>

Alternatively, we could automate this by defining (or extending) the ``PYTHONPATH``
environment variable before launching a Python session or script.

.. code-block:: bash

    $ export PYTHONPATH=/opt/lab/python/modules:$PYTHONPATH

This isn't the best solution however because it requires access to a special location (`/opt/lab/python`)
to make use of the library. If we wanted to be able to use our algorithm in another project
without having to hard-code the location of the installed dependency `in the project`, we
should instead make it so our code is `installable` and automatically placed in the
appropriate location (wherever that happens to be).


Organizing a Python Project
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To make your module or package `installable` we will use
`setuptools <https://setuptools.readthedocs.io/en/latest/>`_.  There is a long
and storied history regarding the development tools used to package Python libraries.
We'll neglect that here and instead simply recommend the current "best practice".

The picture looks a little different if you are trying to make a single ``.py`` file
installable as a module. In either case we need a ``setup.py`` present at the top-level
of our project. The tooling and systems we will use expect a file with this exact name
to exist. Think of it as a configuration file.

.. code-block:: none

    $ tree .
    .
    ├── cumulative_product.py
    └── setup.py

In this case, a minimum viable setup file would look something like the following.

.. code-block:: python
    :caption: setup.py

    from setuptools import setup

    setup(
        name='cumulative_product',
        version='0.0.1',
        py_modules=['cumulative_product']
    )

For a small number of functions this approach is fine, and even recommended, but as the
size and scope of the project grows, it will become necessary to organize the code across
multiple files. Let's assume this to be the case from the outset and restructure our
project. We'll use the name ``python201`` for the purposes of this tutorial, but your
package of course should take on a name relevant to the project.

.. code-block:: none

    $ tree .
    .
    ├── python201/
    │   ├── __init__.py
    │   └── algorithms.py
    └── setup.py

Notice the presence of the ``__init__.py`` file. A detail neglected until this point,
the existence of a file with this special name is what defines a folder as a `package`.
This file must be present throughout the package/sub-package hierarchy at every level.
An entire tutorial could be devoted to the purpose and use of these modules.
Suffice it to say these files can literally be empty.

Now our import would look like the following.

.. code-block:: ipython

    In [1]: from python201.algorithms import cumulative_product

    In [2]: cumulative_product([1, 2, 3])
    Out[2]: [1, 2, 6]

Our setup file would then instead need to be the following.

.. code-block:: python
    :caption: setup.py

    from setuptools import setup

    setup(
        name='python201',
        version='0.0.1',
        packages=['python201']
    )

The ``packages`` keyword argument is similarly a list of strings, but now representing packages
(and any sub-packages therein). The modules below a package will automatically be included, but
sub-packages will not. To automatically enumerate our package structure should we choose to expand
our project, we can use a handy tool included in ``setuptools`` that does exactly what it sounds
like.

.. code-block:: python
    :caption: setup.py

    from setuptools import setup, find_packages

    setup(
        name='python201',
        version='0.0.1',
        packages=find_packages()
    )



Installation
^^^^^^^^^^^^

To install a Python package we will use the command line tool, ``pip``, which is typically
included out-of-the-box with any Python installation. You are likely familiar with the use
of ``pip`` to install packages from Python's online package index, `PyPI <https://pypi.org>`_.
There are in fact numerous types of targets that can be specified to ``pip``, including
local source code repositories you have on your system, such as ours.

.. code-block:: none

    $ pip install .

Here the `dot` represents the current working directory. In practice, you can point to
any folder path that contains a ``setup.py`` file. This will install our package to the
`system` site-packages path. To install to our `user` site-packages, we can include the
``--user`` flag.

.. code-block:: none

    $ pip install . --user

Finally, an often used feature of developers is to install your package in `editable`
mode using the ``-e`` flag. This allows you to work on the code and see the changes
without needing to re-install it every time.

.. code-block:: none

    $ pip install -e . --user


Extras
------

We've arrived now at the conclusion of the essentials for our package. Here are some extra
things that you might want to consider for your project, particularly if you plan on sharing
it with others.

README
^^^^^^

A staple of open-source projects, a `README` file is a plain text file included in your
project that explains what is included in the project and typically some guidance on
how to use it. Many online hosting services including `PyPI` itself understand what these
files are and will render them in different formats.

.. code-block:: rst
    :caption: README.rst

    python201
    =========

    A Python package for numerical algorithms.


Version Control
^^^^^^^^^^^^^^^

Even if you plan to work on the project alone, you definitely should consider developing
your code using some kind of version control system. These days, ``git`` is ubiquitous.
If you'll be sharing the code, online hosting services such as `github.com <https://github.com>`_
and `gitlab.com <https://gitlab.com>`_ offer sophisticated features.


License
^^^^^^^

You should pick a software license that best suites your project. A license specifies the
terms of use of the code. `Choosing a license <https://choosealicense.com>`_ is beyond the scope
of this tutorial. Once you've decided on an appropriate license, most commonly used licenses
are recognized by hosting services like `PyPI` and `github.com`.

You should include the license in full in a ``LICENSE`` file at the top-level of your project.
It may be appropriate to include a brief snippet pertaining to the license at the top of some
or all of your code files.

.. code-block:: none

    $ tree .
    .
    ├── LICENSE
    ├── python201/
    │   ├── __init__.py
    │   └── algorithms.py
    ├── README.rst
    └── setup.py

It doesn't affect the installed package, but if you plan to upload your package to `PyPI`
you can define the license within the setup function using the appropriate name and
`classifier`.

.. code-block:: python
    :caption: setup.py

    from setuptools import setup, find_packages

    setup(
        name='python201',
        version='0.0.1',
        license='Apache Software License',
        classifiers=[
            'License :: OSI Approved :: Apache Software License'
        ],
        packages=find_packages()
    )

More Details
^^^^^^^^^^^^

There are `many` options one can and may need to use within the `setup` function
to make a package function as desired, such as dependencies, non-python installed assets (such as
data files or man pages), etc. You also should consider including additional information
if you plan to upload your package to the package index.

.. code-block:: python
    :caption: setup.py

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
    )


Upload to PyPI
^^^^^^^^^^^^^^

You can validate, register, and upload your package to the Python package index using the
`Twine <https://twine.readthedocs.io/en/latest/>`_ command line tool. This is the officially
supported way of doing so. It's perfectly accepted to `not` host your package via `PyPI`, and
instead merely instruct users how to install directly via GitHub, for example.


|
