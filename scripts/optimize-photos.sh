#!/bin/bash
# Convert iPhone/HDR photos to sRGB JPEGs for consistent browser color
# and smaller downloads. Leave schematics and diagrams as PNG.
#
# Usage:
#   scripts/optimize-photos.sh images/photo.png
#   scripts/optimize-photos.sh images/photo1.png images/photo2.heic
#
# Writes <name>.jpg next to each input (replacing an existing .jpg),
# max 2000px on the long edge, JPEG quality 82. GPS/location EXIF is
# stripped; time and camera tags are kept.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STRIP_GPS="$ROOT/scripts/strip-gps.py"
SRGB="/System/Library/ColorSync/Profiles/sRGB Profile.icc"
QUALITY=82
MAX_EDGE=2000

if [[ ! -f "$SRGB" ]]; then
  echo "Error: sRGB profile not found at $SRGB" >&2
  exit 1
fi

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 <photo> [photo...]" >&2
  exit 1
fi

for src in "$@"; do
  if [[ ! -f "$src" ]]; then
    echo "Error: file not found: $src" >&2
    exit 1
  fi

  dest="${src%.*}.jpg"
  echo "Converting $src -> $dest"
  sips --matchTo "$SRGB" \
    -s format jpeg \
    -s formatOptions "$QUALITY" \
    -Z "$MAX_EDGE" \
    "$src" \
    --out "$dest" >/dev/null
  python3 "$STRIP_GPS" "$dest" >/dev/null
done
