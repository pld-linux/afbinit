Summary:	Loads the microcode for Elite3D framebuffers to use X
Name:		afbinit
Version:	1.0.3
Release:	1
License:	GPL/MIT
Group:		Applications/System
Source0:	http://ftp.pl.debian.org/debian/pool/contrib/a/afbinit/%{name}_1.0.orig.tar.gz
# Source0-md5:	c126b3ebb72e5028fd5d35fb6128316f
Source1:	http://ftp.pl.debian.org/debian/pool/contrib/a/afbinit/%{name}_1.0-3.diff.gz
# Source1-md5:	45dfdb91b3e259a06bc864ffb340580f
Source2:	%{name}.init
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
ExclusiveArch:	sparc sparcv9 sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
afbinit loads the microcode firmware onto Sun Microsystems AFB
Graphics Accelerators aka Sun Microsystems Elite 3D found in many
UltraSPARC systems. The microcode is necessary if you want to run X11
with acceleration on these cards.

%prep

%setup -q -n %{name}-1.0.orig
%{__gzip} -dc %{SOURCE1} | patch -p1 -s


%build
%{__cc} %{rpmcflags} \
%ifarch sparc
    -mv8plus \
%endif
    afbinit.c -o afbinit

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_sbindir}
install afbinit $RPM_BUILD_ROOT/%{_sbindir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/afbinit

install -d $RPM_BUILD_ROOT%{_mandir}/man8
install debian/afbinit.8 $RPM_BUILD_ROOT%{_mandir}/man8/

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/afbinit
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/afbinit.8*
