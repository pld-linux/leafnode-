Summary:	NNTP server for small sites
Summary(pl):	Serwer NNTP przeznaczony dla niedu¿ych serwerów
Name:		leafnode+
Version:	2.10
Release:	1
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Copyright:	free to use, modify and distribute
URL:		http://www.io.com/~kazushi/leafnode+/
Source0:	ftp://hiroshima.isdn.uiuc.edu/leafnode+/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Patch0:		%{name}-DESTDIR.patch
Requires:	rc-inetd
Requires:	inetdaemon
Provides:	nntpserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Leafnode+ is a USENET software package designed for small sites, with a few
tens of readers and only a slow link to the net. Leafnode+ has been derived
from leafnode-1.4.

%description -l pl
Leafnode+ to zestaw programów umo¿liwiaj±cych stworzenie niewielkiego
serwera NNTP dla niewielkiej liczby u¿ytkowników, bez potrzeby posiadania
szybkiego ³±cza do sieci. Leafnode+ zosta³ napisany na podstawie programu
leafnode-1.4.

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

%files
%defattr(644,root,root,755)
%doc *.gz
%{_mandir}/man8/*
%config %dir %attr(750,news,news) %{_sysconfdir}/leafnode+
%ghost %attr(640,news,news) %{_sysconfdir}/leafnode+/groupinfo
%attr(750,news,news) %{_sbindir}/*
%attr(2750,news,news) %{_var}/spool/news
%attr(640,root,root) /etc/sysconfig/rc-inetd/nntpd
