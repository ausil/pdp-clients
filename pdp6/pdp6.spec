%global gitdate 20261106

Name:           pdp6
Version:        1.0
Release:        1.%{gitdate}%{?dist}
Summary:        Tools from the PDP-6 emulator project
License:        MIT
URL:            https://github.com/aap/pdp6
# ./make-git-snapshot.sh
Source0:        %{name}-%{gitdate}.tar.bz2
Source1:        make-git-snapshot.sh

BuildRequires:  gcc

Provides:       mkpty33 = %{version}-%{release}

%description
Tools from aap's PDP-6 emulator project.  Currently this ships only
mkpty33, which creates a pseudo-terminal that behaves like a Teletype
ASR-33 and connects it to the calling terminal, optionally symlinking
the pty to a given file name.

%prep
%autosetup -n %{name}-%{gitdate} -p1

%build
%{__cc} %{optflags} -o mkpty33 tools/mkpty33.c %{build_ldflags}

%install
install -Dm755 mkpty33 %{buildroot}%{_bindir}/mkpty33

%files
%license LICENSE
%doc README.md
%{_bindir}/mkpty33

%changelog
* Fri Nov 06 2026 Dennis Gilmore <dennis@ausil.us> - 1.0-1.20261106
- Initial packaging
