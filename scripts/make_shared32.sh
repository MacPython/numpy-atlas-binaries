# cd ~/archives/atlas/3.10.1-64-sse2/lib2
mkdir lib2
cd lib2
cp ../lib/*.a .
GCC="gcc -m32"
$GCC -shared -fpic -o libatlas.dylib -all_load libatlas.a -install_name $PWD/libatlas.dylib
otool -L libatlas.dylib
$GCC -shared -fpic -o libcblas.dylib -latlas -all_load libcblas.a -install_name $PWD/libcblas.dylib
otool -L libcblas.dylib
$GCC -shared -fpic -o libf77blas.dylib -latlas -lgfortran -all_load libf77blas.a -install_name $PWD/libf77blas.dylib
otool -L libf77blas.dylib
$GCC -shared -fpic -o liblapack.dylib -latlas -lf77blas -lcblas -lgfortran -all_load liblapack.a -install_name $PWD/liblapack.dylib
otool -L liblapack.dylib
rm -rf *.a
