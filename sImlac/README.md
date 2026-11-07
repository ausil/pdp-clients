# sImlac

Packages the [sImlac](https://github.com/jdersch/sImlac) Imlac PDS-1/PDS-4
emulator. `make-git-snapshot.sh` produces `sImlac-YYYYMMDD.tar.bz2` from
upstream HEAD.

- Upstream targets .NET Framework; two patches (taken from the
  `ausil/sImlac` `cross-platform-dotnet` branch) port it to .NET 10 and add
  the case-invert option. Drop them as upstream absorbs the changes.
- `ExclusiveArch: x86_64 aarch64`. Built framework-dependent with
  `dotnet publish`; the system SDL2 (`sdl2-compat`) is used instead of the
  copy bundled in ppy.SDL2-CS.
- NuGet packages come from `Source2`, built by `make-nuget-cache.sh` (needs network and dotnet-sdk-10.0), so the build itself is offline.
- Installs to `%{_libdir}/sImlac` (boot files are found relative to the
  executable); `/usr/bin/sImlac` and `/usr/bin/imlac` are symlinks.
- Upstream has no LICENSE file (headers say AGPL-3.0-or-later), so there is
  no `%license`.
