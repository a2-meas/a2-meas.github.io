#!/usr/bin/env python3
"""Crop original Framework vectors and reuse their exact contours for animation."""
import copy
import json
from pathlib import Path
import re
import xml.etree.ElementTree as E

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/figures/framework'
SOURCE = 'figure/architecture_slide8_cropped.pdf'
NS = '{http://www.w3.org/2000/svg}'
E.register_namespace('', NS[1:-1])
E.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
CLIP = (7, 13, 1022.5, 520)
STAGES = [
    dict(id='reason', title='Reason about the goal', color='orange', paths=[1],
         copy='MetaBrain maintains the goal, reviews progress and specifies how a recovery attempt should change.'),
    dict(id='ground', title='Ground the diagnosis', color='blue', paths=[3],
         copy='When physical conditions are unresolved, diagnostic agents verify objects, motion, contact and feasibility.'),
    dict(id='correct', title='Encode the correction', color='purple', paths=[4, 110],
         copy='For recovery, the context combines guidance, evidence, executed history and a fresh proposal. The adapter conditions action generation.'),
    dict(id='execute', title='Act, observe & verify', color='green', paths=[2, 18],
         regions=[(309, 54, 503, 153)],
         copy='A²-WLA executes an action prefix. Fresh observations and the shared execution record inform the next decision.')
]


def original_path(drawing):
    """Copy original PDF Bézier coordinates, without rounding the panel shape."""
    commands = []
    last = None
    for item in drawing['items']:
        kind, *points = item
        if kind not in ('l', 'c'):
            raise ValueError(f'Unexpected panel geometry: {kind}')
        if last != points[0]:
            commands.append(f'M{points[0].x} {points[0].y}')
        if kind == 'l':
            commands.append(f'L{points[1].x} {points[1].y}')
        else:
            commands.append('C' + ' '.join(f'{p.x} {p.y}' for p in points[1:]))
        last = points[-1]
    commands.append('Z')
    return E.Element(NS + 'path', {'d': ''.join(commands)})


def wrap_contents(root, attribute):
    group = E.Element(NS + 'g', attribute)
    for child in list(root):
        if child.tag != NS + 'defs':
            root.remove(child)
            group.append(child)
    root.append(group)


