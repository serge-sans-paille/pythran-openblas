python-openblas-build
================

This repo provides an automatic way to generate OpenBLAS wheels for Linux, OSX and Windows, thanks to Appveyor and Travis-CI.

The wheels provide **static archive** of OpenBLAS, and a dummy package with a few informations:

.. code-block:: python

    >>> import python_openblas_build as openblas
    >>> openblas.static_library
    libopenblas.a
    >>> openblas.include_dirs
    /I/like/to/move/it/include/openblas
    >>> openblas.library_dir
    /I/like/to/move/it/lib


For information on OpenBLAS, please consult https://www.openblas.net/
