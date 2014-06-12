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
from itertools import cycle

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

numpy_pkgs = {}
for arch in ('32', '64'):
    def _write_setup_cfg(task):
        site_node = task.inputs[0].make_node('site.cfg')
        write_pattern = """
# site.cfg file
[atlas]
library_dirs = {0}dylibs
include_dirs = {0}include
""".format(ATLAS_PATTERN)
        site_node.write(write_pattern.format(
            task.env.SRC_PREFIX,
            arch))
    build_rule = ('cd ${SRC[0].abspath()} && '
                  'LDSHARED="gcc ${PY_LD_FLAGS} -m%s" '
                  'LDFLAGS="${PY_LD_FLAGS} -m%s" '
                  'CC="gcc -m%s" '
                  'CFLAGS="-m%s" '
                  'FFLAGS="-m%s" '
                  'FARCH="-m%s" '
                  '${PYTHON} ${bld.srcnode.abspath()}/bdist_wheel.py'
                  % ((arch,) * 6))
    numpy_pkgs[arch] = GPM('numpy_' + arch,
                           'v1.8.1',
                           build_rule,
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
    ctx.env.PY_LD_FLAGS = "-Wall -undefined dynamic_lookup -bundle"
    ctx.find_program('git', var='GIT')
    # Update submodules in repo
    print('Running git submodule update, this might take a while')
    ctx.exec_command('git submodule update --init')
    # For compiling python modules
    sys_env['MACOSX_DEPLOYMENT_TARGET']='10.6'
    # For using delocate
    sys_env['PYTHONPATH'] = pjoin(ctx.env.SRC_PREFIX, 'delocate')
    ctx.env.env = sys_env
    # Check we have the right gcc
    suffix = ('You probably need to install '
              'archives/gfortran-4.8.2-Mavericks.dmg')
    if not ctx.env.CC[0] == GCC_PATH:
        raise ConfigurationError('gcc path should be exactly {0} but '
                                 'is {1}. '.format(GCC_PATH, ctx.env.CC[0])
                                 + suffix)
    if not '.'.join(ctx.env.CC_VERSION) == GCC_VER:
        raise ConfigurationError('Need gcc version {0}. {1}'.format(
            GCC_VER, suffix))


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
    delocate_tasks = []
    for name, pkg in numpy_pkgs.items():
        py_task_name, dir_node = pkg.unpack_patch_build(ctx)
        delocate_task = pkg.name + '.delocate'
        ctx(
            rule = ('cd ${SRC[0].abspath()} && '
                    'python ${bld.srcnode.abspath()}'
                    '/delocate/scripts/delocate-wheel '
                    'dist/*.whl'),
            source = [dir_node],
            after = [py_task_name],
            name = delocate_task)
        delocate_tasks.append(delocate_task)
    ctx(
        rule = ('cp src/numpy_32/dist/*.whl wheelhouse && '
                'python ${bld.srcnode.abspath()}'
                '/delocate/scripts/delocate-fuse '
                'wheelhouse/numpy*.whl '
                'src/numpy_64/dist/numpy*.whl'),
        after = delocate_tasks,
        name = 'fuse')


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
