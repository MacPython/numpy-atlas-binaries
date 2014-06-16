echo "python $PYTHON"
which $PYTHON

echo "pip $PIP"
which $PIP

PYTHON_TEST="$ARCH $PYTHON"

# Return code
RET=0

echo "sanity checks"
$PYTHON -c "import sys; print('\n'.join(sys.path))"
if [ $? -ne 0 ] ; then RET=1; fi
RET=`expr $RET + $?`
for pkg in numpy scipy
do
    $PYTHON -c "import ${pkg}; print(${pkg}.__version__, ${pkg}.__file__)"
    if [ $? -ne 0 ] ; then RET=1; fi
done

echo "unit tests"
for pkg in numpy scipy
do
    $PYTHON_TEST -c "import sys; import ${pkg}; sys.exit(not ${pkg}.test().wasSuccessful())"
    if [ $? -ne 0 ] ; then RET=1; fi
done

echo "done testing numpy, scipy stack"

# Set the return code
(exit $RET)

