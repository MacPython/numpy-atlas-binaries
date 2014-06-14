""" Make shared ATLAS libraries from static libs

Assumes an INPUT directory into which ATLAS has been 'install'ed

This directory will have a `lib` and `include` directory.

Makes new directory with given name with:

* Copy of <INPUT>/include with include files
* <INPUT>/lib with dynamic libraries corresponding to .a files.
"""
from __future__ import print_function

import sys
import os
from os.path import (join as pjoin, split as psplit, abspath, dirname,
                     realpath, expanduser)
import shutil
from glob import glob

from delocate.tools import get_archs, back_tick


def main():
    try:
        static_root = sys.argv[1]
    except IndexError:
        raise RuntimeError("Need ATLAS input directory")
    try:
        dynamic_root = sys.argv[2]
    except IndexError:
        raise RuntimeError("Need ATLAS output directory")
    static_root = realpath(expanduser(static_root))
    static_libdir = pjoin(static_root, 'lib')
    static_libs = glob(pjoin(static_libdir, '*.a'))
    if len(static_libs) == 0:
        raise RuntimeError("No static libs in " + static_libdir)
    prev_archs = None
    for lib in static_libs:
        archs = get_archs(lib)
        if len(archs) != 1:
            raise RuntimeError("Oops, not just one arch in " + lib)
        if not prev_archs is None and not prev_archs == archs:
            raise RuntimeError("Oops, differing archs in libs")
        prev_archs = archs
    arch = archs.pop()
    if arch not in ('i386', 'x86_64'):
        raise ValueError("Only know i386, x86_64, not " + arch)
    dynamic_root = realpath(expanduser(dynamic_root))
    shutil.copytree(pjoin(static_root, 'include'),
                    pjoin(dynamic_root, 'include'))
    m_flag = '-m32' if arch == 'i386' else '-m64'
    dyn_libdir = pjoin(dynamic_root, 'lib')
    try:
        os.mkdir(dyn_libdir)
    except OSError:
        pass
    for name, depends in (
        ('atlas', ()),
        ('cblas', ('atlas',)),
        ('ptcblas', ('atlas',)),
        ('f77blas', ('atlas', 'gfortran')),
        ('ptf77blas', ('atlas', 'gfortran')),
        ('lapack', ('atlas', 'gfortran', 'f77blas', 'cblas'))
    ):
        static_in = pjoin(static_libdir, 'lib{0}.a'.format(name))
        dyn_out = pjoin(dyn_libdir, 'lib{0}.dylib'.format(name))
        atlas_deps = [pjoin(dyn_libdir, 'lib{0}.dylib'.format(name))
                      for name in depends if name != 'gfortran']
        cmd = (['gcc', m_flag, '-shared', '-o', dyn_out] +
               atlas_deps +
               (['-lgfortran'] if 'gfortran' in depends else []) +
               ['-all_load', static_in, '-install_name', dyn_out])
        back_tick(cmd)


if __name__ == '__main__':
    main()
