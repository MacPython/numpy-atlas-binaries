echo "python"
which python

echo "pip"
which pip

PYTHON=python
PIP=pip
WHEELHOUSE=$PWD/../build/wheelhouse
pip install nose

# Return code
RET=0

echo "sanity checks"
$PYTHON -c "import sys; print('\n'.join(sys.path))"
if [ $? -ne 0 ] ; then RET=1; fi

function simple_import {
    pkg=$1
    $PYTHON -c "import ${pkg}; print(${pkg}.__version__, ${pkg}.__file__)"
    if [ $? -ne 0 ] ; then RET=1; fi
}

function unit_test {
    pkg=$1
    test_str="import sys; import ${pkg}; sys.exit(not ${pkg}.test(verbose=0).wasSuccessful())"
    $PYTHON -c "$test_str"
    if [ $? -ne 0 ] ; then RET=1; fi
    arch -i386 $PYTHON -c "$test_str"
    if [ $? -ne 0 ] ; then RET=1; fi
}

echo "unit tests"
if [[ $PACKAGES =~ "scipy" ]]; then
    # Install scipy from wheel
    $PIP install $WHEELHOUSE/scipy*.whl
    simple_import numpy
    simple_import scipy
    unit_test scipy
fi
if [[ $PACKAGES =~ "numpy" ]]; then
    $PIP install $WHEELHOUSE/numpy*.whl
    simple_import numpy
    unit_test numpy
    if [[ $PACKAGES =~ "scipy" ]]; then
        simple_import scipy
        unit_test scipy
    fi
fi

echo "done testing numpy, scipy"

# Set the return code
(exit $RET)

