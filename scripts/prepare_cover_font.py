#!/usr/bin/env python3
"""Embed a small, licensed Google Sans 700 subset before the first title paint.

Requires fonttools and brotli only when regenerating the font. Runtime pages
use the embedded WOFF2 and never wait for a separate title-font download.
"""
import base64
from pathlib import Path
import re

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'assets/fonts/google-sans-bold.ttf'
TARGET = ROOT / 'assets/fonts/google-sans-cover-latin.woff2'
CSS = ROOT / 'site.css'


def main():
    font = TTFont(SOURCE, recalcTimestamp=False)
    options = subset.Options()
    options.glyph_names = True
    options.layout_features = ['*']
    options.name_IDs = ['*']
    options.name_languages = ['*']
    options.name_legacy = True
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=[*range(32, 127), 0xA0, 0xB2, 0x2013, 0x2014, 0x2018, 0x2019])
    subsetter.subset(font)
    font.flavor = 'woff2'
    font.save(TARGET)
    data = base64.b64encode(TARGET.read_bytes()).decode('ascii')
    face = ('/* cover-font-start */\n'
            '/* Google Sans 700, OFL-1.1: embedded to prevent fallback-font swapping. */\n'
            '@font-face { font-family: "Google Sans Cover"; '
            f'src: url("data:font/woff2;base64,{data}") format("woff2"); '
            'font-style: normal; font-weight: 700; font-display: block; }\n'
            '/* cover-font-end */')
    text = CSS.read_text()
    pattern = r'/\* cover-font-start \*/.*?/\* cover-font-end \*/'
    if not re.search(pattern, text, flags=re.S):
        pattern = r'@font-face\s*\{\s*font-family:\s*"Google Sans Cover";[^}]*\}'
    text, count = re.subn(pattern, lambda _: face, text, count=1, flags=re.S)
    assert count == 1, 'Expected exactly one cover font declaration'
    CSS.write_text(text)
    print(f'Embedded cover font: {SOURCE.stat().st_size:,} → {TARGET.stat().st_size:,} bytes; no separate font request.')


if __name__ == '__main__':
    main()
