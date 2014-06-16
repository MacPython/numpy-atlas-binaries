echo "python"
which python

echo "pip"
which pip

PYTHON=python
PIP=pip
WHEELHOUSE=$PWD/../build/wheelhouse
pip install nose

# Install scipy from wheel
$PIP install $WHEELHOUSE/scipy*.whl

# Return code
RET=0

echo "sanity checks"
$PYTHON -c "import sys; print('\n'.join(sys.path))"
if [ $? -ne 0 ] ; then RET=1; fi

function simple_import {
    for pkg in numpy scipy
    do
        $PYTHON -c "import ${pkg}; print(${pkg}.__version__, ${pkg}.__file__)"
        if [ $? -ne 0 ] ; then RET=1; fi
    done
}

function unit_test {
    pkg=$1
    test_str="import sys; import ${pkg}; sys.exit(not ${pkg}.test().wasSuccessful())"
    $PYTHON -c "$test_str"
    if [ $? -ne 0 ] ; then RET=1; fi
    arch -i386 $PYTHON -c "$test_str"
    if [ $? -ne 0 ] ; then RET=1; fi
}

echo "unit tests"
unit_test scipy
$PIP install $WHEELHOUSE/numpy*.whl
unit_test numpy
unit_test scipy

echo "done testing numpy, scipy"

# Set the return code
(exit $RET)

