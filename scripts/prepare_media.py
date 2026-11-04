#!/usr/bin/env python3
"""Make web copies from supplied media; original files are never changed."""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SOURCES = [
    ('correction-step-2', '咖啡第二步纠错.mp4', 1280, 10),
    ('correction-step-7', '咖啡第七步纠错.mp4', 1280, 11),
    ('coffee', '手冲咖啡全流程.mp4', 1920, 65),
]
TASK_SOURCES = [
    ('usb-storage', 'U盘收纳重剪版.mp4'),
    ('keyboard-pushback', '键盘回推重剪版.mp4'),
    ('bookshelf', '书架重剪版.mp4'),
    ('cosmetics', '化妆品(1).mp4'),
    ('charging', '11月4日手表.mp4'),
    ('medicine', '11月4日药品.mp4'),
    ('bedtime', '睡前物品准备(1).mp4'),
    ('drawer', '首饰盒眼镜重拍版.mp4'),
    ('food-waste', '厨余垃圾分离.mp4'),
    ('cucumber', '11月4日切黄瓜.mp4'),
    ('parcel-unpacking', '11月4日快递开箱.mp4'),
    ('parcel-packing', '11月4日封箱.mp4'),
]


def find_ffmpeg():
    binary = os.environ.get('FFMPEG_BIN') or shutil.which('ffmpeg')
    if binary:
        return binary
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        raise SystemExit('Set FFMPEG_BIN, install ffmpeg, or pip install imageio-ffmpeg.')


def write_json(path, value):
    temporary = path.with_suffix('.tmp.json')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temporary.replace(path)


def prepare(item, ffmpeg, force, hardware):
    slug, source, width, poster_time = item
    source = Path(source)
    name = source.name
    if not source.is_file():
        raise FileNotFoundError(source)
    video = ROOT / 'assets/videos' / f'{slug}.mp4'
    poster = ROOT / 'assets/posters' / f'{slug}.jpg'
    probe = subprocess.run([ffmpeg, '-hide_banner', '-i', str(source)], capture_output=True, text=True)
    match = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', probe.stderr)
    if not match:
        raise ValueError(f'Cannot read duration of {name}')
    hours, minutes, seconds = map(float, match.groups())
    duration = hours * 3600 + minutes * 60 + seconds
    acceleration = ['-hwaccel', 'videotoolbox'] if hardware else ['-threads', '2']
    if force or not poster.is_file():
        subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
                        '-ss', str(min(poster_time, duration * 0.5)), *acceleration, '-i', str(source),
                        '-frames:v', '1', '-vf', 'scale=1280:-2', '-q:v', '3', str(poster)], check=True)
    if force or not video.is_file():
        temporary = video.with_suffix('.tmp.mp4')
        bitrate = min(2000, int(23 * 1024**2 * 8 / duration / 1000) - 128)
        encoder = (['-c:v', 'h264_videotoolbox', '-b:v', f'{bitrate}k', '-maxrate', f'{bitrate}k', '-bufsize', f'{bitrate*2}k']
                   if hardware else ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24', '-threads', '2'])
        video_filter = f'scale={width}:-2'
        decode = acceleration
        if hardware:
            dimensions = re.search(r'Video:.*? (\d{2,5})x(\d{2,5})', probe.stderr)
            source_width, source_height = map(int, dimensions.groups())
            height = round(width * source_height / source_width / 2) * 2
            raw_format = 'p010le' if 'yuv420p10le' in probe.stderr else 'nv12'
            decode = acceleration + ['-hwaccel_output_format', 'videotoolbox_vld']
            video_filter = f'scale_vt=w={width}:h={height},hwdownload,format={raw_format},format=yuv420p'
        with (ROOT / 'assets/videos' / f'{slug}.log').open('w') as log:
            subprocess.run([ffmpeg, '-hide_banner', '-y', *decode, '-i', str(source),
                            '-map', '0:v:0', '-map', '0:a:0?', '-vf', video_filter,
                            *encoder,
                            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k',
                            '-movflags', '+faststart', str(temporary)], stderr=log, stdout=log, check=True)
        temporary.replace(video)
    result = {'id': slug, 'duration': round(duration, 2), 'source': str(source.relative_to(ROOT)),
              'sourceBytes': source.stat().st_size, 'sourceModifiedNs': source.stat().st_mtime_ns,
              'webBytes': video.stat().st_size, 'src': f'assets/videos/{slug}.mp4',
              'poster': f'assets/posters/{slug}.jpg'}
    print(json.dumps(result), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--hardware', action='store_true', help='Use macOS VideoToolbox acceleration')
    parser.add_argument('--tasks-only', action='store_true', help='Leave coffee/correction media unchanged')
    parser.add_argument('--task-dir', type=Path, default=ROOT / 'demo', help='Directory containing the supplied A²-WLA task videos (default: demo/)')
    args = parser.parse_args()
    for folder in ['assets/videos', 'assets/posters']:
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
    ffmpeg = find_ffmpeg()
    sources = [] if args.tasks_only else [(slug, ROOT / 'Tech Report' / name, width, timestamp) for slug, name, width, timestamp in SOURCES]
    if args.task_dir:
        sources.extend((slug, args.task_dir / name, 1280, 5) for slug, name in TASK_SOURCES
                       if (args.task_dir / name).is_file())
    info_path = ROOT / 'assets/media-info.json'
    existing = {item['id']: item for item in json.loads(info_path.read_text())} if info_path.is_file() else {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(prepare, item, ffmpeg, args.force, args.hardware) for item in sources]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            existing[result['id']] = result
            write_json(info_path, list(existing.values()))
            manifest_path = ROOT / 'data/videos.json'
            manifest = json.loads(manifest_path.read_text())
            for task in manifest['tasks']:
                if task['id'] == result['id']:
                    rounded = round(result['duration'])
                    task.update(src=result['src'], poster=result['poster'], duration=f'{rounded//60}:{rounded%60:02d}')
            write_json(manifest_path, manifest)


if __name__ == '__main__':
    main()
