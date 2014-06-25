echo "Python on path: `which python`"
echo "Python cmd: $PYTHON_EXE"

echo "pip on path: `which pip`"
echo "pip cmd: $PIP_CMD"

WHEELHOUSE=$PWD/../build/wheelhouse
$PIP_CMD install nose

# Return code
RET=0

echo "sanity checks"
$PYTHON_EXE -c "import sys; print('\n'.join(sys.path))"
if [ $? -ne 0 ] ; then RET=1; fi

function simple_import {
    pkg=$1
    $PYTHON_EXE -c "import ${pkg}; print(${pkg}.__version__, ${pkg}.__file__)"
    if [ $? -ne 0 ] ; then RET=1; fi
}

function unit_test {
    pkg=$1
    arch=$2
    test_str="import sys; import ${pkg}; sys.exit(not ${pkg}.test(verbose=0).wasSuccessful())"
    arch $arch $PYTHON_EXE -c "$test_str"
    if [ $? -ne 0 ] ; then RET=1; fi
}

echo "unit tests"
if [[ $PACKAGES =~ "scipy" ]]; then
    if [ -n "$UPGRADE_NP" ]; then
        $PIP_CMD install --upgrade numpy
    fi
    # Install scipy from wheel
    $PIP_CMD install $WHEELHOUSE/scipy*.whl
    simple_import numpy
    simple_import scipy
    unit_test scipy -x86_64
    # If we're going to test with new numpy later, skip i386 tests to save
    # time, otherwise travis will time out (50 minute cutoff)
    if [[ ! $PACKAGES =~ "numpy" ]]; then
        unit_test scipy -i386
    fi
fi
if [[ $PACKAGES =~ "numpy" ]]; then
    $PIP_CMD install $WHEELHOUSE/numpy*.whl
    simple_import numpy
    unit_test numpy -x86_64
    unit_test numpy -i386
    if [[ $PACKAGES =~ "scipy" ]]; then
        simple_import scipy
        unit_test scipy -x86_64
        unit_test scipy -i386
    fi
fi

echo "done testing numpy, scipy"

# Set the return code
(exit $RET)
