Name:           rpdp
Version:        1.0
Release:        1%{?dist}
Summary:        Launch terminal simulators connected to a remote PiDP-10
License:        MIT
URL:            https://github.com/obsolescence/rpdp
BuildArch:      noarch
Source0:        rpdp
Source1:        rpdp.conf
Source2:        ssv22.iml
Source3:        LICENSE

# Terminal programs that `rpdp` starts.
Requires:       openssh-clients
Requires:       telnet
Requires:       tvcon
Requires:       vt05
Requires:       terminal-simulator
Requires:       p7sim
Requires:       tek4010
Requires:       sImlac
# sty (the Teletype with sounds) comes from the main PiDP-10 package.
Recommends:     pidp10
Recommends:     lxterminal

%description
rpdp turns a desktop, laptop or second Raspberry Pi into terminals for a
PiDP-10, PiDP-11, PiDP-8 or PiDP-1 elsewhere on the network: Knight TV, DEC VT-52, Datapoint 3300,
Tektronix 4010, Imlac and Teletype consoles.  Run `rpdp vt52`, `rpdp tvcon`
and so on, after setting the PiDP-10's host name and user in /etc/rpdp.conf.

This is the same interface as the rpdp scripts from obsolescence/rpdp, but
uses the terminal programs packaged for the distribution instead of the
binaries bundled in that repository.

%prep
cp -p %{SOURCE3} .

%build

%install
install -Dm755 %{SOURCE0} %{buildroot}%{_bindir}/rpdp
install -Dm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpdp.conf
install -Dm644 %{SOURCE2} %{buildroot}%{_datadir}/rpdp/ssv22.iml

%files
%license LICENSE
%{_bindir}/rpdp
%config(noreplace) %{_sysconfdir}/rpdp.conf
%{_datadir}/rpdp/

%changelog
* Sat Nov 07 2026 Dennis Gilmore <dennis@ausil.us> - 1.0-1
- Initial packaging of the rpdp launcher scripts
