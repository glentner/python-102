.. _setup:

Setup
=====

The methods and code presented in the tutorial are at a basic level. The point of the tutorial is
to teach core concepts to building better scientific software in Python and is not specific to any
operating system, Python distribution, or tool set. Almost without exception, Linux is the
operating system of choice in a scientific context, whether that's in high performance computing
(HPC), the cloud, or a research lab. Nevertheless, nothing presented here is necessarily
restricted to Linux systems.


Python Environment
------------------

The expectation is that you already know what Python *is* and how to use it on your system. This
means that you have Python itself installed in some fashion, and that you understand how to
execute Python code both interactively and as a script.

We strongly recommend that you create some form of isolated environment to install the packages
used for this tutorial and to play with creating your own packages without influencing other
Python installations you may have on your system. If you are unsure of how to do this, we
recommend creating an `Anaconda <https://www.anaconda.com/products/individual>`_ environment.
Alternatively, as is done for the development of this project, you can create a virtual
environment with `Pipenv <https://pipenv.pypa.io/en/latest>`_.



Developer Tools
---------------

For this tutorial you will need to edit code files and then to execute code in various ways in a
shell (i.e., from the command line). No preference is advocated for here on what applications
should be used as it really is a matter of preference.

A terminal emulator of some fashion is needed. On Windows this can be the built in `CMD` prompt,
the new `Windows Terminal`, `Cmder`; or other modern, cross-platform ones such as `Hyper` and
`Alacritty`. For Linux, BSD (e.g., MacOS), or other Unix-like operating systems there is likely a
built-in terminal emulator or some enumerable ones available from the package manager or online.
No shell in particular is required either. Though most folks are familiar to Bash, the native CMD
prompt on Windows is fine, or any other shell for that matter; as long as you can execute
``python`` and/or ``ipython`` directly it will work.

On many systems, from the terminal, you can launch a command line based text editor, such as `Vim`
or `Nano`. If that's your jam, no other software is necessary.

Otherwise, you'll also need a text editor. Some text editors are very simple, others are very
sophisticated. Many even have a terminal built in to the tool with deep integrations. For Python
development, here is a brief list of modern, cross-platform text editors that provide rich
integrations and features.

In no particular order:

- `Visual Studio Code <https://code.visualstudio.com>`_
- `Atom <https://atom.io>`_
- `PyCharm <https://www.jetbrains.com/pycharm/>`_

|
