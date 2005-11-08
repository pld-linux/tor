Summary:	Anonymizing overlay network for TCP (The onion router)
Summary(pl):	Sieæ nak³adkowa dla TCP zapewniaj±ca anonimowo¶æ (router cebulowy)
Name:		tor
Version:	0.1.0.15
Release:	0.2
License:	BSD-like
Group:		Networking/Daemons
Source0:	http://tor.eff.org/dist/%{name}-%{version}.tar.gz
# Source0-md5:	b2f1002da96ebfbfac7edf2272733967
Source1:	%{name}.logrotate
Source2:	%{name}.init
Source3:	%{name}.sysconfig
URL:		http://tor.eff.org/
BuildRequires:	libevent-devel
BuildRequires:	openssl-devel >= 0.9.6
BuildRequires:	rpm-build >= 4.0
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tor is a connection-based low-latency anonymous communication system.

This package provides the "tor" program, which serves as both a client
and a relay node. Scripts will automatically create a "tor"
user and group, and set tor up to run as a daemon when the system is
rebooted.

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

%description -l pl
Tor to oparty na po³±czeniach system anonimowej komunikacji o ma³ych
opó¼nieniach.

Ten pakiet dostarcza program "tor", s³u¿±cy zarówno jako klient, jak i
wêze³ przeka¼nikowy. Skrypty automatycznie tworz± u¿ytkownika i grupê
"tor" i konfiguruj± tora do dzia³ania jako demon po uruchomieniu
systemu.

Aplikacje ³±cz± siê z lokalnym proxy Tor przy u¿yciu protoko³u SOCKS.
Lokalne proxy wybiera ¶cie¿kê poprzez zbiór przeka¼ników, z których
ka¿dy zna swojego poprzednika i nastêpnika, ale ¿adnego wiêcej. Ruch
przychodz±cy jest rozpakowywany przy u¿yciu klucza symetrycznego na
ka¿dym przeka¼niku, który ods³ania kolejny przeka¼nik.

Uwaga: Tor nie oczyszcza protoko³ów. Oznacza to, ¿e istnieje
niebezpieczeñstwo, ¿e protoko³y aplikacji i powi±zane programy mog±
odkryæ informacje o pochodzeniu. Tor polega na Privoxy i podobnych
oczyszczaczach protoko³ów w celu rozwi±zania tego problemu. To jest
kod alpha, wiêc mo¿e mieæ wiêcej b³êdów psuj±cych anonimowo¶æ ni¿ kod
wydany. Obecna sieæ jest bardzo ma³a - co w dalszym stopniu ogranicza
zapewnian± anonimowo¶æ. Tor aktualnie nie nadaje siê do zadañ
wymagaj±cych anonimowo¶ci na wysok± stawkê.

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
install -d $RPM_BUILD_ROOT/var/log/{,archiv/}%{name}

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
	#%{__rm} -f ${_localstatedir}/lib/%{name}/cached-directory
	#%{__rm} -f ${_localstatedir}/lib/%{name}/bw_accounting
	#%{__rm} -f ${_localstatedir}/lib/%{name}/control_auth_cookie
	#%{__rm} -f ${_localstatedir}/lib/%{name}/router.desc
	#%{__rm} -f ${_localstatedir}/lib/%{name}/fingerprint
fi

%postun
if [ "$1" = "0" ]; then
	%userremove  tor
	%groupremove tor
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS INSTALL LICENSE README ChangeLog doc/HACKING doc/TODO doc/FAQ
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man?/*
%attr(755,root,root) /etc/rc.d/init.d/%{name}
%dir %attr(750,root,tor) %{_sysconfdir}/%{name}
%attr(640,root,tor)  %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%dir %attr(750,root,tor) /var/lib/%{name}
%dir %attr(750,root,tor) /var/run/%{name}
%dir %attr(750,root,tor) /var/log/%{name}
%dir %attr(750,root,tor) /var/log/archiv/%{name}
