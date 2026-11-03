#!/usr/bin/env python3
"""Package the static site or a runnable source handoff; never publish anything."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent.parent
REPORT = 'To_the_Era_of_Agentic_Embodied_Intelligence.pdf'
WEB_FILES = ['index.html', 'site.css', 'site.js', '.nojekyll', REPORT]
SOURCE_FILES = ['README.md', 'HANDOFF.md', '.gitignore', 'DESIGN.md',
                'design-contract.md', 'implementation-handoff.md',
                'Preview.command', 'Preview.bat']


def media_paths(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in ('src', 'poster') and child:
                if not child.startswith('assets/') or '..' in Path(child).parts:
                    raise ValueError(f'Expected a bundled relative media path: {child}')
                yield Path(child)
            else:
                yield from media_paths(child)
    elif isinstance(value, list):
        for child in value:
            yield from media_paths(child)


def files_under(directory):
    return [p.relative_to(ROOT) for p in (ROOT / directory).rglob('*')
            if p.is_file() and not p.is_symlink()
            and '__pycache__' not in p.parts and p.name != '.DS_Store'
            and p.suffix not in ('.pyc', '.log')]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['site', 'handoff'], default='site')
    args = parser.parse_args()
    handoff = args.mode == 'handoff'
    destination = ROOT / ('output/handoff/a2meas-homepage' if handoff else 'dist')
    selected = {Path(p) for p in WEB_FILES}
    selected.update(files_under('data'))
    selected.update(p for p in files_under('assets')
                    if p.parts[1] not in ('videos', 'posters'))
    selected.update(media_paths(json.loads((ROOT / 'data/videos.json').read_text())))
    if handoff:
        selected.update(Path(p) for p in SOURCE_FILES)
        for directory in ['scripts', 'figure', 'logo']:
            selected.update(files_under(directory))
    missing = [str(p) for p in sorted(selected) if not (ROOT / p).is_file()]
    if missing:
        raise SystemExit('Missing required files: ' + ', '.join(missing))
    oversized = [str(p) for p in selected if (ROOT / p).stat().st_size >= 100 * 1024**2]
    if oversized:
        raise SystemExit('Files reach GitHub regular-Git limit: ' + ', '.join(oversized))
    # Only these fixed, generated destinations may be replaced.
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    records = []
    for relative in sorted(selected):
        source = ROOT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        records.append({'path': relative.as_posix(), 'bytes': target.stat().st_size,
                        'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
    manifest = {'mode': args.mode, 'files': records,
                'total_bytes': sum(row['bytes'] for row in records),
                'excluded': ['demo/', 'Tech Report/', 'output/', '.git/',
                             'unreferenced video and poster copies', 'credentials'],
                'published': False}
    (destination / 'package-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'{len(records)} files, {manifest["total_bytes"] / 1024**2:.1f} MiB: {destination}')
    if handoff:
        archive = destination.with_suffix('.zip')
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=1) as z:
            for file in sorted(destination.rglob('*')):
                if file.is_file():
                    z.write(file, Path(destination.name) / file.relative_to(destination))
        print(f'ZIP: {archive} ({archive.stat().st_size / 1024**2:.1f} MiB)')


if __name__ == '__main__':
    main()
