#!/bin/sh

# Usage: ./make-git-snapshot.sh [COMMIT]
#
# to make a snapshot of the given tag/branch/commit.  Defaults to HEAD.
# Point env var REF to a local chaosnet-tools repo to reduce clone time.
#
# chaosnet-tools uses git submodules, which git archive leaves out, so each
# submodule is archived at the commit the superproject pins and appended.

set -e

NAME=chaosnet-tools
URL=https://github.com/Chaosnet/chaosnet-tools.git
DIRNAME=$NAME-$( date +%Y%m%d )

echo REF ${REF:+--reference $REF}
echo DIRNAME $DIRNAME
echo HEAD ${1:-HEAD}

rm -rf "$DIRNAME" "$DIRNAME".tar "$DIRNAME".sub.tar

git clone ${REF:+--reference "$REF"} "$URL" "$DIRNAME"
git -C "$DIRNAME" checkout -q "${1:-HEAD}"
git -C "$DIRNAME" submodule update --init --recursive

git -C "$DIRNAME" archive --format=tar --prefix="$DIRNAME"/ HEAD > "$DIRNAME".tar

for path in $( git -C "$DIRNAME" submodule foreach --recursive --quiet 'echo $displaypath' ); do
    git -C "$DIRNAME/$path" archive --format=tar --prefix="$DIRNAME/$path"/ HEAD \
        > "$DIRNAME".sub.tar
    tar -Af "$DIRNAME".tar "$DIRNAME".sub.tar
done

bzip2 -f "$DIRNAME".tar

rm -rf "$DIRNAME" "$DIRNAME".sub.tar
