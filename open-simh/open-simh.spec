%global gitdate 20261120

Name:           open-simh
Version:        4.1.0
Release:        2.%{gitdate}%{?dist}
Summary:        Open SIMH PDP-11 simulator, with VT11 display for use as a GT40
License:        MIT
URL:            https://github.com/open-simh/simh
# ./make-git-snapshot.sh
Source0:        %{name}-%{gitdate}.tar.bz2
Source1:        make-git-snapshot.sh
Source2:        gt40.ini
Source3:        gt40

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  libedit-devel
BuildRequires:  libpcap-devel
BuildRequires:  libpng-devel
BuildRequires:  pcre2-devel
BuildRequires:  zlib-devel

# gt40.ini boots the GT40 bootstrap ROM image (bootvt.img) from the PiDP-10
# client support.
Requires:       pidp10-clients

%description
The PDP-11 simulator from Open SIMH, built with SDL2 video so that the VT11
display works.  This package is mainly here so the PDP-11 can run as a GT40
graphics terminal for the PiDP-10.

The simulator is installed as open-simh-pdp11, because other packages
already ship a /usr/bin/pdp11.

Run "gt40 HOST [PORT]" to boot the GT40 ROM in terminal mode on a DL11
line connected to HOST:PORT (default 10019, the ITS GT40 line on the
PiDP-10).  The startup file it uses is %{_datadir}/%{name}/gt40.ini; its
settings follow the pidp10 package's gt40.simh.

%prep
%autosetup -n %{name}-%{gitdate} -p1

%build
# The makefile adds -Werror unless WARNINGS=ALLOWED, and its tests are not
# wanted in the build.  OPTIMIZE and LDFLAGS_O carry the distribution flags.
%make_build pdp11 \
    TESTS=0 \
    WARNINGS=ALLOWED \
    OPTIMIZE="%{optflags}" \
    LDFLAGS_O="%{build_ldflags}"

%install
install -Dm755 BIN/pdp11 %{buildroot}%{_bindir}/open-simh-pdp11
install -Dm755 %{SOURCE3} %{buildroot}%{_bindir}/gt40
install -Dm644 %{SOURCE2} %{buildroot}%{_datadir}/%{name}/gt40.ini

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/open-simh-pdp11
%{_bindir}/gt40
%{_datadir}/%{name}/

%changelog
* Fri Nov 20 2026 Dennis Gilmore <dennis@ausil.us> - 4.1.0-2.20261120
- Require pidp10-clients for the GT40 bootstrap ROM

* Fri Nov 20 2026 Dennis Gilmore <dennis@ausil.us> - 4.1.0-1.20261120
- Initial packaging: the pdp11 simulator as open-simh-pdp11, with a gt40
  launcher
