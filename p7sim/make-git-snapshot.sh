#!/bin/sh

# Usage: ./make-git-snapshot.sh [COMMIT]
#
# to make a snapshot of the given tag/branch/commit.  Defaults to HEAD.
# Point env var REF to a local p7sim repo to reduce clone time.

set -e

NAME=p7sim
URL=https://github.com/aap/p7sim.git
DIRNAME=$NAME-$( date +%Y%m%d )

echo REF ${REF:+--reference $REF}
echo DIRNAME $DIRNAME
echo HEAD ${1:-HEAD}

rm -rf "$DIRNAME"

git clone ${REF:+--reference "$REF"} "$URL" "$DIRNAME"

GIT_DIR=$DIRNAME/.git git archive --format=tar --prefix="$DIRNAME"/ "${1:-HEAD}" \
    | bzip2 > "$DIRNAME".tar.bz2

rm -rf "$DIRNAME"
