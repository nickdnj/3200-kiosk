#!/usr/bin/env python3
"""Re-pull the latin-subset woff2 files the kiosk embeds.

Run this only when the font stack changes. The files are cached in
assets/fonts/ and committed on purpose: the kiosk has no network, and a build
that silently reaches fonts.googleapis.com produces a page that looks right on
a developer's laptop and reflows on the exhibit floor.
"""
import pathlib, re, urllib.request

URL = ("https://fonts.googleapis.com/css2?"
       "family=Oswald:wght@400;500;600;700"
       "&family=Archivo:wght@500;600;700"
       "&family=Newsreader:ital,wght@0,400;0,500;0,600;1,400"
       "&family=Space+Mono:wght@400;700&display=swap")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")   # woff2, not ttf

D = pathlib.Path(__file__).parent / "assets" / "fonts"
D.mkdir(parents=True, exist_ok=True)

css = urllib.request.urlopen(
    urllib.request.Request(URL, headers={"User-Agent": UA}), timeout=30
).read().decode()

blocks = re.findall(r"/\* (\w[\w-]*) \*/\s*(@font-face \{.*?\})", css, re.S)
rows, total = [], 0
for subset, b in blocks:
    if subset != "latin":            # the exhibit copy is English
        continue
    fam = re.search(r"font-family: '([^']+)'", b).group(1)
    wt  = re.search(r"font-weight: (\d+)", b).group(1)
    st  = re.search(r"font-style: (\w+)", b).group(1)
    url = re.search(r"url\((https://[^)]+)\)", b).group(1)
    name = f"{fam.replace(' ', '')}-{wt}{'i' if st == 'italic' else ''}.woff2"
    data = urllib.request.urlopen(url, timeout=30).read()
    (D / name).write_bytes(data)
    total += len(data)
    rows.append(f"{fam} {st} {wt}  {name}  {len(data)} bytes")
    print(f"  {name:<26} {len(data)/1024:6.1f} KB")

(D / "MANIFEST.txt").write_text(
    "Latin-subset woff2, pulled once from Google Fonts and cached here so the\n"
    "kiosk renders identically with no network. Regenerate with fetch-fonts.py.\n\n"
    + "\n".join(rows) + "\n")
print(f"{len(rows)} faces, {total/1024:.0f} KB total")
