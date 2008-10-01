Summary:	NNTP server for small sites
Summary(pl.UTF-8):	Serwer NNTP przeznaczony dla niedużych serwerów
Name:		leafnode+
Version:	2.15
Release:	4
License:	Free
Group:		Networking/Daemons
Source0:	http://www25.big.jp/~jam/leafnode+/%{name}-%{version}.tar.gz
# Source0-md5:	1a53c4dd8f0d2896c9f1e4d2104318f3
Source1:	%{name}.inetd
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-va_fix.patch
URL:		http://www25.big.jp/~jam/leafnode+/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,postun):	rc-inetd
Requires:	inetdaemon
Provides:	nntpserver
Obsoletes:	leafnode
Conflicts:	inn
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Leafnode+ is a USENET software package designed for small sites, with
a few tens of readers and only a slow link to the net. Leafnode+ has
been derived from leafnode-1.4.

%description -l pl.UTF-8
Leafnode+ to zestaw programów umożliwiających stworzenie niewielkiego
serwera NNTP dla niewielkiej liczby użytkowników, bez potrzeby
posiadania szybkiego łącza do sieci. Leafnode+ został napisany na
podstawie programu leafnode-1.4.

%prep
%setup -q
%patch0 -p1
%patch1

%build
%{__make} LDFLAGS="%{rpmldflags}" \
	CFLAGS="%{rpmcflags} -DHAVE_POSIX_REGCOMP" \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_sysconfdir}/%{name} \
	SPOOLDIR=%{_var}/spool/news

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT%{_var}/spool/news

%{__make} installall \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_sysconfdir}/%{name} \
	SPOOLDIR=%{_var}/spool/news \

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/nntpd

touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/groupinfo
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config.example

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q rc-inetd reload

%postun
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc README COPYING FAQ Changes config.example
%config %dir %attr(770,root,news) %{_sysconfdir}/leafnode+
%ghost %attr(664,news,news) %{_sysconfdir}/leafnode+/groupinfo
%attr(750,root,news) %{_sbindir}/*
%attr(2770,root,news) %{_var}/spool/news
%attr(640,root,root) /etc/sysconfig/rc-inetd/nntpd
%{_mandir}/man8/*
