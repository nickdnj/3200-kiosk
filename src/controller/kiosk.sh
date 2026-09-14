#!/usr/bin/env bash
# Launch the 3280 kiosk. Called by 3280-kiosk.service, not by hand.
#
# Deviation from docs/02-architecture.md A3.2: there is no loopback HTTP
# server. The app is one self-contained file with no fetch(), no modules and
# no external references (build-kiosk.py asserts this), so file:// serves it
# exactly as well with one less thing to crash at 2 a.m.
set -euo pipefail

APP="${KIOSK_APP:-/opt/3280-kiosk/index.html}"
ROTATE="${KIOSK_ROTATE:-right}"      # right | left | normal | inverted
PROFILE="${KIOSK_PROFILE:-/var/lib/3280-kiosk/chrome}"

export DISPLAY="${DISPLAY:-:0}"

# --- the panel ------------------------------------------------------------
# Portrait. Which way depends on how the monitor is physically turned; if the
# picture is upside down use "left", and if touch then lands on the wrong side
# see rotate.sh - the two are set independently and both must agree.
"$(dirname "$0")/rotate.sh" "$ROTATE"

# No blanking, no screensaver, no power management. This runs all day.
xset s off
xset s noblank
xset -dpms

# Belt and braces: the page already sets cursor:none, this covers the gaps
# between page loads and any crash screen.
command -v unclutter >/dev/null && unclutter -idle 0 -root &

# --- the browser ----------------------------------------------------------
# A stale exit flag makes Chromium open a "didn't shut down correctly" bubble
# on top of the exhibit. Clear it every start.
if [ -f "$PROFILE/Default/Preferences" ]; then
  sed -i 's/"exit_type":"[^"]*"/"exit_type":"Normal"/' "$PROFILE/Default/Preferences" || true
fi

BROWSER=$(command -v chromium || command -v chromium-browser || command -v google-chrome)

exec "$BROWSER" \
  --kiosk \
  --user-data-dir="$PROFILE" \
  --start-fullscreen \
  --noerrdialogs \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --disable-features=TranslateUI,Translate,ChromeWhatsNewUI \
  --disable-component-update \
  --disable-background-networking \
  --check-for-update-interval=31536000 \
  --no-first-run \
  --no-default-browser-check \
  --password-store=basic \
  --touch-events=enabled \
  --disable-pinch \
  --overscroll-history-navigation=0 \
  --autoplay-policy=no-user-gesture-required \
  --hide-scrollbars \
  "file://$APP"
