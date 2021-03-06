FROM golang:alpine AS build-env
LABEL maintainer "Eliezer Croitoru <ngtech1ltd@gmail.com>"

# Install OS-level dependencies.
RUN apk add --no-cache curl git vim bash wget

# Copy our source code into the container.
RUN git clone -b 'v2.0.0-rc.2' --single-branch --depth 1 https://github.com/chihaya/chihaya /root/chihaya && \
        cd /root/chihaya && \
        GO111MODULE=on CGO_ENABLED=0 go build ./cmd/chihaya

FROM centos:7
LABEL maintainer "Eliezer Croitoru <ngtech1ltd@gmail.com>"

RUN yum install -y gcc gcc-c++ \
                   libtool libtool-ltdl \
                   make cmake \
                   git \
                   pkgconfig \
                   sudo \
                   automake autoconf \
                   yum-utils rpm-build && \
    yum clean all

RUN useradd builder -u 1000 -m -G users,wheel \
   &&  echo "builder ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers \
   &&  echo "# macros" > /home/builder/.rpmmacros \
   &&  echo "%_topdir /home/builder/rpm" >> /home/builder/.rpmmacros \
   &&  echo "%_sourcedir %{_topdir}/SOURCES" >> /home/builder/.rpmmacros \
   &&  echo "%_builddir %{_topdir}/BUILD" >> /home/builder/.rpmmacros \
   &&  echo "%_specdir %{_topdir}/SPECS" >> /home/builder/.rpmmacros \
   &&  echo "%_rpmdir %{_topdir}/RPMS" >> /home/builder/.rpmmacros \
   &&  echo "%_srcrpmdir %{_topdir}/SRPMS" >> /home/builder/.rpmmacros \
   &&  mkdir /home/builder/rpm \
   &&  chown -R builder /home/builder

USER builder

ENV FLAVOR=rpmbuild OS=centos DIST=el7

COPY --from=build-env /root/chihaya/chihaya /chihaya

CMD ["/srv/pkg"]
