%define _disable_ld_no_undefined 1

#
# crash core analysis suite
#
Summary: Kernel crash and live system analysis utility
Name: crash
Version:	7.2.6
Release:	1
License: GPLv3
Group: System/Configuration/Hardware
Source0: http://people.redhat.com/anderson/crash-%{version}.tar.gz
URL: http://people.redhat.com/anderson
ExclusiveOS: Linux
BuildRequires: ncurses-devel zlib-devel bison flex
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
#We need this to really link using ld.bfd
mkdir bin/
cd bin/ ; ln -s /usr/bin/ld.bfd ld
cd ..
export PATH=$(PWD)/bin:$PATH

make RPMPKG="%{version}-%{release}" CFLAGS=`"echo %{optflags} | sed -e 's/-Wstrict-aliasing=2//'"` CFLAGS+=-fuse-ld=bfd 
make extensions

%install
mkdir -p %{buildroot}%{_bindir}
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_mandir}/man8
cp -p crash.8 %{buildroot}%{_mandir}/man8/crash.8
mkdir -p %{buildroot}%{_includedir}/crash
chmod 0644 defs.h
cp -p defs.h %{buildroot}%{_includedir}/crash

mkdir -p %{buildroot}%{_libdir}/crash/extensions
if [ -f extensions/eppic.so ]
then
	cp extensions/eppic.so %{buildroot}%{_libdir}/crash/extensions
fi

cp extensions/dminfo.so %{buildroot}%{_libdir}/crash/extensions
cp extensions/snap.so %{buildroot}%{_libdir}/crash/extensions
cp extensions/trace.so %{buildroot}%{_libdir}/crash/extensions

find %{buildroot} -iname "*.[c|h]" -exec chmod -x {} \;

%clean
rm -rf %{buildroot}

%files
%{_bindir}/crash
%{_mandir}/man8/crash.8*
%{_libdir}/crash/extensions/*
%doc README COPYING3

%files devel
%{_includedir}/*

%changelog
* Mon May 12 2014 Marco A Benatto <benatto@mandriva.com.br> 7.0.6
- Updating to version 7.0.6
- Enabling crash upstream extensions

