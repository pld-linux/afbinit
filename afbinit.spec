Summary:	Utility to load the microcode for Elite3D framebuffers to use X
Summary(pl.UTF-8):	Narzędzie do wczytywania mikrokodu framebufferów Elite3D potrzebnego dla X
Name:		afbinit
Version:	1.0.3
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://ftp.debian.org/debian/pool/contrib/a/afbinit/%{name}_1.0.orig.tar.gz
# Source0-md5:	c126b3ebb72e5028fd5d35fb6128316f
Source1:	ftp://ftp.debian.org/debian/pool/contrib/a/afbinit/%{name}_1.0-3.diff.gz
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

Note: you need to obtain Sun proprietary microcode (e.g. from Solaris
or Sun website) and place it into /lib/firmware/afb.ucode file.

%description -l pl.UTF-8
afbinit wczytuje mikrokod do akceleratorów graficznych Sun
Microsystems AFB Graphics Accellerator, znanych także pod nazwą Sun
Microsystems Elite 3D, spotykanych w wielu systemach UltraSPARC.
Mikrokod ten jest niezbędny do uruchamiania na tych kartach X11 z w
akceleracją grafiki.

Uwaga: ten program wymaga zdobycia własnościowego mikrokodu Suna (np.
z Solarisa lub strony WWW Suna) i umieszczenia go w pliku
/lib/firmware/afb.ucode .

%prep
%setup -q -n %{name}-1.0.orig
%{__gzip} -dc %{SOURCE1} | patch -p1 -s

# extract copyright information and adapt for PLD
sed -ne '4,11p;$abe found in common-licenses package.' debian/copyright > LICENSE

%build
%{__cc} %{rpmldflags} %{rpmcflags} \
%ifarch sparc
	-mv8plus \
%endif
	afbinit.c -o afbinit

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/etc/rc.d/init.d}

install afbinit $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/afbinit
install debian/afbinit.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc LICENSE
%attr(754,root,root) /etc/rc.d/init.d/afbinit
%attr(755,root,root) %{_sbindir}/afbinit
%{_mandir}/man8/afbinit.8*
