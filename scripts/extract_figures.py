#!/usr/bin/env python3
"""Export supplied PDF artwork as SVG, preserving the original paths and images."""
import json
from pathlib import Path
import pymupdf

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/figures'
OUT.mkdir(parents=True, exist_ok=True)
REPORT = 'To_the_Era_of_Agentic_Embodied_Intelligence.pdf'
SOURCES = [
    ('framework', 'figure/architecture_slide8_cropped.pdf', 1, (7, 13, 1022.5, 520)),
    ('action-model', 'figure/第16页_模型结构_裁剪.pdf', 1, (3, 3, 1080.5, 604.5)),
    ('correction-interface', 'figure/figure3.pdf', 1, (6, 5.5, 503, 354)),
    ('correction-training', 'figure/figure4.pdf', 1, (10.5, 12, 497, 260.5)),
    ('execution-recovery', 'figure/figure5.pdf', 1, (5, 4.5, 504, 311.5)),
    # Crop only the artwork. Paper captions are rendered separately as HTML.
    ('coffee-recovery', REPORT, 36, (70.866, 80.9445, 541.1243, 512.763)),
    ('training-systems', REPORT, 23, (69, 406, 540, 581)),
    ('training-throughput', REPORT, 25, (69, 163, 534, 338)),
]
records = []
for name, relative, number, bounds in SOURCES:
    with pymupdf.open(ROOT / relative) as source:
        page = source[number - 1]
        if name == 'coffee-recovery':
            # The renewed report embeds this complete figure as one PNG.
            # Extract its original pixels, excluding the separate paper caption.
            images = page.get_images(full=True)
            assert len(images) == 1, 'Recovery figure image is ambiguous'
            image = source.extract_image(images[0][0])
            assert image['ext'] == 'png'
            asset = f'assets/figures/{name}.png'
            (ROOT / asset).write_bytes(image['image'])
            records.append({'id': name, 'source': relative, 'page': number,
                            'clip': bounds, 'width': image['width'], 'height': image['height'],
                            'format': 'original embedded PNG extracted losslessly; no screenshot',
                            'asset': asset})
            print(name, image['width'], image['height'], 'original embedded PNG')
            continue
        if bounds:
            clip = pymupdf.Rect(bounds)
            canvas = pymupdf.open()
            page_out = canvas.new_page(width=clip.width, height=clip.height)
            page_out.show_pdf_page(page_out.rect, source, number - 1, clip=clip)
        else:
            canvas = None
            page_out = page
        # Use the original PDF glyph outlines to prevent browser font substitutions.
        (OUT / f'{name}.svg').write_text(page_out.get_svg_image(text_as_path=True))
        records.append({'id': name, 'source': relative, 'page': number, 'clip': bounds,
                        'width': page_out.rect.width, 'height': page_out.rect.height,
                        'safety_margin_pt': 3, 'format': 'original PDF vectors and embedded images',
                        'asset': f'assets/figures/{name}.svg'})
        print(name, round(page_out.rect.width, 2), round(page_out.rect.height, 2))
        if canvas:
            canvas.close()
(OUT / 'sources.json').write_text(json.dumps(records, indent=2, ensure_ascii=False) + '\n')
