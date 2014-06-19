![travis build result](https://travis-ci.org/matthew-brett/numpy-atlas-binaries.svg?branch=master "travis-ci build result")

# Build machinery for numpy / scipy ATLAS binaries

Numpy and scipy need BLAS and LAPACK libraries for fast matrix and vector
computation.

OSX provides a standard library for these called Accelerate, that is present
on every OSX machine at `/System/Library/Frameworks/Accelerate.framework`.

Normally we link numpy and scipy against the Accelerate framework in OSX on
the basis that it is fast, usually reliable, and we don't have to build it.

## Problems with Accelerate

At the moment (June 2014) we have two problems with Accelerate:

### Segfault for float32

We are getting a segfault in recent OSX Accelerate with float32 values not
aligned to 32-byte boundaries:

- https://github.com/numpy/numpy/issues/4007
- http://www.openradar.me/radar?id=5864367807528960

### Errors using multiprocessing

Accelerate also doesn't play well with multiprocessing in Pythons before 3.4:

- https://github.com/numpy/numpy/issues/4776
- http://mail.scipy.org/pipermail/numpy-discussion/2012-August/063589.html

## Other options

- [ATLAS](http://math-atlas.sourceforge.net)
- [OpenBLAS](http://www.openblas.net)

Of these two, ATLAS is the more stable.

Building numpy with OpenBLAS in June 2014 was giving me a [test
error](https://github.com/numpy/numpy/issues/4007#issuecomment-44901713)

## Building with ATLAS

Now the details:

### Dual architecture

A binary installer should work for as many Pythons as possible. In particular
it should work for the Python.org installer which is a standard default.

- Python.org provides a dual i386 / x86\_64 build
- It advertises itself thus with its platform information; `python -c "import
  distutils.util; print(distutils.util.get_platform())"` gives `macosx-10.6-intel`, where `intel` means a combined i386 / x86\_64 binary.
- A compatible binary installer, such as a wheel, should therefore also be a
  combined i386 / x86\_64 build

### Build process

#### Compilers

I need gcc and gfortran compilers to build ATLAS and scipy.

I chose gcc / gfortran 4.8.2 from (at the time)
https://gcc.gnu.org/wiki/GFortranBinaries#MacOS

I've put the binary I used in this repo at https://github.com/matthew-brett/numpy-atlas-binaries/tree/master/archives to make sure the builds are reproducible.

Another option I could have used was the default Apple gcc 4.2.  This [uses
clang as a
backend](https://support.enthought.com/entries/26184115-GCC-Clang-and-Cython-in-OS-X-10-9-Mavericks)

clang still seems to be slower than modern gcc - see:
http://openbenchmarking.org/result/1204215-SU-LLVMCLANG23

With clang, I'd still need a gfortran compiler, maybe the [default suggested on
the scipy website](http://www.scipy.org/scipylib/building/macosx.html) hosted
on CRAN.  This is currently very old - version 4.2.3.

The clang / CRAN gfortran combination has the advantage that they do dual
architecture compilation.  That is if you pass `-arch i386 -arch x86_64` then
these compilers will compile 32 bit and 64 bit binaries and fuse them so that
a 32 bit or 64 bit program can link against them.

Instead, I bravely went for modern gcc, knowing that I would have to take care
of the i386 / x86\_64 dual architecture problem by hand.

#### ATLAS

The ATLAS build is fairly straightforward once you know what you're doing, but
it's impractical to farm out to virtual machines because:

- it relies on having nearly complete use of the machine CPUs in order to
  test timing of candidate routines
- anything but a build with known architecture ("architectural defaults" in
  ATLAS parlance) takes about 6 hours even on a fast machine.

I've therefore built ATLAS on my laptop with CPU throttling turned off as far
as I could, and no other significant processes running.

I build 32 and 64 bit ATLAS binaries separately.  The resulting built ATLAS
libraries are in [the repo archives
directory](https://github.com/matthew-brett/numpy-atlas-binaries/tree/master/archives).
The scripts I used to build them are here: [32
bit](https://github.com/matthew-brett/numpy-atlas-binaries/blob/master/scripts/install_atlas_32_sse2.sh)
; [64
bit](https://github.com/matthew-brett/numpy-atlas-binaries/blob/master/scripts/install_atlas_64_sse2.sh).

These archives are linked against gfortran libs specific to this build of the
compiler.

The default ATLAS build builds static libraries only.  The build process makes
dynamic libraries from the static libraries, for numpy and scipy to link
against.

#### Building Numpy and scipy

This is just a sketch.  The full build process is in the waf
`wscript` in the repository.

- for each architecture (i386, x86\_64)
    - make new ATLAS directory for arch in build directory; copy ATLAS include
      directory into new directory; make dynamic ATLAS libs using [this
      script](https://github.com/matthew-brett/numpy-atlas-binaries/blob/master/bin/make_shared_atlas.py)
      and copy into `lib` sub-directory in new ATLAS directory.
    - copy numpy / scipy sources to new directory
    - if building scipy, build numpy with recorded back-compatibility tag to
      build against
    - use ATLAS environment variable to point numpy / scipy at ATLAS binaries
      with matching architecture
    - Compile with crafted compile / link flags to remove default `arch` flags
      and add specific architecture flags.  This gives an
      architecture-specific wheel
    - use `delocate` and `delocate-wheel` to copy required dynamic libraries
      into the built wheel
- Fuse the architecture specific wheels into one combined architecture wheel
  using `lipo -create` command via `delocate-fuse`.

I run this process for numpy / scipy using a command like this:

    workon py27 # use python virtualenv
    python waf distclean configure build cp_wheels --wheel-dir ~/wheelhouse

where `py27` is a virtualenv for Python 2.7.  Repeat using virtualenvs for
Pythons 3.3 and 3.4.  `cp_wheels` copies the fused build wheels into a
directory `~/wheelhouse` (given with the `--wheel-dir` option).

#### Automated build / test of numpy / scipy on Travis-CI

I've set these builds to run on [travis-ci](http://travis-ci.org) - see the
[travis builds
page](https://travis-ci.org/matthew-brett/numpy-atlas-binaries).

The builds upload the binaries to a [Rackspace hosted
container](http://a365fff413fe338398b6-1c8a9b3114517dc5fe17b7c3f8c63a43.r19.cf2.rackcdn.com)
(thanks to Olivier Grisel and Rackspace for setting up access).

#### To do

- Maybe iterate over Python.org versions in the build process rather than
  doing it by hand on the command line, as above.
