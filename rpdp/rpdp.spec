Name:           rpdp
Version:        1.0
Release:        4%{?dist}
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
Requires:       open-simh
# sty (the Teletype with sounds) comes from the PiDP-10 client support.
Requires:       pidp10-clients
Recommends:     lxterminal

%description
rpdp turns a desktop, laptop or second Raspberry Pi into terminals for a
PiDP-10, PiDP-11, PiDP-8 or PiDP-1 elsewhere on the network: Knight TV, DEC VT-52, Datapoint 3300,
Tektronix 4010, Imlac, GT40 and Teletype consoles.  Run `rpdp vt52`, `rpdp tvcon`
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
* Fri Nov 20 2026 Dennis Gilmore <dennis@ausil.us> - 1.0-4
- Add rpdp pdp6, which attaches to the PiDP-10's PDP-6 console session
- Imlac on the PiDP-10 is ITS line 7, port 10016 (was 10003)
- Accept sim, console and sty, the names pdp uses on the PiDP-10

* Fri Nov 20 2026 Dennis Gilmore <dennis@ausil.us> - 1.0-3
- Require pidp10-clients for sty and the Teletype sounds

* Fri Nov 20 2026 Dennis Gilmore <dennis@ausil.us> - 1.0-2
- Add rpdp gt40, the GT40 terminal from open-simh (PORT_GT40, default 10019)

* Sat Nov 07 2026 Dennis Gilmore <dennis@ausil.us> - 1.0-1
- Initial packaging of the rpdp launcher scripts
