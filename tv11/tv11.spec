%global gitdate 20261106

Name:           tv11
Version:        1.0
Release:        1.%{gitdate}%{?dist}
Summary:        Knight TV emulator for ITS
License:        MIT
URL:            https://github.com/aap/tv11
# ./make-git-snapshot.sh
Source0:        %{name}-%{gitdate}.tar.bz2
Source1:        make-git-snapshot.sh

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(sdl2)

%description
tv11 emulates the PDP-11 that drove the Knight TV display system on
MIT's ITS.  It talks to a PDP-10 emulator over the TEN11 interface and
serves the TV displays to tvcon clients over the network.

%package -n tvcon
Summary:        Knight TV console client for tv11

%description -n tvcon
tvcon is the SDL2 client for tv11.  It shows one Knight TV screen and
sends keyboard input back to ITS.

%prep
%autosetup -n %{name}-%{gitdate} -p1

%build
%make_build CFLAGS="%{optflags} -Wall -Wextra -Wno-parentheses" \
    LDFLAGS="%{build_ldflags}"
%{__cc} %{optflags} $(pkg-config --cflags sdl2) -o tvcon/tvcon tvcon/tvcon.c \
    %{build_ldflags} $(pkg-config --libs sdl2) -lpthread

%install
install -Dm755 tv11 %{buildroot}%{_bindir}/tv11
install -Dm755 tvcon/tvcon %{buildroot}%{_bindir}/tvcon

%files
%license LICENSE
%doc README.md
%{_bindir}/tv11

%files -n tvcon
%license LICENSE
%doc README.md
%{_bindir}/tvcon

%changelog
* Fri Nov 06 2026 Dennis Gilmore <dennis@ausil.us> - 1.0-1.20261106
- Initial packaging
