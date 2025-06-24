%global haproxy_version 3.2.1
%global lua_version 5.4.8
%global haproxy_mainversion %(echo %{haproxy_version} | awk -F. '{print $1 "." $2}')

%global _hardened_build 1

Name:           haproxy
Version:        %{haproxy_version}
Release:        1%{?dist}
Summary:        HAProxy reverse proxy for high availability environments
License:        GPLv2+
Group:          System Environment/Daemons
URL:            https://www.haproxy.org/
Source0:        https://www.haproxy.org/download/%{haproxy_mainversion}/src/haproxy-%{version}.tar.gz
Source1:        https://www.lua.org/ftp/lua-%{lua_version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pcre2-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros

%description
HAProxy is a TCP/HTTP reverse proxy which is particularly suited for high availability environments. Indeed, it can:
 - route HTTP requests depending on statically assigned cookies
 - spread load among several servers while assuring server persistence through the use of HTTP cookies
 - switch to backup servers in the event a main one fails
 - accept connections to special ports dedicated to service monitoring
 - stop accepting connections without breaking existing ones
 - add, modify, and delete HTTP headers in both directions
 - block requests matching particular patterns
 - report detailed status to authenticated users from a URI intercepted from the application

%global debug_package %{nil}
%global _build_id_links none

%prep
%autosetup
%autosetup -a1  # unpack lua inside the haproxy top directory

%build
%define lua_dir ./lua-%{lua_version}
# Compile lua with position independent code.
%{__make} -C %{lua_dir} MYCFLAGS=-fPIC

# Compile haproxy using the lua libraries and includes.
%{__make} CPU="generic" TARGET="linux-glibc" USE_OPENSSL=1 USE_PCRE2=1 USE_SLZ=1 USE_LUA=1 USE_CRYPT_H=1 USE_LINUX_TPROXY=1 USE_GETADDRINFO=1 USE_PROMEX=1 ${regparm_opts} ADDINC="%{build_cflags}" ADDLIB="%{build_ldflags}" LUA_LIB=%{lua_dir}/src LUA_INC=%{lua_dir}/src
%{__make} admin/halog/halog ADDINC="%{build_cflags}" ADDLIB="%{build_ldflags}"
pushd admin/iprange
%{__make} OPTIMIZE="%{build_cflags}" LDFLAGS="%{build_ldflags}"
popd

%install
%{__make} install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix} TARGET="linux-glibc"
%{__make} install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

%{__install} -p -D -m 0644 %{_sourcedir}/local/haproxy.service %{buildroot}%{_unitdir}/haproxy.service
%{__install} -p -D -m 0644 %{_sourcedir}/local/haproxy.cfg %{buildroot}%{_sysconfdir}/haproxy/haproxy.cfg
%{__install} -p -D -m 0644 %{_sourcedir}/local/haproxy.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/haproxy
%{__install} -p -D -m 0644 %{_sourcedir}/local/haproxy.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/haproxy
%{__install} -p -D -m 0644 %{_sourcedir}/local/haproxy.sysusers %{buildroot}%{_sysusersdir}/haproxy.conf
%{__install} -p -D -m 0644 %{_sourcedir}/local/halog.1 %{buildroot}%{_mandir}/man1/halog.1

%{__install} -d -m 0755 %{buildroot}%{_localstatedir}/lib/haproxy
%{__install} -d -m 0755 %{buildroot}%{_datadir}/haproxy
%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}/haproxy/conf.d
%{__install} -d -m 0755 %{buildroot}%{_bindir}
%{__install} -p -m 0755 ./admin/halog/halog %{buildroot}%{_bindir}/halog
%{__install} -p -m 0755 ./admin/iprange/iprange %{buildroot}%{_bindir}/iprange
%{__install} -p -m 0755 ./admin/iprange/ip6range %{buildroot}%{_bindir}/ip6range
%{__cp} ./examples/errorfiles/* %{buildroot}%{_datadir}/haproxy
find %{buildroot}%{_datadir}/haproxy -type f -exec chmod 644 {} \;

%pre
%sysusers_create_compat %{_sourcedir}/local/haproxy.sysusers

%post
%systemd_post haproxy.service

%preun
%systemd_preun haproxy.service

%postun
%systemd_postun_with_restart haproxy.service

%files
%doc doc/* examples/*
%doc CHANGELOG README.md VERSION
%license LICENSE
%dir %{_localstatedir}/lib/haproxy
%dir %{_sysconfdir}/haproxy
%dir %{_sysconfdir}/haproxy/conf.d
%dir %{_datadir}/haproxy
%{_datadir}/haproxy/*
%config(noreplace) %{_sysconfdir}/haproxy/haproxy.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/haproxy
%config(noreplace) %{_sysconfdir}/sysconfig/haproxy
%{_unitdir}/haproxy.service
%{_sbindir}/haproxy
%{_bindir}/halog
%{_bindir}/iprange
%{_bindir}/ip6range
%{_mandir}/man1/*
%{_sysusersdir}/haproxy.conf
