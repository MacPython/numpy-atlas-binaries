export MACOSX_DEPLOYMENT_TARGET=10.6
BITS=32
M_BITS="-m$BITS"
if [ "$BITS" == "32" ]; then
    M_BITS="$M_BITS -mincoming-stack-boundary=2"
fi
DIST_DIR="dist$BITS"
LINK_FLAGS="-Wall -undefined dynamic_lookup -bundle $M_BITS"
LDSHARED="gcc $LINK_FLAGS" LDFLAGS=$LINK_FLAGS CC="gcc $M_BITS" CFLAGS="$M_BITS" FFLAGS=$M_BITS FARCH=$M_BITS python setup.py bdist_wheel --dist-dir=$DIST_DIR
