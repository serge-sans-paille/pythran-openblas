pythran-openblas
================

This repo provides an automatic way to generate OpenBLAS wheels for Linux, OSX and Windows, thanks to Appveyor and Travis-CI.
These wheels can be used by `pythran <https://github.com/serge-sans-paille/pythran/>`_ users to make installation of BLAS dependency easier when using pip.

The wheels provide **static archive** of OpenBLAS, and a dummy package with a few informations:


>>> import pythran_openblas as openblas
>>> openblas.static_library
libopenblas.a
>>> openblas.include_dirs
/I/like/to/move/it/include/openblas
>>> openblas.library_dir
/I/like/to/move/it/lib



For information on OpenBLAS, please consult https://www.openblas.net/
