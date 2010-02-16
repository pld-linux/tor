Summary:	Anonymizing overlay network for TCP (The onion router)
Summary(pl.UTF-8):	Sieć nakładkowa dla TCP zapewniająca anonimowość (router cebulowy)
Name:		tor
Version:	0.2.1.23
Release:	1
License:	BSD-like
Group:		Networking/Daemons
Source0:	http://www.torproject.org/dist/%{name}-%{version}.tar.gz
# Source0-md5:	2e0bf3dbb83bbaadaa99d1dfe59c75f7
Source1:	%{name}.logrotate
Source2:	%{name}.init
Source3:	%{name}.sysconfig
URL:		http://www.torproject.org/
# http://archives.seul.org/or/announce/Feb-2009/msg00000.html
BuildRequires:	libevent-devel >= 1.1
BuildRequires:	openssl-devel >= 0.9.6
BuildRequires:	rpm-build >= 4.0
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	group(tor)
Provides:	user(tor)
Conflicts:	logrotate < 3.7-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tor is a connection-based low-latency anonymous communication system.

This package provides the "tor" program, which serves as both a client
and a relay node. Scripts will automatically create a "tor" user and
group, and set tor up to run as a daemon when the system is rebooted.

Applications connect to the local Tor proxy using the SOCKS protocol.
The local proxy chooses a path through a set of relays, in which each
relay knows its predecessor and successor, but no others. Traffic
flowing down the circuit is unwrapped by a symmetric key at each
relay, which reveals the downstream relay.

Warnings: Tor does no protocol cleaning. That means there is a danger
that application protocols and associated programs can be induced to
reveal information about the initiator. Tor depends on Privoxy and
similar protocol cleaners to solve this problem. This is alpha code,
and is even more likely than released code to have anonymity-spoiling
bugs. The present network is very small -- this further reduces the
strength of the anonymity provided. Tor is not presently suitable for
high-stakes anonymity.

%description -l pl.UTF-8
Tor to oparty na połączeniach system anonimowej komunikacji o małych
opóźnieniach.

Ten pakiet dostarcza program "tor", służący zarówno jako klient, jak i
węzeł przekaźnikowy. Skrypty automatycznie tworzą użytkownika i grupę
"tor" i konfigurują tora do działania jako demon po uruchomieniu
systemu.

Aplikacje łączą się z lokalnym proxy Tor przy użyciu protokołu SOCKS.
Lokalne proxy wybiera ścieżkę poprzez zbiór przekaźników, z których
każdy zna swojego poprzednika i następnika, ale żadnego więcej. Ruch
przychodzący jest rozpakowywany przy użyciu klucza symetrycznego na
każdym przekaźniku, który odsłania kolejny przekaźnik.

Uwaga: Tor nie oczyszcza protokołów. Oznacza to, że istnieje
niebezpieczeństwo, że protokoły aplikacji i powiązane programy mogą
odkryć informacje o pochodzeniu. Tor polega na Privoxy i podobnych
oczyszczaczach protokołów w celu rozwiązania tego problemu. To jest
kod alpha, więc może mieć więcej błędów psujących anonimowość niż kod
wydany. Obecna sieć jest bardzo mała - co w dalszym stopniu ogranicza
zapewnianą anonimowość. Tor aktualnie nie nadaje się do zadań
wymagających anonimowości na wysoką stawkę.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/torrc{.sample,}
install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -D %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d $RPM_BUILD_ROOT/var/lib/%{name}
install -d $RPM_BUILD_ROOT/var/run/%{name}
install -d $RPM_BUILD_ROOT/var/log/{,archive/}%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 156 tor
%useradd  -u 156 -r -d /var/lib/tor -s /bin/false -c "Tor" -g tor tor

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove  tor
	%groupremove tor
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS INSTALL LICENSE README ChangeLog doc/HACKING doc/TODO
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man?/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %attr(750,root,tor) %{_sysconfdir}/%{name}
%attr(640,root,tor)  %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%dir %attr(750,root,tor) /var/lib/%{name}
%dir %attr(750,root,tor) /var/run/%{name}
%dir %attr(750,root,tor) /var/log/%{name}
%dir %attr(750,root,tor) /var/log/archive/%{name}
