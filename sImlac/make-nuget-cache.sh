#!/bin/sh

# Usage: ./make-nuget-cache.sh [SNAPSHOT.tar.bz2]
#
# Makes sImlac-nuget-YYYYMMDD.tar.xz, a NuGet package cache holding everything
# "dotnet publish" needs to restore sImlac offline for linux-x64 and
# linux-arm64.  Defaults to the newest sImlac-*.tar.bz2 here, after any
# downstream patches have been applied, so the packages match the build.
# Needs network access and dotnet-sdk-10.0.

set -e

SNAP=${1:-$(ls -t sImlac-[0-9]*.tar.bz2 | head -n 1)}
[ -f "$SNAP" ] || { echo "no snapshot tarball; run ./make-git-snapshot.sh" >&2; exit 1; }

DATE=${SNAP#sImlac-}
DATE=${DATE%.tar.bz2}
SNAPDIR=sImlac-$DATE
OUT=sImlac-nuget-$DATE
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

tar -C "$WORK" -xjf "$SNAP"
for p in [0-9][0-9][0-9][0-9]-*.patch; do
    [ -f "$p" ] || continue
    patch -d "$WORK/$SNAPDIR" -p1 < "$p"
done

export DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1
for rid in linux-x64 linux-arm64; do
    # Keep these properties identical to the dotnet publish in sImlac.spec,
    # or the build will want packages that were never restored here.
    # RuntimeIdentifiers is overridden so win-x64 packs aren't pulled in.
    dotnet restore "$WORK/$SNAPDIR/imlac/imlac.csproj" -r "$rid" \
        -p:SelfContained=false -p:RuntimeIdentifiers="$rid" \
        --packages "$WORK/$OUT"
done

# Only the packages are wanted, not the per-user HTTP cache bits.
tar -C "$WORK" -cf - "$OUT" | xz > "$OUT.tar.xz"
echo "wrote $OUT.tar.xz"
