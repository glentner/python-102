.. _tutorial:

Tutorial
========

The following sections outline some important topics in well managed, robust scientific software.
These topics are not the *only* thing that one could include in such a list, but they are common
ones.

The implementations here are Python specific: the packaging, *pytest* for testing, *sphinx* for
documentation, etc. But the notion of these topics are universal. You should use conventional
packaging methods for the language you're using. You should be automating your tests. You should
have well managed documentation. Your command-line interfaces and logging behavior should follow
established conventions. You should benchmark and profile the performance and memory footprint of
your code.

These things will not make your scientific software correct. But doing these things are a big part
of making your scientific software easy to use and easy to maintain.

|


.. toctree::

    packaging
    testing
    documentation
    commandline
    logging
    performance

