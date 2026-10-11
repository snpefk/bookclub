#!/bin/sh
# Regenerate the three standalone diploma images from diploma.jpg.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
font=${DIPLOMA_FONT:-/System/Library/Fonts/MarkerFelt.ttc}

for name in snpefk barsoosayque alradish; do
    magick "$here/diploma.jpg" \
        -font "$font" -gravity north -interline-spacing 0 \
        -stroke '#ffe3bf' -strokewidth 9 -fill '#ffe3bf' \
        -pointsize 49 -annotate +0+475 'CERTIFICATE FOR FINISHING' \
        -pointsize 56 -annotate +0+580 '"Rust atomics and locks"' \
        -pointsize 52 -annotate +0+665 'presented to' \
        -pointsize 68 -annotate +0+760 "@$name" \
        -stroke '#2f2021' -strokewidth 3 -fill '#f27045' \
        -pointsize 49 -annotate +0+475 'CERTIFICATE FOR FINISHING' \
        -pointsize 56 -annotate +0+580 '"Rust atomics and locks"' \
        -pointsize 52 -annotate +0+665 'presented to' \
        -pointsize 68 -annotate +0+760 "@$name" \
        -quality 93 "$here/$name.jpg"
done
