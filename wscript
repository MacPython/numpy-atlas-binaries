# waf script
# vim: ft=python
from __future__ import division, print_function, absolute_import
import os
from os.path import (join as pjoin, isfile, dirname, pathsep, expanduser,
                     exists, basename)
import sys
from glob import glob
import shutil
from subprocess import check_call, CalledProcessError
from functools import partial

from waflib.Errors import ConfigurationError
from wafutils import GitPackageMaker as GPM
from monkeyexec import monkey_patch

# Could get these from ATLAS libs directly - numpy does it in numpy distutils
# it seems.
GCC_VER = '4.8.2'
GCC_PATH = '/usr/local/gfortran/bin/gcc'

# Standard root for installed Python.org Pythons
MACPIES_ROOT = '/Library/Frameworks/Python.framework/Versions'
# Pattern for 32 / 64 bit built ATLAS library directories
ATLAS_SDIR_PATTERN = 'archives/atlas-3.10.1-build-{0}-sse2-full-gcc4.8.2'
# subdirectory in build directory for virtualenv
VENV_SDIR = 'venv'
# Python version first digit -> required numpy for scipy build
PY_SP_NP_DEPENDS = {2: '1.5.1', 3: '1.7.1'}
# git tags for numpy and scipy to build
PKG2TAG = dict(numpy = 'v1.8.1', scipy = 'v0.14.0')

# If you change any git commits in the package definitions, you may need to run
# the ``waf refresh_submodules`` command


def options(opt):
    opt.load('compiler_c')
    # Output for wheel writing
    opt.add_option('-w', '--wheel-dir', action='store',
                   help='directory to write built mpkg')
    opt.add_option('--packages', action='store',
                   help='comma separated list of package to build from '
                   'numpy, scipy; e.g "numpy", "numpy,scipy"')
    opt.add_option('--clobber', action='store_true', default=False,
                   help='whether to overwrite existing output wheels')
    opt.add_option('--continuous-stdout', action='store_true', default=False,
                   help='whether to monkey patch waf to give continuous '
                   'stdout (useful for long-running jobs on travis)')
    opt.add_option('--pip-install-opts', action='store', default='',
                   help='options to prepend to pip install')


def configure(ctx):
    sys_env = dict(os.environ)
    bld_path = ctx.bldnode.abspath()
    src_path = ctx.srcnode.abspath()
    # Add
    # * SRC scripts path
    # * expected gcc path
    # * output virtualenv path
    sys_env['PATH'] = pathsep.join((
        '{0}/bin'.format(src_path),
        dirname(GCC_PATH),
        '{0}/{1}/bin'.format(bld_path, VENV_SDIR),
        sys_env['PATH']))
    os.environ['PATH'] = sys_env['PATH']
    ctx.load('compiler_c')
    # We need to record the build directory for use by non-build functions
    ctx.env.BLD_PREFIX = bld_path
    ctx.env.SRC_PREFIX = ctx.srcnode.abspath()
    ctx.env.BLD_SRC = pjoin(bld_path, 'src')
    ctx.env.PY_LD_FLAGS = "-Wall -undefined dynamic_lookup -bundle"
    ctx.find_program('git', var='GIT')
    ctx.find_program('virtualenv', var='VIRTUALENV')
    # Update submodules in repo
    ctx.to_log('Running git submodule update, this might take a while')
    ctx.exec_command('git submodule update --init')
    # For compiling python modules
    sys_env['MACOSX_DEPLOYMENT_TARGET']='10.6'
    # Check we have the right gcc
    ctx.env.env = sys_env
    suffix = ('You probably need to install '
              'archives/gfortran-4.8.2-Mavericks.dmg')
    if not ctx.env.CC[0] == GCC_PATH:
        raise ConfigurationError('gcc path should be exactly {0} but '
                                 'is {1}. '.format(GCC_PATH, ctx.env.CC[0])
                                 + suffix)
    if not '.'.join(ctx.env.CC_VERSION) == GCC_VER:
        raise ConfigurationError('Need gcc version {0}. {1}'.format(
            GCC_VER, suffix))
    # Set numpy dependings
    ctx.env.NP_SP_DEPENDS = PY_SP_NP_DEPENDS[sys.version_info[0]]
    # Input Python version
    ctx.env.PYTHON_EXE=sys.executable
    # packages to compile
    packages = ctx.options.packages
    if packages is None or packages == '':
        packages = ['numpy', 'scipy']
    else:
        packages = [pkg.strip() for pkg in packages.split(',') if pkg.strip()]
    ctx.env.PACKAGES = packages


