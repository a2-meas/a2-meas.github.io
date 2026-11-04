#!/usr/bin/env python3
"""Make web cover assets from the original video, without changing the source."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
source = ROOT / 'demo/封面-en.mp4'
TITLE_START_SECONDS = 8.0
ffmpeg = os.environ.get('FFMPEG') or shutil.which('ffmpeg')
if not ffmpeg:
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
target = ROOT / 'assets/videos/cover.mp4'
images = ROOT / 'assets/cover'
images.mkdir(parents=True, exist_ok=True)
subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
                '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
                '-threads', '4', '-maxrate', '5000k', '-bufsize', '10000k',
                '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(target)], check=True)
for seek, name in [(['-ss', '0'], 'cover-start.jpg'),
                   (['-sseof', '-0.5'], 'cover-mosaic.jpg')]:
    subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', *seek,
                    '-i', str(source), '-frames:v', '1', '-q:v', '3',
                    str(images / name)], check=True)
manifest_path = ROOT / 'data/videos.json'
manifest = json.loads(manifest_path.read_text())
manifest['cover'] = {'src': 'assets/videos/cover.mp4',
                     'poster': 'assets/cover/cover-start.jpg',
                     'finalPoster': 'assets/cover/cover-mosaic.jpg',
                     'titleStartSeconds': TITLE_START_SECONDS,
                     'loop': True, 'endHoldSeconds': 0}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
html_path = ROOT / 'index.html'
html_path.write_text(re.sub(r'data-title-start="[\d.]+"',
                            f'data-title-start="{TITLE_START_SECONDS:g}"',
                            html_path.read_text()))
info_path = ROOT / 'assets/media-info.json'
info = [row for row in json.loads(info_path.read_text()) if row['id'] != 'cover']
info.append({'id': 'cover', 'source': str(source.relative_to(ROOT)),
             'sourceBytes': source.stat().st_size, 'webBytes': target.stat().st_size,
             'src': 'assets/videos/cover.mp4', 'poster': 'assets/cover/cover-start.jpg'})
info_path.write_text(json.dumps(info, ensure_ascii=False, indent=2) + '\n')
print(f'Cover: {target.stat().st_size / 1024**2:.1f} MiB; source untouched.')
