#!/usr/bin/env bash
# Rotate the panel AND remap every touch device onto it. The display and the
# digitizer are separate devices: rotating the picture does NOT rotate the
# touch, so a finger lands 90 degrees away until this runs. Called by kiosk.sh.
set -euo pipefail
ROT="${1:-right}"
export DISPLAY="${DISPLAY:-:0}"

OUT=$(xrandr --query | awk '/ connected/{print $1; exit}')
[ -n "$OUT" ] || { echo "rotate: no connected output"; exit 1; }
xrandr --output "$OUT" --rotate "$ROT"

# Map each touchscreen (identified by exposing a libinput Calibration Matrix)
# onto the rotated output. map-to-output derives the transform from the output
# geometry itself, so it stays correct for whatever rotation we choose.
xinput list --id-only 2>/dev/null | while read -r ID; do
  xinput list-props "$ID" 2>/dev/null | grep -q "libinput Calibration Matrix" || continue
  if xinput --map-to-output "$ID" "$OUT" 2>/dev/null; then
    echo "rotate: mapped touch device $ID -> $OUT ($ROT)"
  fi
done
