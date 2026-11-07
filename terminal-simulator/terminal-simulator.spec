%global gitdate 20261106

Name:           terminal-simulator
Version:        0.2
Release:        1.%{gitdate}%{?dist}
Summary:        Hardware-level simulation of the DEC VT100 terminal
# LICENSE is GPLv3; the sources carry no headers stating "or later".
License:        GPL-3.0-only
URL:            https://github.com/larsbrinkhoff/terminal-simulator
# ./make-git-snapshot.sh
Source0:        %{name}-%{gitdate}.tar.bz2
Source1:        make-git-snapshot.sh
# Stop the CPU thread hanging when sdl2-compat never drains the audio queue
Patch0:         0001-Recover-when-the-audio-backend-never-drains-its-queu.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_image)
BuildRequires:  pkgconfig(gl)

%description
A software simulation of the DEC VT100 hardware.  The original firmware
ROM is built in and executed by an 8080 emulator, together with the
video display and character generator, settings NVRAM, Intel 8251
USART and keyboard matrix scanner.  The Advanced Video Option is not
included.

The upstream VT52 simulation is not packaged; the vt52 command comes
from the vt05 package.

%prep
%autosetup -n %{name}-%{gitdate} -p1

%build
%make_build -C vt100 \
    CFLAGS='%{optflags} -DSHADERDIR=\"%{_datadir}/%{name}/\"' \
    LDFLAGS="%{build_ldflags} -lGL"

%install
install -Dm755 vt100/vt100 %{buildroot}%{_bindir}/vt100
install -Dm644 -t %{buildroot}%{_datadir}/%{name} \
    common/vertex.shader common/crt.shader

%check
# CP/M CPU exercisers; -R runs them without opening a window.
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy sh test/test.sh

%files
%license LICENSE
%doc README.md
%{_bindir}/vt100
%{_datadir}/%{name}/

%changelog
* Fri Nov 06 2026 Dennis Gilmore <dennis@ausil.us> - 0.2-1.20261106
- Initial packaging
