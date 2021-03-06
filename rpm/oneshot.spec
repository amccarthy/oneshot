# we can't use %include for files in the source tarballs, so redefine the macros for now
%define _oneshotdir %{_libdir}/oneshot.d
%define _default_uid %(grep "^UID_MIN" /etc/login.defs |  tr -s " " | cut -d " " -f2)
%define _system_groupadd() getent group %{1} >/dev/null || groupadd -r %{1}

Name: oneshot
Version: 0.3.1
Release: 1
Summary: Hooks run on first start
BuildArch: noarch
Group: System/Base
License: GPLv2
Source0: %{name}-%{version}.tar.gz
URL: https://github.com/nemomobile/oneshot
BuildRequires: qt5-qmake, grep, systemd
Requires: systemd-user-session-targets
Requires(pre): /usr/bin/getent, /usr/sbin/groupadd
Requires: /usr/bin/getent, /bin/ln, /bin/touch, /bin/sed, /bin/grep, /usr/sbin/usermod
Requires: /etc/login.defs

%description
%{summary}.

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/rpm/*
%attr (755, -, -) %{_bindir}/*
%{_sysconfdir}/oneshot.d/
%dir %{_sysconfdir}/oneshot.d/
%dir %{_sysconfdir}/oneshot.d/0
%dir %{_sysconfdir}/oneshot.d/0/late
%dir %attr(775, -, oneshot) %{_sysconfdir}/oneshot.d/default/
%dir %attr(775, -, oneshot) %{_sysconfdir}/oneshot.d/default/late
%dir %{_sysconfdir}/oneshot.d/group.d
%dir %{_sysconfdir}/oneshot.d/preinit
%dir %{_oneshotdir}
%attr (755, -, -) %{_oneshotdir}/*
%{_libdir}/systemd/user/oneshot-user.service
%{_libdir}/systemd/user/oneshot-user-late.service
%{_libdir}/systemd/user/pre-user-session.target.wants/oneshot-user.service
%{_libdir}/systemd/user/post-user-session.target.wants/oneshot-user-late.service
%{_unitdir}/oneshot-root.service
%{_unitdir}/oneshot-root-late.service
%{_unitdir}/multi-user.target.wants/oneshot-root.service
%{_unitdir}/graphical.target.wants/oneshot-root-late.service

%pre
%_system_groupadd oneshot

%prep
%setup -q

%build
ls %{_builddir}/%{name}-%{version}/macros/
BINDIR=%{_bindir} ONESHOTDIR=%{_oneshotdir} SERVICEDIR=%{_unitdir} USERSERVICEDIR=%{_libdir}/systemd/user qmake -qt=5

%install
make INSTALL_ROOT=%{buildroot} install
install -d %{buildroot}%{_sysconfdir}/oneshot.d/0/late
install -d %{buildroot}%{_sysconfdir}/oneshot.d/default/late
install -d %{buildroot}%{_sysconfdir}/oneshot.d/group.d/
install -d %{buildroot}%{_sysconfdir}/oneshot.d/preinit/

mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
mkdir -p %{buildroot}%{_unitdir}/graphical.target.wants
mkdir -p %{buildroot}%{_libdir}/systemd/user/pre-user-session.target.wants
mkdir -p %{buildroot}%{_libdir}/systemd/user/post-user-session.target.wants
ln -sf ../oneshot-root.service %{buildroot}%{_unitdir}/multi-user.target.wants/
ln -sf ../oneshot-root-late.service %{buildroot}%{_unitdir}/graphical.target.wants/
ln -sf ../oneshot-user.service %{buildroot}%{_libdir}/systemd/user/pre-user-session.target.wants/
ln -sf ../oneshot-user-late.service %{buildroot}%{_libdir}/systemd/user/post-user-session.target.wants/
ln -sf ./default %{buildroot}%{_sysconfdir}/oneshot.d/%{_default_uid}


%post
%{_bindir}/groupadd-user oneshot
