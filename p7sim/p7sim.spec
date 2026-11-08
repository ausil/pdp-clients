%global gitdate 20261107

Name:           p7sim
Version:        0.1
Release:        1.%{gitdate}%{?dist}
Summary:        P7 phosphor CRT display simulator for the PDP-1 Type 30 and friends
License:        MIT
URL:            https://github.com/aap/p7sim
# ./make-git-snapshot.sh
Source0:        %{name}-%{gitdate}.tar.bz2
Source1:        make-git-snapshot.sh

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(sdl2)

%description
p7sim simulates a P7 phosphor CRT for old computer displays such as the
PDP-1 Type 30 and the PDP-6 340.  It connects to an emulator over TCP
(port 3400 by default; the PiDP-1 uses 3401 for a second display) and draws
the points it is sent with a decaying phosphor glow.

Usage: p7sim [-d] [-p port] [server]

Two builds are installed: p7sim uses desktop OpenGL and p7simES uses
OpenGL ES, which is what the Raspberry Pi wants.

%prep
%autosetup -n %{name}-%{gitdate} -p1

%build
# The sources typedef bool, which clashes with the C23 keyword.
CFLAGS="%{optflags} -std=gnu17 $(sdl2-config --cflags)"
LIBS="%{build_ldflags} -lm -ldl -lpthread $(sdl2-config --libs)"
%{__cc} $CFLAGS -c glad/glad.c -o glad/glad.o
%{__cc} $CFLAGS -o p7sim main.c glad/glad.o $LIBS
%{__cc} $CFLAGS -DGLES -o p7simES main.c glad/glad.o $LIBS

%install
install -Dm755 -t %{buildroot}%{_bindir} p7sim p7simES

%files
%license LICENSE
%doc README.md
%{_bindir}/p7sim
%{_bindir}/p7simES

%changelog
* Sat Nov 07 2026 Dennis Gilmore <dennis@ausil.us> - 0.1-1.20261107
- Initial packaging
