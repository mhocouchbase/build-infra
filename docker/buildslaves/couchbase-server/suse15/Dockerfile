# Docker container for SUSE 15, based on openSUSE LEAP

FROM opensuse/leap:15.0

MAINTAINER build-team@couchbase.com

USER root
RUN perl -pi -e 's#download.opensuse.org#suse.mirrors.tds.net/pub/opensuse#g' /etc/zypp/repos.d/*
RUN zypper -n install vim sudo curl && zypper clean

# Create couchbase user with password-less sudo privs, and give
# ownership of /opt/couchbase
RUN groupadd -g1000 couchbase && \
    useradd couchbase -g couchbase -u1000 -m -s /bin/bash && \
    mkdir /opt/couchbase && chown -R couchbase:couchbase /opt/couchbase && \
    echo 'couchbase:couchbase' | chpasswd && \
    sed -ri 's/ALL\) ALL/ALL) NOPASSWD:ALL/' /etc/sudoers

# tini, to avoid zombie issues when running with Swarm jar
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

# JDK for Jenkins
RUN zypper -n install java-1_8_0-openjdk-headless && zypper clean
RUN curl \
    https://repo.jenkins-ci.org/releases/org/jenkins-ci/plugins/swarm-client/3.13/swarm-client-3.13.jar \
    -o /usr/local/lib/swarm-client.jar

### Install Couchbase build dependencies ######################################
# * Packages from the base CentOS repository
RUN zypper -n install \
                hostname \
                binutils \
                curl \
                ed \
                gcc-c++ \
                make \
                cmake \
                ccache \
                git \
                man \
                ncurses-devel \
                libffi-devel \
                libnuma-devel \
                libopenssl-devel \
                lsb-release \
                python-devel \
                rpm-build \
                ruby \
                tar \
                unzip && \
                zypper clean

#paramiko for testrunner
RUN zypper -n --gpg-auto-import-keys install python-pip
RUN pip install -U pip && pip install paramiko pygerrit2

# Install autoconf and friends - necessary for building some third-party deps
# from source, not for Couchbase. (The "full" version of perl is also required
# for some third-party builds.)
RUN zypper -n install perl m4 autoconf automake libtool && zypper clean

# * ccache symlinks
RUN ln -s /usr/bin/ccache /home/couchbase/bin/gcc && \
    ln -s /usr/bin/ccache /home/couchbase/bin/g++ && \
    ln -s /usr/bin/ccache /home/couchbase/bin/cc && \
    ln -s /usr/bin/ccache /home/couchbase/bin/c++

# * repo
RUN curl https://storage.googleapis.com/git-repo-downloads/repo -o /usr/local/bin/repo && \
    chmod a+x /usr/local/bin/repo

# Run our builder startup script
ADD .ssh /home/couchbase/.ssh
COPY build/couchbuilder_start.sh /usr/sbin/
ENTRYPOINT [ "/tini", "--", "/usr/sbin/couchbuilder_start.sh" ]
CMD [ "swarm" ]

# Keep this stuff at the end, because the ARG declaration breaks
# Docker build caching
ARG CONTAINER_TAG_ARG
ENV CONTAINER_TAG=${CONTAINER_TAG_ARG}
