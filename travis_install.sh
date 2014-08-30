# Install script for numpy atlas binaries
# Should be 'source'ed

# Use generic macpython fetching and utilities
source terryfy/travis_tools.sh

# GNU Fortran specifics
GF_ARCHIVE=archives/gfortran-4.8.2-Mavericks.dmg
GF_PKG_SDIR=gfortran-4.8.2-Mavericks/gfortran.pkg
GF_BIN_PATH=/usr/local/gfortran/bin

# Cache for wheels neede for building
NIPY_WHEELHOUSE=https://nipy.bic.berkeley.edu/scipy_installers


function install_gfortran {
    local gf_vol=/Volumes/gfortran
    check_var $GF_ARCHIVE
    check_var $GF_PKG_SDIR
    check_var $GF_BIN_PATH
    hdiutil attach $GF_ARCHIVE -mountpoint $gf_vol
    require_success "Failed to mount compiler dmg"
    sudo installer -pkg $gf_vol/$GF_PKG_SDIR -target /
    require_success "Failed to install gfortran compiler"
    export PATH=/usr/local/gfortran/bin:$PATH
    # in case these are set to clang versions
    export CC=$GF_BIN_PATH/gcc
    export CXX=$GF_BIN_PATH/g++
}


function build_wheels {
    local packages=$1
    check_var $packages
    local package_settings=""
    if [ -n "$NP_TAG" ]; then
        $package_settings="$package_settings --np-tag ${NP_TAG}"
    fi
    if [ -n "$SP_TAG" ]; then
        $package_settings="$package_settings --sp-tag ${SP_TAG}"
    fi
    # Continuous-stdout flag is to keep travis-ci from timing out the build
    # commands because they last longer than 10 minutes without stdout
    $PYTHON_EXE ./waf distclean configure build --continuous-stdout \
        --pip-install-opts="-f $NIPY_WHEELHOUSE" --packages="$packages" \
        $package_settings
    require_success "Build failed I'm afraid"
    rename_wheels build/wheelhouse
}


# Need to run in virtualenv for Python 3 - hence "installation_venv" at the
# end of the invocation to install within virtualenv
#
# Otherwise paths get very confused when using virtualenv
# Related to https://github.com/pypa/virtualenv/issues/620
get_python_environment macpython $VERSION installation_venv
install_gfortran
# Need virtualenv to make build virtualenv
$PIP_CMD install virtualenv
build_wheels $PACKAGES
