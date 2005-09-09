Summary:	Anonymizing overlay network for TCP (The onion router)
Name:		tor
Version:	0.1.0.14
Release:	0.1
Source0:	http://tor.eff.org/dist/%{name}-%{version}.tar.gz
# Source0-md5:	f210023a97b5b97d1517a47f587876b9
Source1:	%{name}.logrotate
URL:		http://tor.eff.org/
Group:		Networking/Daemons
License:	BSD-like
BuildRequires:	libevent-devel
BuildRequires:	openssl-devel >= 0.9.6
BuildRequires:	rpm-build >= 4.0
Requires(pre):	shadow-utils, /usr/bin/id, /bin/date, /bin/sh
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

%prep
%setup -q -n %{name}-%{version}

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/torrc{.sample,}
install -D contrib/tor.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -D %{SOURCE1}     $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

%{__mkdir_p} $RPM_BUILD_ROOT/var/lib/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT/var/run/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT/var/log/{,archiv/}%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 156 tor
%useradd  -u 156 -r -d /var/lib/tor -s /bin/false -c "Tor" -g tor tor
[ -f %{_initrddir}/%{name}  ] && /sbin/service %{name} stop

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

%files
%defattr(644,root,root,755)
%doc AUTHORS INSTALL LICENSE README ChangeLog doc/HACKING doc/TODO doc/FAQ
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man?/*
%config %{_initrddir}/%{name}
%dir %attr(755,root,tor) %{_sysconfdir}/%{name}/
%attr(644,root,tor)  %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%dir %attr(750,root,tor) /var/lib/%{name}
%dir %attr(750,root,tor) /var/run/%{name}
%dir %attr(750,root,tor) /var/log/{,archiv/}%{name}
