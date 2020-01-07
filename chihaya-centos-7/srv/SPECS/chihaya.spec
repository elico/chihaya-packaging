%define release_number %(echo $RELEASE_NUMBER)
%define version_number %(echo $VERSION_NUMBER)

Name:     chihaya
Version:  %{version_number}
Release:  %{release_number}%{?dist}
Summary:  Chihaya Bittorrent Tracker Written in GoLang
Epoch:    7
Packager: Eliezer Croitoru <eliezer@ngtech.co.il>
Vendor:   NgTech Ltd
License:  3 Clause BSD
Group:    System Environment/Daemons
URL:      https://github.com/chihaya/chihaya/tags
Source0:  chihaya.service
Source1:  chihaya
Source2:  chihaya.sysconfig
Source3:  example_config.yaml
Source4:  chihaya-add-firewalld-service.sh

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Requires: systemd-units
# Required to allow debug package auto creation
BuildRequires:  redhat-rpm-config
BuildRequires:  systemd-units

# Required to validate auto requires AutoReqProv: no
## aaaAutoReqProv: no

%description
Chihaya an opensource and public tracker written in GoLang.
An example command to scrap the stats from the service:
 curl http://localhost:6880/stats?flatten=1
** Use Firewall since the service is open by default for to anyone!!

%prep
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
install -m 644 %{SOURCE0} ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_bindir}/chihaya
install -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/chihaya
install -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/chihaya.yaml
install -m 644 %{SOURCE4} ${RPM_BUILD_ROOT}%{_sbindir}/chihaya-add-firewalld-service.sh

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%attr(755,root,root) %dir %{_sysconfdir}
%attr(755,root,root) %dir %{_sysconfdir}/sysconfig
%config(noreplace) %{_sysconfdir}/sysconfig/chihaya
%config(noreplace) %{_sysconfdir}/chihaya.yaml
%attr(755,root,root) %{_bindir}/chihaya
%attr(755,root,root) %{_sbindir}/chihaya-add-firewalld-service.sh

%{_unitdir}/chihaya.service

%pre
if ! /usr/bin/getent group chihaya >/dev/null 2>&1; then
  /usr/sbin/groupadd -g 5005 chihaya
fi

if ! /usr/bin/getent passwd chihaya >/dev/null 2>&1 ; then
  /usr/sbin/useradd -g 5005 -u 5005 -m -d /home/chihaya -r -s /sbin/nologin chihaya >/dev/null 2>&1 || exit 1
fi

%post
echo "** Use Firewall since the service is open by default for to anyone!!"
%systemd_post chihaya.service

%preun
%systemd_preun chihaya.service

%postun
%systemd_postun_with_restart chihaya.service

%changelog
* Tue Jan 07 2020 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 2.0.0 Stable.
