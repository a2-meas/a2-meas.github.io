#!/usr/bin/env python3
"""Make web cover assets from the original video, without changing the source."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
source = ROOT / 'demo/封面-en-v6.mp4'
TITLE_START_SECONDS = 0
FADE_SECONDS = 0.6
ffmpeg = os.environ.get('FFMPEG') or shutil.which('ffmpeg')
if not ffmpeg:
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
target = ROOT / 'assets/videos/cover.mp4'
images = ROOT / 'assets/cover'
images.mkdir(parents=True, exist_ok=True)
# Count decoded frames, so the fade reaches black on the actual last frame,
# rather than a container-duration timestamp after the last visible frame.
probe = subprocess.run([ffmpeg, '-hide_banner', '-i', str(source),
                        '-map', '0:v:0', '-an', '-f', 'null', '-',
                        '-progress', 'pipe:1', '-nostats'],
                       capture_output=True, text=True, check=True)
frame_count = int(re.findall(r'^frame=(\d+)$', probe.stdout, flags=re.M)[-1])
fps = float(re.search(r'(\d+(?:\.\d+)?) fps', probe.stderr)[1])
fade_frames = max(1, round(FADE_SECONDS * fps))
fade_out_start = frame_count - 1 - fade_frames
assert fade_out_start > fade_frames, 'Cover must be longer than both fades'
# One scalar brightness ramp applies to every pixel of the complete frame.
# Never crop, mask, stagger, or fade the individual grid cells independently.
filters = (f'scale=1280:-2,fade=t=in:s=0:n={fade_frames}:color=black,'
           f'fade=t=out:s={fade_out_start}:n={fade_frames}:color=black')
subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
                '-an', '-vf', filters,
                '-c:v', 'libx264', '-preset', 'fast', '-crf', '26',
                '-threads', '4', '-maxrate', '1500k', '-bufsize', '3000k', '-g', '60',
                '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(target)], check=True)
# Match the black opening frame while retaining an unfaded, useful still for
# reduced-motion, blocked-autoplay and no-video fallbacks.
for input_path, seek, poster_filters, name in [
        (target, ['-ss', '0'], [], 'cover-start.jpg'),
        (source, ['-sseof', '-0.25'], ['-vf', 'reverse,scale=1280:-2'], 'cover-mosaic.jpg')]:
    subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', *seek,
                    '-i', str(input_path), *poster_filters, '-frames:v', '1', '-q:v', '3',
                    str(images / name)], check=True)
manifest_path = ROOT / 'data/videos.json'
manifest = json.loads(manifest_path.read_text())
manifest['cover'] = {'src': 'assets/videos/cover.mp4',
                     'poster': 'assets/cover/cover-start.jpg',
                     'finalPoster': 'assets/cover/cover-mosaic.jpg',
                     'titleStartSeconds': TITLE_START_SECONDS,
                     'loop': True, 'endHoldSeconds': 0,
                     'fadeInSeconds': fade_frames / fps,
                     'fadeOutSeconds': fade_frames / fps,
                     'fadeOutStartFrame': fade_out_start,
                     'frameCount': frame_count}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
info_path = ROOT / 'assets/media-info.json'
info = [row for row in json.loads(info_path.read_text()) if row['id'] != 'cover']
info.append({'id': 'cover', 'source': str(source.relative_to(ROOT)),
             'sourceBytes': source.stat().st_size, 'webBytes': target.stat().st_size,
             'src': 'assets/videos/cover.mp4', 'poster': 'assets/cover/cover-start.jpg'})
info_path.write_text(json.dumps(info, ensure_ascii=False, indent=2) + '\n')
print(f'Cover: {target.stat().st_size / 1024**2:.1f} MiB; source untouched.')
