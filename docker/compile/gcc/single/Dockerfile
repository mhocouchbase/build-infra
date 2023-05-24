# Docker container just to build GCC, because it's slow.
# Note: A new version of binutils is also bundled for GCC>=12

FROM centos:7.9.2009 as builder
ARG GCC_VER
ARG BINUTILS_VERSION=2.40

# Install the older gcc so we can bootstrap up to the newer, then
# build and install newer. Note: important to update binutils here,
# as the version in the stock base image has a slightly bogus
# version string that is mis-parsed by the gcc build process.
RUN yum install --setopt=keepcache=0 -y \
        binutils \
        bison \
        bzip2 \
        file \
        gcc \
        gcc-c++ \
        make \
        texinfo \
        wget

RUN set -x \
      && mkdir /tmp/deploy \
      && cd /tmp/deploy \
      && curl -O https://ftp.gnu.org/gnu/gcc/gcc-${GCC_VER}/gcc-${GCC_VER}.tar.xz \
      && tar xf gcc-${GCC_VER}.tar.xz
RUN cd /tmp/deploy/gcc-${GCC_VER} && ./contrib/download_prerequisites
RUN mkdir /tmp/deploy/objdir
WORKDIR /tmp/deploy/objdir
RUN $PWD/../gcc-${GCC_VER}/configure --prefix=/opt/gcc-${GCC_VER} --disable-multilib --enable-languages=c,c++
RUN make -j$(nproc)

# We use install-strip for size reasons, but copy the non-stripped
# libstdc++.so.6.0.* afterward (because we ship that file in Server)
# so that we can get debug stack traces in production.
RUN make install-strip
RUN set -x \
      && ln -s gcc /opt/gcc-${GCC_VER}/bin/cc \
      && cp -a $(uname -m)-*-linux-gnu/libstdc++-v3/src/.libs/libstdc++.so.6.0.* /opt/gcc-${GCC_VER}/lib64

# This will cause g++ to bake "-rpath /opt/gcc-${GCC_VER}/lib64" into all
# binaries it builds, so they'll run correctly on the build systems.
# https://stackoverflow.com/questions/17220872/linking-g-4-8-to-libstdc/17224826#17224826
RUN export PATH=/opt/gcc-${GCC_VER}/bin:${PATH} \
    && g++ -dumpspecs \
         | awk "/^\*link:/ { print; getline; print \"-rpath=/opt/gcc-${GCC_VER}/lib64\", \$0; next } { print }" \
         > $(dirname $(g++ -print-libgcc-file-name))/specs

# If we're building a version of GCC more recent than 12, bundle in a newer
# binutils - this will avoid e.g the stock version on centos7 failing to
# build v8 on arm
WORKDIR /tmp
RUN set -x \
    && if [ ! "${GCC_VER}" = "$(printf ${GCC_VER}\\n12 | sort -V | head -n1)" ]; then \
      curl -Lf https://ftp.gnu.org/gnu/binutils/binutils-${BINUTILS_VERSION}.tar.xz -o binutils.tar.xz && \
      mkdir binutils && cd binutils && \
      tar xf ../binutils.tar.xz --strip-components=1 && \
      ./configure --prefix=/opt/gcc-${GCC_VER} && \
      make -j$(nproc) && \
      make install && \
      rm -rf /tmp/binutils* ; \
    fi

FROM scratch
ARG GCC_VER
LABEL maintainer="build-team@couchbase.com"
COPY --from=builder /opt/gcc-${GCC_VER} /opt/gcc-${GCC_VER}