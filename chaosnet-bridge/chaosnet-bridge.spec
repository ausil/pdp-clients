%define gitdate 20261106

Name:           chaosnet-bridge
Version:        1.0
Release:        1.%{gitdate}%{?dist}
Summary:        This program is a bridge between Chaosnet implementations

License:        Apache-2.0
URL:            https://github.com/bictorv/chaosnet-bridge/
# tarball is a git snapshot make by running make-git-snapshot.sh
Source0:        chaosnet-bridge-%{gitdate}.tar.bz2
Source1:        make-git-snapshot.sh

Patch0:         0001-ensure-CFLAGS-can-be-overridden.patch

BuildRequires:  gcc make openssl-devel

%description
This program is a bridge between Chaosnet implementations. It supports
different link layer implementations:

Chaos-over-Ethernet (protocol nr 0x0804, cf
https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml)
Chaos-over-UDP (encapsulation used by e.g. the klh10/its pdp10 emulator,
 see https://its.victor.se/wiki/ch11)
Chaos-over-Unix-sockets (used by the usim CADR emulator,
see http://www.unlambda.com/cadr/)
Chaos-over-TLS (see below)
Chaos-over-IP (using IP protocol 16, cf
https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)

It also implements the transport layer of Chaosnet (using any of the above
 link layers).

%prep
%autosetup -p1 -n %{name}-%{gitdate}


%build
%make_build


%install
install -Dm 0755 src/cbridge %{buildroot}%{_bindir}/cbridge
install -Dm 0755 tools/hostat %{buildroot}%{_bindir}/hostat
install -Dm 0755 tools/finger %{buildroot}%{_bindir}/finger


%files
%license LICENSE.txt
%doc README.md COPYRIGHT.md doc/
%{_bindir}/cbridge
%{_bindir}/hostat
%{_bindir}/finger

%changelog
* Fri Nov 06 2026 Dennis Gilmore <dennis@ausil.us> - 1.0-1.20261106
- initial packaging
