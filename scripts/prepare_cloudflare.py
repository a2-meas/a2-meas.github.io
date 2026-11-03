#!/usr/bin/env python3
"""Prepare Pages-sized video copies, preserving the primary site and source media."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'output/cloudflare-private/site'
LIMIT = 25 * 1024**2


def main():
    try:
        import imageio_ffmpeg
    except ImportError:
        raise SystemExit('Install imageio-ffmpeg or run with its directory in PYTHONPATH.')
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([sys.executable, str(ROOT / 'scripts/package_site.py')], check=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / 'dist', OUT)
    changes = []
    for target in sorted(OUT.rglob('*.mp4')):
        if target.stat().st_size < LIMIT:
            continue
        relative = target.relative_to(OUT)
        source = ROOT / relative
        info = subprocess.run([ffmpeg, '-hide_banner', '-i', str(source)], capture_output=True, text=True).stderr
        match = re.search(r'Duration: (\d+):(\d+):([\d.]+)', info)
        if not match:
            raise SystemExit(f'Cannot read duration: {relative}')
        duration = int(match[1])*3600 + int(match[2])*60 + float(match[3])
        # Target ~22MiB including audio, leaving margin for container overhead.
        bitrate = min(1500, int(22 * 1024**2 * 8 / duration / 1000) - 128)
        command = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
                   '-map', '0:v:0', '-map', '0:a?', '-vf', 'scale=1280:-2',
                   '-c:v', 'libx264', '-preset', 'veryfast', '-threads', '4',
                   '-b:v', f'{bitrate}k', '-maxrate', f'{bitrate}k',
                   '-bufsize', f'{bitrate*2}k', '-pix_fmt', 'yuv420p',
                   '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', str(target)]
        subprocess.run(command, check=True)
        if target.stat().st_size >= LIMIT:
            raise SystemExit(f'Encoded file exceeds Pages limit: {relative}')
        result = {'path': str(relative), 'original_bytes': source.stat().st_size,
                  'preview_bytes': target.stat().st_size, 'duration_seconds': duration,
                  'video_bitrate_kbps': bitrate, 'source_unchanged': True}
        changes.append(result)
        print(json.dumps(result), flush=True)
    records = []
    for file in sorted(OUT.rglob('*')):
        if file.is_file() and file.name != 'package-manifest.json':
            if file.stat().st_size >= LIMIT:
                raise SystemExit(f'Asset exceeds Pages limit: {file.relative_to(OUT)}')
            records.append({'path': file.relative_to(OUT).as_posix(), 'bytes': file.stat().st_size,
                            'sha256': hashlib.sha256(file.read_bytes()).hexdigest()})
    manifest = {'mode': 'cloudflare-private-preview', 'files': records,
                'total_bytes': sum(r['bytes'] for r in records), 'media_copies': changes,
                'published': False}
    (OUT / 'package-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Prepared {len(records)} assets: {OUT}', flush=True)


if __name__ == '__main__':
    main()
