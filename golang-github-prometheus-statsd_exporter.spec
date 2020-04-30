%global repo    statsd_exporter
%undefine _missing_build_ids_terminate_build

Name:           golang-github-prometheus-statsd_exporter
Version:        0.15.0
Release:        3%{?dist}
Summary:        statsd_exporter receives StatsD-style metrics and exports them as Prometheus metrics.
License:        ASL 2.0
URL:            https://github.com/prometheus/statsd_exporter
Source0:        https://github.com/prometheus/statsd_exporter/archive/master.tar.gz
Source1:        statsd_exporter.service
Source2:        statsd_exporter

# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires: golang >= 1.6
BuildRequires: golang-github-prometheus-promu
BuildRequires: systemd

%description
With StatsD To pipe metrics from an existing StatsD environment into Prometheus, configure StatsD's repeater backend to repeat all received metrics to a statsd_exporter process. This exporter translates StatsD metrics to Prometheus metrics via configured mapping rules.

%package -n statsd_exporter
Summary:        statsd_exporter receives StatsD-style metrics and exports them as Prometheus metrics.
%{?systemd_requires}

%description -n statsd_exporter
With StatsD To pipe metrics from an existing StatsD environment into Prometheus, configure StatsD's repeater backend to repeat all received metrics to a statsd_exporter process. This exporter translates StatsD metrics to Prometheus metrics via configured mapping rules.

This package contains the statsd exporter.

%prep
%setup -q -n %{repo}-master

%build
#sed -i "s/    flags: -mod=vendor -a -tags 'netgo static_build'/    flags: -mod=vendor -a -tags netgo static_build\n    ldflags:\n       -compressdwarf=false/" .promu.yml
sed -i "s/    flags: -mod=vendor -a -tags 'netgo static_build'/    flags: -mod=vendor -a -tags 'netgo static_build'\n    ldflags:\n       -compressdwarf=false\n    binaries:\n      - name: statsd_exporter/" .promu.yml
GO111MODULE=on promu build -v

%install
install -d %{buildroot}%{_bindir}
install -p -m 0755 statsd_exporter %{buildroot}%{_bindir}/statsd_exporter
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/statsd_exporter
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/statsd_exporter.service

%post -n statsd_exporter
%systemd_post statsd_exporter.service

%preun -n statsd_exporter
%systemd_preun statsd_exporter.service

%postun -n statsd_exporter
%systemd_postun_with_restart statsd_exporter.service

%files -n statsd_exporter
%license LICENSE
%doc     README.md
%doc     .promu.yml
%{_bindir}/statsd_exporter
%{_sysconfdir}/sysconfig/statsd_exporter
%{_unitdir}/statsd_exporter.service

%changelog
* Thu Apr 30 2020 Daniel Pawlik <dpawlik@redhat.com> - 0.15.0-1
- Initial version
