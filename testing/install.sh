#!/usr/bin/env sh
# Depends on following envs being defined:
# REQUIREMENTS_FILE (URL or filename for pip requirements file)
# TEST (name of test - see TEST checks below)
#
# These variables may or may not be defined depending on the test
# PY (major.minor form of Python version)
# PY_VERSION (major.minor.point form of Python version)
# VENV (defined if we should install and test in virtualenv)

GET_PIP_URL=https://bootstrap.pypa.io/get-pip.py
MACPYTHON_PREFIX=/Library/Frameworks/Python.framework/Versions
GF_ARCHIVE=archives/gfortran-4.8.2-Mavericks.dmg
GF_PKG_SDIR=gfortran-4.8.2-Mavericks/gfortran.pkg
WHEELHOUSE=build/wheelhouse

function require_success {
    STATUS=$?
    MESSAGE=$1
    if [ "$STATUS" != "0" ]; then
        echo $MESSAGE
        exit $STATUS
    fi
}


function install_gfortran {
    GF_VOL=/Volumes/gfortran
    hdiutil attach $GF_ARCHIVE -mountpoint $GF_VOL
    require_success "Failed to mount compiler dmg"
    sudo installer -pkg $GF_VOL/$GF_PKG_SDIR -target /
    require_success "Failed to install gfortran compiler"
}


function build_wheels {
    $PYTHON ./waf distclean configure build
    require_success "Build failed I'm afraid"
}


function install_mac_python {
    PY_VERSION=$1
    PY_DMG=python-$PY_VERSION-macosx10.6.dmg
    curl https://www.python.org/ftp/python/$PY_VERSION/${PY_DMG} > $PY_DMG
    require_success "Failed to download mac python $PY_VERSION"

    hdiutil attach $PY_DMG -mountpoint /Volumes/Python
    sudo installer -pkg /Volumes/Python/Python.mpkg -target /
    require_success "Failed to install Python.org Python $PY_VERSION"
    M_dot_m=${PY_VERSION:0:3}
    export PYTHON=/usr/local/bin/python$M_dot_m
    export PATH=$MACPYTHON_PREFIX/$M_dot_m/bin:$PATH
}


function get_pip {
    PYTHON=$1

    curl -O $GET_PIP_URL > get-pip.py
    require_success "failed to download get-pip"

    sudo $PYTHON get-pip.py
    require_success "Failed to install pip"
}


if [ "$TEST" == "macpython" ] ; then

    install_mac_python $PY_VERSION
    PY=${PY_VERSION:0:3}
    get_pip $PYTHON
    export PIP="sudo $MACPYTHON_PREFIX/$PY/bin/pip$PY"
    install_gfortran
    $PIP install virtualenv
    build_wheels
    $PIP install $WHEELHOUSE/numpy*.whl
    $PIP install $WHEELHOUSE/scipy*.whl

else
    echo "Unknown test setting ($TEST)"
    exit -1
fi
