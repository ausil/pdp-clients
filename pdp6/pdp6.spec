%global gitdate 20261107

Name:           pdp6
Version:        1.0
Release:        1.%{gitdate}%{?dist}
Summary:        PDP-6 emulator with virtual front panel
License:        MIT
URL:            https://github.com/aap/pdp6
# ./make-git-snapshot.sh
Source0:        %{name}-%{gitdate}.tar.bz2
Source1:        make-git-snapshot.sh

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_image)

%description
aap's PDP-6 emulator, a low-level C transcription of the DEC schematics.
It implements the processor, console TTY, paper tape reader and punch,
data control, DECtape and a 340 display.  This package has the emulator
with its SDL2 virtual front panel (pdp6), the headless serial-panel
variant (pdp6_s) and the networked variant (pdp6_n).

The emulator reads init.ini from the current directory; sample startup
files are in %{_datadir}/%{name}/.

%package tools
Summary:        PDP-6 assembler, loader and paper tape / DECtape utilities
Provides:       mkpty33 = %{version}-%{release}

%description tools
Tools from the PDP-6 emulator project: as6 (assembler), ld6 (loader),
ptdump, dtdump, rel, dtr2dta and dta2dtr (DECtape image conversion),
mkpty and mkpty33 (pseudo-terminals, mkpty33 behaves like a Teletype
ASR-33), and scon33.

%package panel
Summary:        Standalone SDL2 front panel for the PDP-6 emulator

%description panel
panel6 is the standalone SDL2 virtual front panel.  It drives a PDP-6
emulator built without a panel (pdp6_s) over a serial line.

%prep
%autosetup -n %{name}-%{gitdate} -p1
# The panel loads its images from ../art relative to the build tree.
sed -i 's|"\.\./art/|"%{_datadir}/%{name}/art/|' panel/panel6.c

%build
# The sources typedef bool, which clashes with the keyword in C23.
CFLAGS="%{optflags} -Wall -Wno-parentheses -std=gnu17"

%make_build -C emu pdp6 pdp6_s pdp6_n \
    CFLAGS="$CFLAGS" LIBS="-lpthread -lm %{build_ldflags}"

%make_build -C panel panel6 \
    CFLAGS="$CFLAGS $(sdl2-config --cflags) $(pkg-config SDL2_image --cflags)" \
    LIBS="$(sdl2-config --libs) $(pkg-config SDL2_image --libs) -lpthread %{build_ldflags}"

cd tools
for t in as6 ld6 ptdump dtdump; do
    %{__cc} $CFLAGS -o $t $t.c pdp6common.c %{build_ldflags}
done
for t in dtr2dta mkpty mkpty33 scon33 rel; do
    %{__cc} $CFLAGS -o $t $t.c %{build_ldflags}
done
# dtr2dta.c picks its direction from argv[0]
cp -p dtr2dta dta2dtr

%install
install -Dm755 -t %{buildroot}%{_bindir} emu/pdp6 emu/pdp6_s emu/pdp6_n
install -Dm755 -t %{buildroot}%{_bindir} panel/panel6
install -Dm755 -t %{buildroot}%{_bindir} \
    tools/as6 tools/ld6 tools/ptdump tools/dtdump tools/rel \
    tools/dtr2dta tools/dta2dtr tools/mkpty tools/mkpty33 tools/scon33
install -Dm644 -t %{buildroot}%{_datadir}/%{name} \
    emu/init.ini emu/mem_0_rim emu/mem_0_sysgen_macdmp
install -Dm644 -t %{buildroot}%{_datadir}/%{name}/art art/*.png

%files
%license LICENSE
%doc README.md
%{_bindir}/pdp6
%{_bindir}/pdp6_s
%{_bindir}/pdp6_n
%{_datadir}/%{name}/
%exclude %{_datadir}/%{name}/art/

%files tools
%license LICENSE
%{_bindir}/as6
%{_bindir}/ld6
%{_bindir}/ptdump
%{_bindir}/dtdump
%{_bindir}/rel
%{_bindir}/dtr2dta
%{_bindir}/dta2dtr
%{_bindir}/mkpty
%{_bindir}/mkpty33
%{_bindir}/scon33

%files panel
%license LICENSE
%{_bindir}/panel6
%{_datadir}/%{name}/art/

%changelog
* Sat Nov 07 2026 Dennis Gilmore <dennis@ausil.us> - 1.0-1.20261107
- Build the emulators, tools and standalone panel; split into pdp6,
  pdp6-tools and pdp6-panel

* Fri Nov 06 2026 Dennis Gilmore <dennis@ausil.us> - 1.0-1.20261106
- Initial packaging
