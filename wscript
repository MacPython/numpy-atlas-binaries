# waf script
# vim: ft=python
from __future__ import division, print_function, absolute_import
import os
from os.path import join as pjoin, split as psplit, isfile, dirname, pathsep
import sys
from glob import glob
import shutil
from subprocess import check_call, CalledProcessError
from functools import partial

from waflib.Errors import ConfigurationError
from wafutils import back_tick, FilePackageMaker as FPM, GitPackageMaker as GPM

PY3 = sys.version_info[0] >= 3
# Could get these from ATLAS libs directly - numpy does it in numpy distutils
# it seems.
GCC_VER = '4.8.2'
GCC_PATH = '/usr/local/gfortran/bin/gcc'
MACPIES_ROOT = '/Library/Frameworks/Python.framework/Versions'
# Source lib, width of architecture
ATLAS_PATTERN = '{0}/archives/atlas-3.10.1-build-{1}-sse2-full-gcc4.8.2/'

# If you change any git commits in the package definitions, you may need to run
# the ``waf refresh_submodules`` command

python_install_rule = ('cd ${SRC[0].abspath()} && ${PYTHON} setup.py install '
                       '--prefix=${bld.bldnode.abspath()}')
mpkg_build_rule = ('cd ${SRC[0].abspath()} && bdist_mpkg setup.py bdist_mpkg')
wheel_build_rule = ('cd ${SRC[0].abspath()} && '
                    '${PYTHON} ${bld.srcnode.abspath()}/bdist_wheel.py')


numpy_pkgs = {}
for arch in ('32', '64'):
    def _write_setup_cfg(task):
        site_node = task.inputs[0].make_node('site.cfg')
        write_pattern = """
# site.cfg file
[atlas]
library_dirs = {0}lib
include_dirs = {0}include
""".format(ATLAS_PATTERN)
        site_node.write(write_pattern.format(
            task.env.SRC_PREFIX,
            arch))
    numpy_pkgs[arch] = GPM('numpy_' + arch,
                           'v1.8.1',
                           wheel_build_rule,
                           patcher = _write_setup_cfg,
                           out_sdir = 'numpy_' + arch,
                           git_sdir = 'numpy')


def options(opt):
    opt.load('compiler_c')
    # Output for mpkg writing
    opt.add_option('--mpkg-outpath', action='store',
                   help='directory to write built mpkg')
    opt.add_option('--mpkg-clobber', action='store_true', default=False,
                   help='whether to overwrite existing output mpkg')


def _lib_path(start_path):
    version = sys.version_info
    return '{0}/lib/python{1}.{2}/site-packages'.format(
        start_path, version[0], version[1])


def configure(ctx):
    sys_env = dict(os.environ)
    bld_path = ctx.bldnode.abspath()
    # Add build path and expected gcc path to PATH
    sys_env['PATH'] = pathsep.join(('{0}/bin'.format(bld_path),
                                    dirname(GCC_PATH),
                                    sys_env['PATH']))
    os.environ['PATH'] = sys_env['PATH']
    ctx.load('compiler_c')
    # We need to record the build directory for use by non-build functions
    ctx.env.BLD_PREFIX = bld_path
    ctx.env.SRC_PREFIX = ctx.srcnode.abspath()
    ctx.env.BLD_SRC = pjoin(bld_path, 'src')
    ctx.find_program('git', var='GIT')
    # Update submodules in repo
    print('Running git submodule update, this might take a while')
    ctx.exec_command('git submodule update --init')
    # Prepare environment variables for compilation
    if not 'ARCH_FLAGS' in sys_env:
        sys_env['ARCH_FLAGS'] = '-arch i386 -arch x86_64'
    ctx.env.THIN_LDFLAGS = '{0} -L{1}/lib'.format(
        sys_env['ARCH_FLAGS'],
        bld_path)
    ctx.env.THICK_LDFLAGS = ctx.env.THIN_LDFLAGS + ' -lpng -lbz2'
    # For installing python modules
    ctx.env.PYTHONPATH = _lib_path(bld_path)
    sys_env['PYTHONPATH'] = ctx.env.PYTHONPATH
    sys_env['PKG_CONFIG_PATH'] = '{0}/lib/pkgconfig'.format(bld_path)
    sys_env['MACOSX_DEPLOYMENT_TARGET']='10.6'
    sys_env['CPPFLAGS'] = ('-I{0}/include '
                           '-I{0}/freetype2/include').format(bld_path)
    sys_env['CFLAGS'] = sys_env['ARCH_FLAGS']
    sys_env['LDFLAGS'] = ctx.env.THICK_LDFLAGS
    ctx.env.env = sys_env
    # Check we have the right gcc
    if not ctx.env.CC[0] == GCC_PATH:
        raise ConfigurationError('gcc path should be exactly {0} '
                                 'but is {1}'.format(GCC_PATH, ctx.env.CC[0]))
    if not '.'.join(ctx.env.CC_VERSION) == GCC_VER:
        raise ConfigurationError('Need gcc version ' + GCC_VER)


def build(ctx):
    bld_node = ctx.bldnode
    bld_path = bld_node.abspath()
    # We need the src directory before we start
    def pre(ctx):
        # src directory for code tree copies
        ctx.exec_command('mkdir -p {0}/src'.format(bld_path))
        # python site-packages directory for python installs
        ctx.exec_command('mkdir -p {0}'.format(_lib_path(bld_path)))
        # wheelhouse directory
        ctx.exec_command('mkdir -p {0}/wheelhouse'.format(bld_path))
    ctx.add_pre_fun(pre)
    wheel_tasks = []
    for name, pkg in numpy_pkgs.items():
        py_task_name, dir_node = pkg.unpack_patch_build(ctx)
        wheel_task = pkg.name + '.wheel.build'
        ctx(
            rule = wheel_build_rule,
            source = [dir_node],
            after = [py_task_name, 'wheel.build'],
            name = wheel_task)
        wheel_tasks.append(wheel_task)


def refresh_submodules(ctx):
    # Command to set submodules to defined commits
    call = partial(check_call, shell=True)
    print('Running git submodule update, this might take a while')
    call('git submodule update --init')
    for git_name, git_pkg in GPM.instances.items():
        checkout_cmd = 'cd {s.git_sdir} && git checkout {s.commit}'.format(
            s = git_pkg)
        fetch_cmd = 'cd {s.git_sdir} && git fetch'.format(
            s = git_pkg)
        try:
            call(checkout_cmd)
        except CalledProcessError:
            call(fetch_cmd)
            call(checkout_cmd)
