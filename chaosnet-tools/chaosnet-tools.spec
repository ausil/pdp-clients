%global gitdate 20261106

Name:           chaosnet-tools
Version:        1.0
Release:        1.%{gitdate}%{?dist}
Summary:        Chaosnet utilities: TCP gateway, MLDEV file transfer, SEND and RTAPE
# chaos.c, rtape.c, senver.c: Apache-2.0.  Other top-level files carry no
# licence header.  dasm/libword (linked into mlftp): GPL-2.0-or-later.
License:        Apache-2.0 AND GPL-2.0-or-later
URL:            https://github.com/Chaosnet/chaosnet-tools
# ./make-git-snapshot.sh
# Includes the dasm (pdp10-its-disassembler) submodule.
Source0:        %{name}-%{gitdate}.tar.bz2
Source1:        make-git-snapshot.sh

BuildRequires:  gcc
BuildRequires:  make

# The tools reach Chaosnet through cbridge's /tmp/chaos_stream socket.
Suggests:       chaosnet-bridge

%description
Utilities that talk Chaosnet through the Chaosnet bridge (cbridge):

  gw        gateway incoming TCP connections to a Chaosnet contact
  mlftp     transfer files to and from ITS with the MLDEV protocol
  qsend     send a message to a Chaosnet user
  senver    server for incoming SEND messages
  rtape     server for the RTAPE remote tape protocol
  shutdown  ask a Chaosnet host to shut down

shutdown and the gateway.sh helper are installed in
%{_libexecdir}/%{name} so they do not clash with the system shutdown.

%prep
%autosetup -n %{name}-%{gitdate} -p1
# Point the gateway helper at the installed gw.
sed -i 's|^GW=.*|GW=%{_bindir}/gw|' gateway.sh

%build
%make_build CFLAGS="%{optflags} -Idasm/libword" LDFLAGS="%{build_ldflags}"

%install
install -d %{buildroot}%{_bindir} %{buildroot}%{_libexecdir}/%{name}
install -m755 gw mlftp qsend senver rtape qsend-incoming %{buildroot}%{_bindir}/
install -m755 shutdown gateway.sh %{buildroot}%{_libexecdir}/%{name}/

%files
%license dasm/COPYING
%doc README.md chaosnet-gateway.service chaosnet-rtape.service
%{_bindir}/gw
%{_bindir}/mlftp
%{_bindir}/qsend
%{_bindir}/qsend-incoming
%{_bindir}/rtape
%{_bindir}/senver
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/shutdown
%{_libexecdir}/%{name}/gateway.sh

%changelog
* Fri Nov 06 2026 Dennis Gilmore <dennis@ausil.us> - 1.0-1.20261106
- Initial packaging
