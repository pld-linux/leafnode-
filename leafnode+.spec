Summary:	NNTP server for small sites
Summary(pl):	Serwer NNTP przeznaczony dla niedużych serwerów
Name:		leafnode+
Version:	2.12
Release:	1
License:	free to use, modify and distribute
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://www.io.com/~kazushi/leafnode+/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.io.com/~kazushi/leafnode+/
Requires:	rc-inetd
Requires:	inetdaemon
Provides:	nntpserver
Obsoletes:	leafnode
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Leafnode+ is a USENET software package designed for small sites, with
a few tens of readers and only a slow link to the net. Leafnode+ has
been derived from leafnode-1.4.

%description -l pl
Leafnode+ to zestaw programów umożliwiających stworzenie niewielkiego
serwera NNTP dla niewielkiej liczby użytkowników, bez potrzeby
posiadania szybkiego łącza do sieci. Leafnode+ został napisany na
podstawie programu leafnode-1.4.

%prep
%setup -q
%patch0 -p1

%build
%{__make} LDFLAGS="%{!?debug:-s}" \
	CFLAGS="%{!?debug:$RPM_OPT_FLAGS}%{?debug:-O -g} -DHAVE_POSIX_REGCOMP" \
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_sysconfdir}/%{name} \
	SPOOLDIR=%{_var}/spool/news \

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/nntpd

touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/groupinfo
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config.example

gzip -9nf README COPYING FAQ Changes config.example

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%config %dir %attr(750,news,news) %{_sysconfdir}/leafnode+
%ghost %attr(640,news,news) %{_sysconfdir}/leafnode+/groupinfo
%attr(750,news,news) %{_sbindir}/*
%attr(2750,news,news) %{_var}/spool/news
%attr(640,root,root) /etc/sysconfig/rc-inetd/nntpd
%{_mandir}/man8/*
