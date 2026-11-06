#!/usr/bin/env python3
"""Prepare efficient full videos and low-bandwidth full-duration gallery previews."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
FFMPEG = os.environ['FFMPEG']
manifest_path = ROOT / 'data/videos.json'
manifest = json.loads(manifest_path.read_text())
backup = ROOT / 'output/playback-original-web-assets'
backup.mkdir(parents=True, exist_ok=True)
(ROOT / 'assets/previews').mkdir(exist_ok=True)
# Cover encoding belongs to prepare_cover_media.py, which reads the current
# source. Reusing the old playback backup here would restore an obsolete cover.
items = [*manifest['tasks'], *manifest['corrections'], manifest['coffee']]

def run(item):
    target = ROOT / item['src']
    original = backup / target.name
    if not original.exists():
        shutil.copy2(target, original)
    temporary = target.with_suffix('.optimized.mp4')
    maximum = '1100k'
    command = [FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(original),
               '-map', '0:v:0', '-map', '0:a?', '-vf', 'scale=1280:-2,fps=24',
               '-c:v', 'libx264', '-preset', 'fast', '-crf', '26', '-threads', '2',
               '-maxrate', maximum, '-bufsize', '3000k', '-g', '48',
               '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '64k',
               '-movflags', '+faststart', str(temporary)]
    subprocess.run(command, check=True)
    if temporary.stat().st_size < original.stat().st_size:
        temporary.replace(target)
    else:
        temporary.unlink()
        shutil.copy2(original, target)
    if item in manifest['tasks']:
        preview = ROOT / 'assets/previews' / target.name
        subprocess.run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(original),
                        '-an', '-vf', 'scale=480:-2,fps=20', '-c:v', 'libx264',
                        '-preset', 'fast', '-crf', '30', '-threads', '2',
                        '-maxrate', '180k', '-bufsize', '360k', '-g', '40',
                        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(preview)], check=True)
        item['previewSrc'] = preview.relative_to(ROOT).as_posix()
    print(f"{item['id']}: {original.stat().st_size / 1048576:.1f} → {target.stat().st_size / 1048576:.1f} MiB", flush=True)
    return target

with ThreadPoolExecutor(max_workers=2) as executor:
    list(executor.map(run, items))
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
info_path = ROOT / 'assets/media-info.json'
info = json.loads(info_path.read_text())
for item in info:
    if 'src' in item and (ROOT / item['src']).exists():
        item['webBytes'] = (ROOT / item['src']).stat().st_size
info_path.write_text(json.dumps(info, ensure_ascii=False, indent=2) + '\n')
print('Optimized playback assets and full-duration previews ready.')
