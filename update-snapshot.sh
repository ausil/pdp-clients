#!/bin/sh

# Usage: ./update-snapshot.sh [-r RELEASE] [-m MESSAGE] [-c] [-p PROJECT] PACKAGE...
#
# For each PACKAGE directory:
#   1. run ./make-git-snapshot.sh to make PACKAGE-YYYYMMDD.tar.bz2 from HEAD
#      (and ./make-nuget-cache.sh, if present, for the NuGet cache source)
#   2. set %global gitdate in PACKAGE.spec to today
#   3. bump the leading number of Release: N.%{gitdate}%{?dist}
#   4. add a %changelog entry (default "Update to git snapshot YYYYMMDD")
#   5. run "fedpkg --release RELEASE srpm", which leaves the SRPM in the
#      package directory next to the spec and tarball
# With -c, submit each SRPM with "copr-cli build PROJECT".

set -e

RELEASE=f45
PROJECT=ausil/pdp
MESSAGE=
COPR=

usage() {
    sed -n 's/^# \{0,1\}//; 3,13p' "$0" >&2
    echo "Defaults: -r $RELEASE -p $PROJECT" >&2
    exit 1
}

while getopts r:m:p:ch opt; do
    case $opt in
        r) RELEASE=$OPTARG ;;
        m) MESSAGE=$OPTARG ;;
        p) PROJECT=$OPTARG ;;
        c) COPR=1 ;;
        *) usage ;;
    esac
done
shift $((OPTIND - 1))
[ $# -gt 0 ] || usage

TOP=$(cd "$(dirname "$0")" && pwd)
TODAY=$(date +%Y%m%d)
CLDATE=$(LC_ALL=C date '+%a %b %d %Y')
PACKAGER=$(rpmdev-packager 2>/dev/null || \
           echo "$(git config user.name) <$(git config user.email)>")

for pkg in "$@"; do
    pkg=${pkg%/}
    dir=$TOP/$pkg
    spec=$dir/$pkg.spec
    if [ ! -f "$spec" ] || [ ! -x "$dir/make-git-snapshot.sh" ]; then
        echo "$pkg: needs $pkg.spec and make-git-snapshot.sh" >&2
        exit 1
    fi
    if ! grep -q '^%global[[:space:]]\{1,\}gitdate[[:space:]]' "$spec" ||
       ! grep -q '^Release:[[:space:]]*[0-9]\{1,\}\.%{gitdate}' "$spec"; then
        echo "$pkg: spec needs %global gitdate and Release: N.%{gitdate}%{?dist}" >&2
        exit 1
    fi

    (cd "$dir" && ./make-git-snapshot.sh)
    if [ -x "$dir/make-nuget-cache.sh" ]; then
        (cd "$dir" && ./make-nuget-cache.sh "$pkg-$TODAY.tar.bz2")
    fi

    n=$(sed -n 's/^Release:[[:space:]]*\([0-9]\{1,\}\)\..*/\1/p' "$spec")
    sed -i -e "s/^\(%global[[:space:]]\{1,\}gitdate[[:space:]]\{1,\}\).*/\1$TODAY/" \
           -e "s/^\(Release:[[:space:]]*\)[0-9]\{1,\}\./\1$((n + 1))./" "$spec"

    evr=$(rpmspec -q --srpm --undefine dist --qf '%{version}-%{release}' "$spec")
    msg=${MESSAGE:-Update to git snapshot $TODAY}
    sed -i "/^%changelog/a\\
* $CLDATE $PACKAGER - $evr\\
- $msg\\
" "$spec"

    out=$(cd "$dir" && fedpkg --release "$RELEASE" srpm)
    echo "$out"
    srpm=$(echo "$out" | sed -n 's/^Wrote: //p' | tail -n 1)
    if [ -z "$srpm" ] || [ ! -f "$srpm" ]; then
        echo "$pkg: fedpkg did not report an SRPM" >&2
        exit 1
    fi

    if [ -n "$COPR" ]; then
        copr-cli build "$PROJECT" "$srpm"
    else
        echo "$pkg: $srpm"
    fi
done
