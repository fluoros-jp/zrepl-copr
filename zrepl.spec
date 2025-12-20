# Global meta data
Version:          1.1.0
%global common_description %{expand:
zrepl is a one-stop, integrated solution for ZFS replication.}

Name:             zrepl
Release:          1%{?dist}
Summary:          One-stop, integrated solution for ZFS replication
License:          MIT
URL:              https://github.com/dsh2dsh/zrepl
Source:		  https://github.com/dsh2dsh/zrepl/releases/download/v1.1.0/zrepl_1.1.0_linux_amd64.tar.gz
BuildRequires:    systemd, git, wget, make
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
%{common_description}

%global debug_package %{nil}

%prep
rm -rf %{buildroot}
%autosetup -c

%build
mkdir artifacts
mv zrepl artifacts/zrepl

# Generate complation for bash and zsh
artifacts/zrepl gencompletion bash "artifacts/bash_completion"
artifacts/zrepl gencompletion zsh "artifacts/_zrepl.zsh_completion"

# Correct the path in the systemd unit file
sed s:/usr/local/bin/:%{_bindir}/:g dist/systemd/zrepl.service > artifacts/zrepl.service

# Generate the default configuration file
sed s:/sbin/zfs:/usr/sbin/zfs:g dist/freebsd/etc/zrepl/zrepl.yml > artifacts/zrepl.yml

%install
install -Dm 0755 artifacts/zrepl                        %{buildroot}%{_bindir}/zrepl
install -Dm 0644 artifacts/zrepl.service       %{buildroot}%{_unitdir}/zrepl.service
install -Dm 0644 artifacts/_zrepl.zsh_completion        %{buildroot}%{_datadir}/zsh/site-functions/_zrepl
install -Dm 0644 artifacts/bash_completion              %{buildroot}%{_datadir}/bash-completion/completions/zrepl
install -Dm 0644 artifacts/zrepl.yml           %{buildroot}%{_sysconfdir}/zrepl/zrepl.yml
install -Dm 0644 dist/freebsd/etc/zrepl/keys.yaml       %{buildroot}%{_sysconfdir}/zrepl/keys.yaml

%post
%systemd_post zrepl.service


%preun
%systemd_preun zrepl.service


%postun
%systemd_postun_with_restart zrepl.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/zrepl
%config %{_unitdir}/zrepl.service
%dir %{_sysconfdir}/zrepl
%config %{_sysconfdir}/zrepl/zrepl.yml
%config %{_sysconfdir}/zrepl/keys.yaml
%{_datadir}/zsh/site-functions/_zrepl
%{_datadir}/bash-completion/completions/zrepl

%changelog
* Sat Dec 20 2025 Fluoros <fluoros@fluoroserve.jp> 1.1.0-1
- Initial release of zrepl v1.1.0
* Mon Nov 3 2025 Fluoros <fluoros@fluoroserve.jp> 1.0.0-1
- Initial release of zrepl v1.0.0
* Sat Aug 2 2025 Fluoros <fluoros@fluoroserve.jp> 0.9.11-1
- Initial release of zrepl v0.9.11
* Sat May 3 2025 Fluoros <fluoros@fluoroserve.jp> 0.9.10-1
- Initial release of zrepl v0.9.10
