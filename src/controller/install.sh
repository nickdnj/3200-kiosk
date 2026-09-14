#!/usr/bin/env bash
# Install the 3280 kiosk onto a fresh Debian/Ubuntu machine.
#
#   sudo ./install.sh
#
# Targets X11 deliberately. Rotation plus touch remapping is one xrandr call
# and one xinput matrix on X; on Wayland it is compositor-specific and varies
# between releases. An exhibit that must come up unattended after a power cut
# is the wrong place to be clever.
set -euo pipefail
[ "$EUID" -eq 0 ] || { echo "run with sudo"; exit 1; }

HERE="$(cd "$(dirname "$0")" && pwd)"
APP_SRC="$HERE/../kiosk-app"
DEST=/opt/3280-kiosk
USER_NAME=kiosk

echo "== packages"
apt-get update
apt-get install -y --no-install-recommends \
  xserver-xorg xinit x11-xserver-utils xinput unclutter openbox \
  python3 fonts-dejavu-core
# Debian calls it chromium, Ubuntu ships a snap under chromium-browser. Take
# whichever the machine has; a snap Chromium cannot read /opt, so on Ubuntu
# prefer the .deb from the chromium-team PPA if the kiosk comes up blank.
apt-get install -y --no-install-recommends chromium \
  || apt-get install -y --no-install-recommends chromium-browser

echo "== build the app"
( cd "$APP_SRC" && python3 build-kiosk.py )

echo "== user"
id -u "$USER_NAME" >/dev/null 2>&1 || useradd -m -s /bin/bash "$USER_NAME"
usermod -aG video,input "$USER_NAME"

echo "== files"
install -d "$DEST" /var/lib/3280-kiosk
touch /var/log/3280-kiosk.log
install -m 0644 "$APP_SRC/dist/kiosk/index.html" "$DEST/index.html"
install -m 0755 "$HERE/kiosk.sh" "$HERE/rotate.sh" "$DEST/"
chown -R "$USER_NAME": /var/lib/3280-kiosk /var/log/3280-kiosk.log

echo "== X on boot, no desktop"
# One start path, not two. A systemd unit AND an .xinitrc would race each
# other for the display; this is the whole supervision chain instead:
#   agetty autologin -> .bash_profile -> startx -> .xinitrc -> loop -> kiosk.sh
# Chromium dies      -> the loop restarts it in 3 s.
# X dies             -> startx exits, agetty respawns the login, X comes back.
# The machine dies   -> the BIOS power-on setting brings all of it back.
cat > /home/$USER_NAME/.xinitrc <<'XEOF'
#!/bin/sh
openbox-session &
while true; do
  /opt/3280-kiosk/kiosk.sh >> /var/log/3280-kiosk.log 2>&1
  echo "$(date -Is) kiosk exited, restarting" >> /var/log/3280-kiosk.log
  sleep 3
done
XEOF
chown "$USER_NAME": /home/$USER_NAME/.xinitrc
chmod +x /home/$USER_NAME/.xinitrc

echo "== autologin on tty1"
install -d /etc/systemd/system/getty@tty1.service.d
cat > /etc/systemd/system/getty@tty1.service.d/autologin.conf <<AEOF
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin $USER_NAME --noclear %I \$TERM
AEOF

grep -q startx /home/$USER_NAME/.bash_profile 2>/dev/null || cat >> /home/$USER_NAME/.bash_profile <<'BEOF'
# start the exhibit on the console login, and only on the console
if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then exec startx; fi
BEOF
chown "$USER_NAME": /home/$USER_NAME/.bash_profile

systemctl daemon-reload
systemctl set-default multi-user.target 2>/dev/null || true

cat <<'DONE'

Installed.

Two things this script CANNOT do for you, both required:

  1. BIOS: set "Restore on AC Power Loss" (or "After Power Failure") to
     POWER ON. Without it the exhibit stays dark after every outage and
     someone has to walk over and press a button. This is Gate 1.

  2. The monitor's own power button behaves the same way on some panels -
     check that it returns on its own after the plug is pulled.

Reboot to test the whole chain cold:   sudo reboot
DONE
