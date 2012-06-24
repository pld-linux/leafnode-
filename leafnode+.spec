Summary:	NNTP server for small sites
Summary(pl):	Serwer NNTP przeznaczony dla niedu�ych serwer�w
Name:		leafnode+
Version:	2.10
Release:	1
License:	free to use, modify and distribute
Group:		Networking/Daemons
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
Leafnode+ to zestaw program�w umo�liwiaj�cych stworzenie niewielkiego
serwera NNTP dla niewielkiej liczby u�ytkownik�w, bez potrzeby
posiadania szybkiego ��cza do sieci. Leafnode+ zosta� napisany na
podstawie programu leafnode-1.4.

%prep
%setup -q
%patch0 -p1

%build
make 	LDFLAGS="-s" CFLAGS="$RPM_OPT_FLAGS" \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_sysconfdir}/%{name} \
	SPOOLDIR=%{_var}/spool/news

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT/{%{_sysconfdir}/%{name},/etc/sysconfig/rc-inetd}

make	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_sysconfdir}/%{name} \
	SPOOLDIR=%{_var}/spool/news \
	installall

touch $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/groupinfo
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config.example

gzip -9nf README COPYING FAQ Changes config.example \
	$RPM_BUILD_ROOT%{_mandir}/man8/*

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/nntpd

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
%{_mandir}/man8/*
%config %dir %attr(750,news,news) %{_sysconfdir}/leafnode+
%ghost %attr(640,news,news) %{_sysconfdir}/leafnode+/groupinfo
%attr(750,news,news) %{_sbindir}/*
%attr(2750,news,news) %{_var}/spool/news
%attr(640,root,root) /etc/sysconfig/rc-inetd/nntpd
