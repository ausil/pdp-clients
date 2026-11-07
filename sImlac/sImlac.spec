%global gitdate 20261107

# Managed assemblies; there is nothing for debugedit/strip to work on.
%global debug_package %{nil}
%global __strip /bin/true

%ifarch x86_64
%global dotnet_rid linux-x64
%endif
%ifarch aarch64
%global dotnet_rid linux-arm64
%endif

Name:           sImlac
Version:        0
Release:        2.%{gitdate}%{?dist}
Summary:        Imlac PDS-1 / PDS-4 emulator
# Source headers say AGPL-3.0-or-later; upstream ships no LICENSE file.
License:        AGPL-3.0-or-later
URL:            https://github.com/jdersch/sImlac
# ./make-git-snapshot.sh
Source0:        %{name}-%{gitdate}.tar.bz2
Source1:        make-git-snapshot.sh
# Offline NuGet package cache (ppy.SDL2-CS, System.IO.Ports, ...)
# ./make-nuget-cache.sh
Source2:        %{name}-nuget-%{gitdate}.tar.xz
Source3:        make-nuget-cache.sh
# Port to SDK-style .NET 10 project for Linux x86_64/aarch64
Patch0:         0001-Port-to-modern-.NET-for-Linux-x86_64-aarch64-and-Win.patch
# Option to flip the case of typed text
Patch1:         0002-add-option-to-flip-the-case-of-text-typing.patch
# Fix recursive read lock crash in the telnet async read callback
Patch2:         0003-Fix-recursive-read-lock-crash-in-telnet-async-read-c.patch

ExclusiveArch:  x86_64 aarch64

BuildRequires:  dotnet-sdk-10.0
Requires:       dotnet-runtime-10.0
Requires:       sdl2-compat

%description
sImlac emulates the Imlac PDS-1 and PDS-4 graphics minicomputers,
including the display processor, keyboard, paper tape and TTY/telnet
I/O channels, plus a debugger console.

%prep
%autosetup -n %{name}-%{gitdate} -p1
%setup -q -T -D -a 2 -n %{name}-%{gitdate}

%build
# Restore from the bundled NuGet cache (Source2); no network access needed.
export NUGET_PACKAGES=$PWD/%{name}-nuget-%{gitdate}
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1
export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
dotnet publish imlac/imlac.csproj -c Release -r %{dotnet_rid} \
    --self-contained false -p:RuntimeIdentifiers=%{dotnet_rid} \
    --source "$NUGET_PACKAGES" -o publish

%install
install -d %{buildroot}%{_libdir}/%{name}
cp -a publish/. %{buildroot}%{_libdir}/%{name}/
# Use the system SDL2 rather than the copy bundled in ppy.SDL2-CS.
find %{buildroot}%{_libdir}/%{name} -name 'libSDL2*' -delete
chmod 755 %{buildroot}%{_libdir}/%{name}/%{name}
install -d %{buildroot}%{_bindir}
ln -s %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}
ln -s %{name} %{buildroot}%{_bindir}/imlac

%files
%doc README.md
%{_libdir}/%{name}/
%{_bindir}/%{name}
%{_bindir}/imlac

%changelog
* Sat Nov 07 2026 Dennis Gilmore <dennis@ausil.us> - 0-2.20261107
- Add patch to deal with crash when running top inside of ssv

* Sat Nov 07 2026 Dennis Gilmore <dennis@ausil.us> - 0-1.20261107
- Initial packaging