def build(ctx):
    bld_path = ctx.bldnode.abspath()
    packages = ctx.env.PACKAGES
    # Monkey patching exec_command if required
    if ctx.options.continuous_stdout:
        monkey_patch()
    # We need the src directory before we start
    def pre(ctx):
        # src directory for code tree copies
        ctx.exec_command('mkdir -p {0}/src'.format(bld_path))
        # wheelhouse directory
        ctx.exec_command('mkdir -p {0}/wheelhouse'.format(bld_path))
    ctx.add_pre_fun(pre)
    # Set up virtualenv
    ctx(
        rule = '${VIRTUALENV} --python=${PYTHON_EXE} ${TGT}',
        target = VENV_SDIR,
        name = 'mkvirtualenv')
    v_bin = pjoin(bld_path, VENV_SDIR, 'bin')
    v_python = pjoin(v_bin, 'python')
    v_pip_install = '{0}/pip install {1} '.format(
        v_bin, ctx.options.pip_install_opts)
    # Install various packages into virtualenv.  Install sequentially
    # for simplicity
    ctx( # to make sure wheel installs will work
        rule = v_pip_install + '--ignore-installed pip',
        after = 'mkvirtualenv',
        name = 'upgrade-pip')
    ctx(
        rule = v_pip_install + 'wheel',
        after = 'upgrade-pip',
        name = 'install-wheel')
    # Install delocate into virtualenv
    pkg = GPM('delocate',
              'HEAD',
              'cd ${SRC[0].abspath()} && ' + v_python + ' setup.py install',
              after = 'install-wheel')
    delocate_name, dir_node = pkg.unpack_patch_build(ctx)
    # And Cython, tempita.
    ctx(
        rule = v_pip_install + 'cython',
        after = delocate_name,
        name = 'install-cython')
    ctx(
        rule = v_pip_install + 'tempita',
        after = 'install-cython',
        name = 'install-tempita')
    after_build_ready = ['install-tempita']
    # Build ATLAS libs
    atlas_libs = {}
    for arch in ('32', '64'):
        atlas_dir_in = pjoin(
            ctx.env.SRC_PREFIX,
            ATLAS_SDIR_PATTERN.format(arch))
        atlas_dir_out = pjoin(bld_path, 'src', 'atlas_' + arch)
        name = 'atlas-{0}-lib'.format(arch)
        ctx(
            rule = 'make_shared_atlas.py {0} {1}'.format(atlas_dir_in,
                                                         atlas_dir_out),
            after = delocate_name,
            name = name)
        atlas_libs[arch] = dict(path=atlas_dir_out, name=name)
    # Prepare for scipy build
    if 'scipy' in packages:
        ctx(
            rule = v_pip_install + 'numpy==' + ctx.env.NP_SP_DEPENDS,
            after = after_build_ready,
            name = 'numpy-for-scipy')
    build_strs = {}
    for arch in ('32', '64'):
        # Build command for numpy and scipy
        build_strs[arch] = ('ATLAS="{atlas_path}" '
                            'LDSHARED="gcc {PY_LD_FLAGS} -m{arch}" '
                            'LDFLAGS="{PY_LD_FLAGS} -m{arch}" '
                            'CC="gcc -m{arch}" '
                            'CFLAGS="-m{arch}" '
                            'FFLAGS="-m{arch}" '
                            'FARCH="-m{arch}" '
                            '{v_python} setup.py bdist_wheel').format(
                                atlas_path = atlas_libs[arch]['path'],
                                arch = arch,
                                PY_LD_FLAGS = ctx.env.PY_LD_FLAGS,
                                v_python = v_python)
    for pkg_name in packages:
        git_tag = PKG2TAG[pkg_name]
        add_after = ['numpy-for-scipy'] if pkg_name == 'scipy' else after_build_ready
        delocate_tasks = []
        for arch in ('32', '64'):
            pkg = GPM(pkg_name + '_' + arch,
                      git_tag,
                      'cd ${SRC[0].abspath()} && ' + build_strs[arch],
                      after = [atlas_libs[arch]['name']] + add_after,
                      out_sdir = pkg_name + '_' + arch,
                      git_sdir = pkg_name)
            py_task_name, dir_node = pkg.unpack_patch_build(ctx)
            delocate_task = pkg_name + '.delocate'
            ctx(
                rule = 'cd ${SRC[0].abspath()} && delocate-wheel dist/*.whl',
                source = [dir_node],
                after = [py_task_name],
                name = delocate_task)
            delocate_tasks.append(delocate_task)
        ctx(
            rule = ('cp src/{pkg}_32/dist/*.whl wheelhouse && '
                    'delocate-fuse wheelhouse/{pkg}*.whl '
                    'src/{pkg}_64/dist/{pkg}*.whl').format(pkg = pkg_name),
            after = delocate_tasks,
            name = 'fuse')


def refresh_submodules(ctx):
    # Command to set submodules to defined commits
    call = partial(check_call, shell=True)
    ctx.to_log('Running git submodule update, this might take a while')
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


def cp_wheels(ctx):
    # Wheel out directory
    wheel_dir = ctx.options.wheel_dir
    if wheel_dir is None:
        ctx.fatal('Need to set --wheel-dir to copy wheels')
    wheel_dir = expanduser(wheel_dir)
    # Get build time configuration
    from waflib.ConfigSet import ConfigSet
    env = ConfigSet()
    env_cache = pjoin('build', 'c4che', '_cache.py')
    if not isfile(env_cache):
        ctx.fatal('Run `configure` and `build` before `cp_wheels`')
    env.load(env_cache)
    # Check if any wheels have been built
    build_path = env.BLD_PREFIX
    globber = pjoin(build_path, 'wheelhouse', '*whl')
    wheels = glob(globber)
    if len(wheels) == 0:
        ctx.fatal("No wheels found with " + globber)
    if not exists(wheel_dir):
        os.makedirs(wheel_dir)
    if len(wheels) == 0:
        ctx.to_log('No wheels to copy')
    for wheel in wheels:
        out_wheel = pjoin(wheel_dir, basename(wheel))
        if exists(out_wheel):
            if not ctx.options.clobber:
                ctx.fatal('{0} exists, --clobber not set'.format(out_wheel))
        shutil.copyfile(wheel, out_wheel)
        ctx.to_log('Copied ' + wheel)
