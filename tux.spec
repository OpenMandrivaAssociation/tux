Summary:	User-space component of TUX kernel-based threaded HTTP server
Name:		tux
Version:	3.2.18
Release:	%mkrel 5
License:	GPL
Group:		System/Servers
URL:		http://people.redhat.com/mingo/TUX-patches/2.1-docs/
Source:		%{name}-%{version}.tar.bz2
Patch0:		tux-fix.diff.bz2
Patch1:		%{name}-2.2.7-init.patch.bz2
Patch2:		%{name}-3.2.14-Makefile.patch.bz2
Patch3:		tux-3.2.18-gcc34.patch.bz2
Requires(post): rpm-helper
Requires(preun):rpm-helper
ExclusiveArch:	%{ix86}
Requires:	mailcap
BuildRequires:	popt 
BuildRequires:  glib-devel 
BuildRequires:  popt-devel
BuildRequires:	docbook-utils
BuildRequires:	openjade
BuildRoot:	%{_tmppath}/%{name}-%{version}-%release}-buildroot

%description
TUX is a kernel-based, threaded, extremely high performance HTTP server.
It is able to efficiently and safely serve both static and dynamic data.
TUX moves the HTTP protocol stack to the kernel, and can handle requests
for data with both kernel-space and user-space modules.

See http://www.redhat.com/mailing-lists/ for instructions on subscribing
to tux-list@redhat.com; users of TUX have the opportunity to share their
experiences and receive notices of new versions on that list.

%package	devel
Summary:	Header files for developing apps which will use TUX
Group:		Development/C
Provides:	libtux-devel
Obsoletes:	libtux-devel

%description	devel
Development files for Tux server.

%prep

%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p1 -b .gcc34

%build
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall TOPDIR=%{buildroot}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}
if [ "$1" = 0 ]; then
    rm -rf /var/tux/*
fi

%files
%defattr(-,root,root)
%doc tux.README NEWS SUCCESS gettuxconfig checkbindings
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/rc.d/init.d/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/tux.mime.types
%attr(0644,root,root) %{_mandir}/man*/*
%attr(0700,root,root) %dir /var/tux
%attr(0755,root,root) %{_sbindir}/*

%files devel
%defattr(-,root,root)
%doc tux.README demo.c demo?.c samples/sample.log samples/sample.out docs/tux docs/TUXAPI*
%attr(0644,root,root) %{_includedir}/*
