# Must be unix line endings
# In vim - set ff=unix
# Turn off CPU throttling
# Control panel, Hardware and sound, Power options, Select a power plan, Show
# additional plans, High perfornamce
atlas_home="$HOME/atlas"
downloads="${atlas_home}/downloads"
lapack_tarfile="${downloads}/lapack-3.5.0.tgz"
prefix_home=$HOME/archives/atlas
gtar=gtar
bit_width=32
# atlas_ver="3.11.26"
atlas_ver="3.10.1"
build_suff="-$bit_width-sse2-full-gcc4.8.2"
# build_suff="-cygwin-mingw"
# config_opts="-b 32"
# config_opts="-b 32 -Si archdef 0 -A 13 -V 384 \
#    --with-netlib-lapack-tarfile=${lapack_tarfile} \
#    -Fa al '-mincoming-stack-boundary=2 -mfpmath=sse -msse2'"
config_opts="-b $bit_width -V 384 \
    --with-netlib-lapack-tarfile=${lapack_tarfile} \
    -Fa al '-mfpmath=sse -msse2 \
    -m$bit_width'"

# usually don't need to change these guys
atlas_sdir=atlas-${atlas_ver}
atlas_src=$atlas_home/$atlas_sdir
build_sdir="atlas-${atlas_ver}-build${build_suff}"
atlas_build="$atlas_home/$build_sdir"
atlas_prefix="$prefix_home/$build_sdir"
atlas_tar="${downloads}/atlas${atlas_ver}.tar.bz2"

# doit
rm -rf $atlas_build
mkdir -p $atlas_build
mkdir -p $atlas_prefix
# Copy this install script file into the build directory
if [ -e "$0" ]; then
    cp $0 $atlas_build
fi
cd $atlas_home
if [ ! -d "$atlas_src" ]; then
    $gtar jxvf "$atlas_tar"
    mv ATLAS ${atlas_src}
fi
cd $atlas_build
${atlas_src}/configure ${config_opts} --prefix=$atlas_prefix
make build
