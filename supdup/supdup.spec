%global gitdate 20261106

Name:           supdup
Version:        1.0
Release:        1.%{gitdate}%{?dist}
Summary:        SUPDUP protocol client for ITS and other PDP-10 systems
# COPYING is a 2001 email from the author permitting redistribution; there
# is no standard licence.  Fine for COPR, needs clarifying for Fedora proper.
License:        LicenseRef-supdup-redistribution
URL:            https://github.com/PDP-10/supdup
# ./make-git-snapshot.sh
Source0:        %{name}-%{gitdate}.tar.bz2
Source1:        make-git-snapshot.sh

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(ncurses)

%description
supdup is a client for the SUPDUP (Super Duper TELNET) remote display
protocol used by ITS and other PDP-10 systems.  It connects over TCP/IP
or, through a Chaosnet bridge such as cbridge, over Chaosnet.

%prep
%autosetup -n %{name}-%{gitdate} -p1

%build
# The server (supdupd) is marked experimental upstream; build the client only.
%make_build supdup CFLAGS="%{optflags} $(pkg-config --cflags ncurses)" \
    LDFLAGS="%{build_ldflags}"

%install
install -Dm755 supdup %{buildroot}%{_bindir}/supdup

%files
%license COPYING
%doc README.md INFO
%{_bindir}/supdup

%changelog
* Fri Nov 06 2026 Dennis Gilmore <dennis@ausil.us> - 1.0-1.20261106
- Initial packaging
