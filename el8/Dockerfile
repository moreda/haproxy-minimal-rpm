FROM rockylinux/rockylinux:8

RUN yum install -y epel-release
RUN yum install -y --allowerasing curl diffutils gcc git make openssl-devel patch pcre-devel python3 rpm-build rpm-devel rpmdevtools rpmlint sed systemd-devel tree vim yum-utils zlib-devel readline-devel

VOLUME ["/docker"]
CMD ["make"]
