#!/bin/bash
set -e -x

#targets="/opt/python/cp27-cp27mu/bin /opt/python/cp27-cp27m/bin /opt/python/cp36-cp36m/bin/ /opt/python/cp37-cp37m/bin/"
targets="/opt/python/$1/bin"

# Compile wheels
for PYBIN in $targets
do
    "${PYBIN}/pip" install cmake
    PATH=$("${PYBIN}/python" -c 'import sys, os; print(os.path.dirname(sys.executable))'):$PATH "${PYBIN}/pip" wheel /io/ -w /io/wheelhouse/
done

find /io/wheelhouse/

# Install packages and test
for PYBIN in $targets
do
    "${PYBIN}/pip" install pythran-openblas --no-index -f /io/wheelhouse
done
