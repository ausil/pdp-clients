# PDP client packaging

RPM packaging for the client side of a PDP-10/PDP-6/PDP-11 retro-computing
setup: emulators, terminals, network tools and a few utilities. Each package
is a git snapshot of an upstream project, built for Fedora and published to
the COPR project [`ausil/pdp`](https://copr.fedorainfracloud.org/coprs/ausil/pdp/).

## Packages

| Directory | Upstream | Provides |
|---|---|---|
| `chaosnet-bridge` | [bictorv/chaosnet-bridge](https://github.com/bictorv/chaosnet-bridge/) | Chaosnet bridge between implementations |
| `chaosnet-tools` | [Chaosnet/chaosnet-tools](https://github.com/Chaosnet/chaosnet-tools) | TCP gateway, MLDEV file transfer, SEND, RTAPE |
| `rpdp` | [obsolescence/rpdp](https://github.com/obsolescence/rpdp) (scripts only) | `rpdp` launcher for terminals connected to a remote PiDP-10, -11, -8 or -1; config in `/etc/rpdp.conf` |
| `p7sim` | [aap/p7sim](https://github.com/aap/p7sim) | `p7sim` / `p7simES` P7 phosphor display simulator (PDP-1 Type 30) |
| `pdp6` | [aap/pdp6](https://github.com/aap/pdp6) | `pdp6-emu` (emulator), `pdp6-tools` (as6, ld6, DECtape/paper tape utilities, mkpty33), `pdp6-panel` (standalone front panel) |
| `sImlac` | [jdersch/sImlac](https://github.com/jdersch/sImlac) | Imlac PDS-1/PDS-4 emulator (.NET) |
| `supdup` | [PDP-10/supdup](https://github.com/PDP-10/supdup) | SUPDUP client |
| `terminal-simulator` | [larsbrinkhoff/terminal-simulator](https://github.com/larsbrinkhoff/terminal-simulator) | VT100 simulation |
| `tv11` | [aap/tv11](https://github.com/aap/tv11) | Knight TV emulator, plus `tvcon` client subpackage |

Package-specific notes live in a README in the package directory where there
is anything non-obvious (currently `sImlac/`).

## Layout of a package directory

    PACKAGE/
      PACKAGE.spec            spec file
      make-git-snapshot.sh    makes PACKAGE-YYYYMMDD.tar.bz2 from upstream HEAD
      NNNN-*.patch            downstream patches, if any (Patch0, Patch1, ...)

Versioning is date based. Each spec has `%global gitdate YYYYMMDD` and
`Release: N.%{gitdate}%{?dist}`, and the source tarball is named
`%{name}-%{gitdate}.tar.bz2`. The tarball is built from upstream HEAD, so it
is not committed (`.gitignore` excludes `*.tar.bz2`, `*.tar.xz`, `*.src.rpm`).

## Updating a package

`update-snapshot.sh` does the whole routine for one or more packages:

    ./update-snapshot.sh PACKAGE...
    ./update-snapshot.sh -m "Fix the thing" tv11
    ./update-snapshot.sh -c pdp6 supdup          # also submit to COPR

For each package it:

1. runs `make-git-snapshot.sh` to make `PACKAGE-YYYYMMDD.tar.bz2` (and
   `make-nuget-cache.sh` if the package has one),
2. sets `%global gitdate` to today,
3. bumps the leading number of `Release:`,
4. adds a `%changelog` entry (`-m` sets the message),
5. runs `fedpkg --release f45 srpm`, leaving the SRPM in the package
   directory.

Options: `-r RELEASE` (default `f45`), `-p PROJECT` (default `ausil/pdp`),
`-c` to submit with `copr-cli build`. Set `REF` to a local clone of the
upstream repo to speed up the snapshot clone.

It needs `fedpkg`, `rpmdev-packager` (falls back to git config), and
`copr-cli` for `-c`. Commit the changed spec when you're happy with it.

## Building

Test in mock before sending anything to COPR:

    mock -r fedora-45-aarch64 --rebuild PACKAGE/PACKAGE-*.src.rpm
    mock -r fedora-45-x86_64  --rebuild PACKAGE/PACKAGE-*.src.rpm

Then submit the SRPM:

    copr-cli build ausil/pdp PACKAGE/PACKAGE-*.src.rpm

Builds run with the network off, so every source must be in the SRPM.

## Downstream patches

Patches live next to the spec and are applied by `%autosetup -p1`. They are
generated from commits in a checkout of the upstream project, for example:

    git -C ~/code/pdp/sImlac format-patch -N -o ~/code/pdp/clients/sImlac

Name them `NNNN-*.patch` in order and list each as a `PatchN:` line in the
spec with a comment saying what it is for. Drop a patch when upstream
absorbs the change. Current patches:

- `sImlac`: port to .NET 10 for Linux, the case-invert option, and a fix for
  a telnet read-lock crash.
- `chaosnet-bridge`: let `CFLAGS` be overridden.
- `terminal-simulator`: recover when the audio backend never drains its queue.

## Notes on specific packages

- **sImlac** is .NET, limited to `x86_64` and `aarch64`. COPR has no network
  during the build, so NuGet packages come from a second source,
  `sImlac-nuget-YYYYMMDD.tar.xz`, built by `sImlac/make-nuget-cache.sh`
  (needs network and `dotnet-sdk-10.0`). `update-snapshot.sh` runs it for you.
  See `sImlac/README.md`.
- **pdp6** builds with `-std=gnu17` because upstream typedefs `bool`, which
  clashes with the C23 keyword. `fe6/` (real-hardware front end, ARM
  cross-build) and `newemu/` are not packaged.
- **rpdp** is a noarch package of sources kept in the repo (launcher script,
  `rpdp.conf`, `ssv22.iml` from obsolescence/rpdp), not a git snapshot, so
  `update-snapshot.sh` does not apply. It ships no binaries: it requires
  `tvcon`, `vt05` (vt05, vt52, dp3300), `terminal-simulator` (vt100), `p7sim` (Type 30), `tek4010` and `sImlac`, and recommends
  `pidp10` for `sty` and the Teletype sounds. Bump `Release:` by hand.