def main():
    OUT.mkdir(exist_ok=True)
    with pymupdf.open(ROOT / SOURCE) as document:
        page = document[0]
        drawings = page.get_drawings()
        root = E.fromstring(page.get_svg_image(text_as_path=True))
        # Remove only the original full-page white paint; keep internal whites.
        white = next(node for node in root.iter()
                     if node.get('fill') == '#ffffff' and node.get('d', '').startswith('M0 .28363H1442.16'))
        for parent in root.iter():
            if white in list(parent):
                parent.remove(white)
                break
        # Source outer panel fills are replaced by HTML/SVG color plates.
        panel_prefixes = ['M180.36 568.03', 'M702.36 614.93', 'M180.36 390.35',
                          'M702.36 392.15', 'M534.6 457.16']
        for node in root.iter():
            if node.get('fill') and any(node.get('d', '').startswith(prefix) for prefix in panel_prefixes):
                node.set('fill', 'none')
            # The source paints Adapter after its vertical connector. Keep that
            # opaque source layer so the connector stops at the box, not the text.
            if node.get('fill') not in (None, 'none') and node.get('d', '').startswith('M915.48 '):
                node.set('fill', '#eee5f2')
        records = []
        shapes_by_stage = {}
        for stage in STAGES:
            shapes = [original_path(drawings[i]) for i in stage['paths']]
            regions = [pymupdf.Rect(drawings[i]['rect']) for i in stage['paths']]
            for bounds in stage.get('regions', []):
                rect = pymupdf.Rect(bounds)
                regions.append(rect)
                shapes.append(E.Element(NS + 'rect', {
                    'x': str(rect.x0), 'y': str(rect.y0),
                    'width': str(rect.width), 'height': str(rect.height)}))
            bounds = regions[0]
            for rect in regions[1:]:
                bounds = bounds | rect
            shapes_by_stage[stage['id']] = shapes
            asset = copy.deepcopy(root)
            asset.set('viewBox', f'{bounds.x0} {bounds.y0} {bounds.width} {bounds.height}')
            asset.set('width', str(bounds.width))
            asset.set('height', str(bounds.height))
            asset.set('preserveAspectRatio', 'none')
            clip_id = 'original-framework-' + stage['id']
            clip = E.SubElement(asset.find(NS + 'defs'), NS + 'clipPath',
                                {'id': clip_id, 'clipPathUnits': 'userSpaceOnUse'})
            clip.extend(copy.deepcopy(shapes))
            wrap_contents(asset, {'clip-path': f'url(#{clip_id})'})
            path = OUT / f"{stage['id']}.svg"
            E.ElementTree(asset).write(path, encoding='unicode')
            records.append({**stage, 'bounds': list(bounds), 'source': SOURCE,
                            'asset': path.relative_to(ROOT).as_posix(),
                            'contours': [E.tostring(s, encoding='unicode') for s in shapes]})
        connections = copy.deepcopy(root)
        # Panels render their original outline in their own stage asset. A
        # shape-hole mask removes only the inner half of a centered stroke,
        # leaving a second rim outside the hole. Remove those strokes from the
        # connections layer completely, while retaining every connector.
        for node in connections.iter():
            if node.get('stroke') and any(node.get('d', '').startswith(prefix)
                                          for prefix in [*panel_prefixes, 'M915.48 ']):
                node.set('stroke', 'none')
        x, y, right, bottom = CLIP
        width, height = right - x, bottom - y
        connections.set('viewBox', f'{x} {y} {width} {height}')
        connections.set('width', str(width))
        connections.set('height', str(height))
        mask = E.SubElement(connections.find(NS + 'defs'), NS + 'mask',
                            {'id': 'framework-module-holes', 'maskUnits': 'userSpaceOnUse',
                             'x': str(x), 'y': str(y), 'width': str(width), 'height': str(height)})
        E.SubElement(mask, NS + 'rect', {'x': str(x), 'y': str(y), 'width': str(width),
                                       'height': str(height), 'fill': 'white'})
        for shapes in shapes_by_stage.values():
            for shape in copy.deepcopy(shapes):
                shape.set('fill', 'black')
                mask.append(shape)
        wrap_contents(connections, {'mask': 'url(#framework-module-holes)'})
        E.ElementTree(connections).write(OUT / 'connections.svg', encoding='unicode')

    parts = ['<div class="framework-flow" id="framework-flow" data-framework-flow role="group" aria-label="Framework: reasoning, diagnosis, correction and execution">',
             '<figure class="paper-figure framework-figure"><div class="framework-diagram-scroll"><div class="flow-canvas" style="aspect-ratio:1015.5/507">',
             '<img class="flow-connections" src="assets/figures/framework/connections.svg" width="1016" height="507" loading="lazy" alt="Original nominal-control, recovery and feedback connections from the paper.">']
    for item in records:
        a, b, c, d = item['bounds']
        w, h = c - a, d - b
        ident = 'framework-' + item['id']
        # The outer HTML button clips both blur and plate to the same union of
        # original contours. Disconnected source pieces remain disconnected.
        transform = f'matrix({1/w} 0 0 {1/h} {-a/w} {-b/h})'
        normalized = []
        for raw in item['contours']:
            shape = E.fromstring(raw)
            shape.set('transform', transform)
            normalized.append(E.tostring(shape, encoding='unicode'))
        # clipPath children must be shapes, not a grouped <g> (WebKit).
        parts.append(f'<svg class="flow-clip-defs" width="0" height="0" aria-hidden="true"><defs><clipPath id="{ident}-clip" clipPathUnits="objectBoundingBox">{"".join(normalized)}</clipPath></defs></svg>')
        plate = E.Element('svg', {'class': 'flow-plate', 'viewBox': f'{a} {b} {w} {h}',
                                 'preserveAspectRatio': 'none',
                                 'aria-hidden': 'true', 'focusable': 'false'})
        for i, shape in enumerate(shapes_by_stage[item['id']]):
            # Observation-history images have no outer box in the source.
            if i >= len(item['paths']):
                continue
            node = copy.deepcopy(shape)
            node.set('class', 'plate-fill')
            plate.append(node)
        position = f'left:{(a-x)/width*100}%;top:{(b-y)/height*100}%;width:{w/width*100}%;height:{h/height*100}%;clip-path:url(#{ident}-clip)'
        title = item['title'].replace('&', '&amp;')
        active = item['id'] == 'reason'
        parts.append(f'<button type="button" class="flow-module framework-module tone-{item["color"]}{" is-active" if active else ""}" style="{position}" data-flow-module="{item["id"]}" data-figure="{item["asset"]}" data-caption="{title}" aria-pressed="{str(active).lower()}" aria-label="Enlarge Framework module: {title}">{E.tostring(plate, encoding="unicode")}<img src="{item["asset"]}" width="{w}" height="{h}" loading="lazy" alt="Original paper artwork: {title}."></button>')
    parts.extend(['</div></div><figcaption>The A²-MEAS framework</figcaption></figure>',
                  '<div class="principles" id="framework-stages" role="group" aria-label="Four functional stages of the framework">'])
    for index, item in enumerate(records, 1):
        active = index == 1
        parts.append(f'<button class="principle-card tone-{item["color"]}{" is-active" if active else ""}" data-flow-peer="{item["id"]}" type="button" aria-pressed="{str(active).lower()}" aria-labelledby="principle-title-{index}" aria-describedby="principle-copy-{index}"><span class="principle-number" aria-hidden="true">0{index}</span><span class="principle-title" id="principle-title-{index}">{item["title"].replace("&", "&amp;")}</span><span class="principle-copy" id="principle-copy-{index}">{item["copy"]}</span></button>')
    parts.extend(['</div>', '</div>'])
    html_path = ROOT / 'index.html'
    html = html_path.read_text()
    pattern = r'<div class="framework-flow".*?<!-- framework-flow-end -->'
    if not re.search(pattern, html, flags=re.S):
        pattern = r'<figure class="paper-figure original-figure">\s*<button class="figure-button" data-figure="assets/figures/framework.svg".*?<div class="principles".*?</div>'
    html, count = re.subn(pattern, '\n'.join(parts) + '\n<!-- framework-flow-end -->', html, count=1, flags=re.S)
    assert count == 1, 'Framework target missing or ambiguous'
    html_path.write_text(html)
    (OUT / 'sources.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
    print('Framework: four original-vector stage groups, exact contours and synchronized peer cards')


if __name__ == '__main__':
    main()
