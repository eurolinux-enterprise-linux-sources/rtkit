%global _hardened_build 1

Name:             rtkit
Version:          0.11
Release:          10%{?dist}
Summary:          Realtime Policy and Watchdog Daemon
Group:            System Environment/Base
# The daemon itself is GPLv3+, the reference implementation for the client BSD
License:          GPLv3+ and BSD
URL:              http://git.0pointer.de/?p=rtkit.git
Requires:         dbus
Requires:         polkit
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    dbus-devel >= 1.2
BuildRequires:    libcap-devel
BuildRequires:    polkit-devel
BuildRequires:    autoconf automake libtool
Source0:          http://0pointer.de/public/%{name}-%{version}.tar.xz
Patch1:           0001-build-Link-against-lrt.patch
Patch2:           0001-SECURITY-Pass-uid-of-caller-to-polkit.patch
Patch3:           0001-systemd-remove-unsupported-option-ControlGroup.patch

%description
RealtimeKit is a D-Bus system service that changes the
scheduling policy of user processes/threads to SCHED_RR (i.e. realtime
scheduling mode) on request. It is intended to be used as a secure
mechanism to allow real-time scheduling to be used by normal user
processes.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
autoreconf -fvi
%configure --with-systemdsystemunitdir=/usr/lib/systemd/system
make %{?_smp_mflags}
./rtkit-daemon --introspect > org.freedesktop.RealtimeKit1.xml

%install
make install DESTDIR=$RPM_BUILD_ROOT
install -D org.freedesktop.RealtimeKit1.xml $RPM_BUILD_ROOT/%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml

%pre
getent group rtkit >/dev/null 2>&1 || groupadd \
        -r \
        -g 172 \
        rtkit
getent passwd rtkit >/dev/null 2>&1 || useradd \
        -r -l \
        -u 172 \
        -g rtkit \
        -d /proc \
        -s /sbin/nologin \
        -c "RealtimeKit" \
        rtkit
:;

%post
%systemd_post rtkit-daemon.service
dbus-send --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig >/dev/null 2>&1 || :

%preun
%systemd_preun rtkit-daemon.service

%postun
%systemd_postun

%files
%defattr(0644,root,root,0755)
%doc README GPL LICENSE rtkit.c rtkit.h
%attr(0755,root,root) %{_sbindir}/rtkitctl
%attr(0755,root,root) %{_libexecdir}/rtkit-daemon
%{_datadir}/dbus-1/system-services/org.freedesktop.RealtimeKit1.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.RealtimeKit1.xml
%{_datadir}/polkit-1/actions/org.freedesktop.RealtimeKit1.policy
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.RealtimeKit1.conf
%{_prefix}/lib/systemd/system/rtkit-daemon.service
%{_mandir}/man8/*

%changelog
* Thu Sep 11 2014 Michal Sekletar <msekleta@redhat.com> - 0.11-10
- turn on hardening flags (#1092529)

* Tue Sep 09 2014 Michal Sekletar <msekleta@redhat.com> - 0.11-9
- remove unsupported option ControlGroup for systemd unit file (#1095607)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.11-8
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.11-7
- Mass rebuild 2013-12-27

* Mon Sep 23 2013 Colin Walters <walters@redhat.com> - 0.11-6
- CVE-2013-4326
  Resolves: #1005140

* Thu Aug 22 2013 Colin Walters <walters@verbum.org> - 0.11-5
- Add patch to make this build again

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 14 2012 Lennart Poettering <lpoetter@redhat.com> - 0.11-3
- Make use of the new systemd macros

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Lennart Poettering <lpoetter@redhat.com> - 0.11-1
- New upstream release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Feb 17 2011 Lennart Poettering <lpoetter@redhat.com> - 0.10-1
- new upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug  4 2010 Lennart Poettering <lpoetter@redhat.com> - 0.9-2
- Convert systemd-install to systemctl

* Tue Jul 13 2010 Lennart Poettering <lpoetter@redhat.com> - 0.9-1
- New upstream release

* Tue Jun 29 2010 Lennart Poettering <lpoetter@redhat.com> - 0.8-1
- New upstream release

* Fri Dec 18 2009 Lennart Poettering <lpoetter@redhat.com> - 0.5-1
- New release
- By default don't demote unknown threads
- Make messages less cute
- Fixes 530582

* Wed Aug 5 2009 Lennart Poettering <lpoetter@redhat.com> - 0.4-1
- New release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 2 2009 Lennart Poettering <lpoetter@redhat.com> - 0.3-1
- New release

* Thu Jun 17 2009 Lennart Poettering <lpoetter@redhat.com> - 0.2-1
- Initial packaging
