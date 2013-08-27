%define Werror_cflags %{nil}

#
# crash core analysis suite
#
Summary: Kernel crash and live system analysis utility
Name: crash
Version: 6.1.0
Release: 1%{?dist}
License: GPLv3
Group: System/Configuration/Hardware
Source: http://people.redhat.com/anderson/crash-%{version}.tar.gz
URL: http://people.redhat.com/anderson
ExclusiveOS: Linux
BuildRequires: ncurses-devel zlib-devel
Requires: binutils

%description
The core analysis suite is a self-contained tool that can be used to
investigate either live systems, kernel core dumps created from the
netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch
offered by Mission Critical Linux, or the LKCD kernel patch.

%package devel
Requires: %{name} = %{version}, zlib-devel
Summary: kernel crash and live system analysis utility
Group: System/Configuration/Hardware

%description devel
The core analysis suite is a self-contained tool that can be used to
investigate either live systems, kernel core dumps created from the
netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch
offered by Mission Critical Linux, or the LKCD kernel patch.

%prep
%setup -n %{name}-%{version} -q

%build
export ERROR_ON_WARNING=no
make GDB_CONF_FLAGS="--disable-Werror" RPMPKG="%{version}-%{release}" CFLAGS="%{optflags}"

%install
mkdir -p %{buildroot}%{_bindir}
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_mandir}/man8
cp -p crash.8 %{buildroot}%{_mandir}/man8/crash.8
mkdir -p %{buildroot}%{_includedir}/crash
chmod 0644 defs.h
cp -p defs.h %{buildroot}%{_includedir}/crash

%files
%{_bindir}/crash
%{_mandir}/man8/crash.8*
%doc README COPYING3

%files devel
%{_includedir}/*
