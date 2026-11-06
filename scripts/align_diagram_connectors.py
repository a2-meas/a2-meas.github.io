"""Draw cross-module connectors once, in a shared, unblurred SVG coordinate space.

Works from the existing source-derived SVGs; the original PDFs are never edited.
Extraction/layout scripts call this too, so regenerated diagrams retain the fix.
"""
import argparse
import copy
from pathlib import Path
import re
import xml.etree.ElementTree as E

ROOT = Path(__file__).resolve().parent.parent
NS = '{http://www.w3.org/2000/svg}'
E.register_namespace('', NS[1:-1])
E.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

# Exact source paths: shafts and their corresponding arrowheads stay together.
PREFIXES = {
    'framework': (
        'M484.92 569.22', 'M667.8 569.22',
        'M482.4 ', 'M450.72 530.35',
        'M671.04 ', 'M833.04 530.35',
        'M416.16 573.17', 'M833.04 589.01',
        'M780.48 494.73', 'M631.44 463.06',
        'M532.8 445.79', 'M372.24 494.73',
        'M631.44 428.51', 'M631.44 400.44',
        'M730.08 445.79', 'M783.36 400.44',
        'M414 495.45', 'M627.84 ', 'M813.24 400.44',
    ),
    'correction-training': (
        'M244 587H339V266H388.43', 'M398.59 266',
        'M687 526H745V419H774.34', 'M784.54 419',
    ),
    'execution-recovery': (
        'M363 645H455V539H483.19', 'M491.99 539',
        'M885 684H954V468H981.98', 'M991.88 468',
        'M1200 754V843H1141.02', 'M1131.12 843',
        'M448 843H29V506H51.98', 'M60.88 506',
    ),
}
GROUPS = ('framework', 'correction-interface', 'correction-training',
          'execution-recovery', 'action-model')


def separate_connectors(group, update_html=True):
    directory = ROOT / 'assets/figures' / ('framework' if group == 'framework' else 'method')
    stem = '' if group == 'framework' else group + '-'
    context_path = directory / (stem + 'connections.svg')
    overlay_path = directory / ('connectors.svg' if group == 'framework' else stem + 'connectors.svg')
    context = E.parse(context_path).getroot()
    if group == 'framework':
        modules = [directory / (name + '.svg') for name in ('reason', 'ground', 'correct', 'execute')]
    else:
        modules = [p for p in directory.glob(stem + '*.svg')
                   if p.stem.removeprefix(stem) in ('a', 'a-detail', 'b', 'c', 'c-current', 'd', 'e')]
    trees = {path: E.parse(path).getroot() for path in modules}
    trees[context_path] = context
    previous = E.parse(overlay_path).getroot() if overlay_path.exists() else None

    if group in PREFIXES:
        prefixes = PREFIXES[group]
        selected = lambda node: node.tag == NS + 'path' and node.get('d', '').startswith(prefixes)
        candidates = [node for tree in trees.values()
                      for node in tree.iter() if selected(node)]
        # A fresh PDF extraction wins over a previous, normalized overlay.
        # Otherwise old/new coordinates or linejoin values would be duplicated.
        if not candidates and previous is not None:
            candidates = [node for node in previous.iter() if selected(node)]
        # Source fill and outline may share a path; deduplicate exact nodes only.
        unique = {}
        for node in candidates:
            unique.setdefault(tuple(sorted(node.attrib.items())), copy.deepcopy(node))
        nodes = list(unique.values())
        assert all(any(n.get('d', '').startswith(prefix) for n in nodes) for prefix in prefixes), group
    else:
        # These groups already isolate the connectors from their module crops.
        # Move them out of the rasterized context into a small vector overlay.
        nodes = [copy.deepcopy(n) for n in context if n.tag == NS + 'path']
        if not nodes and previous is not None:
            nodes = [copy.deepcopy(n) for n in previous if n.tag == NS + 'path']
        assert len(nodes) == (3 if group == 'correction-interface' else 6), group
        keys = {tuple(sorted(n.attrib.items())) for n in nodes}
        selected = lambda node: node.tag == NS + 'path' and tuple(sorted(node.attrib.items())) in keys

    for path, tree in trees.items():
        for parent in tree.iter():
            # Do not alter definitions used by glyphs, masks, or source contours.
            if parent.tag == NS + 'defs':
                continue
            for node in list(parent):
                if node.get('id') == 'zoom-connectors' or selected(node):
                    parent.remove(node)
        if path == context_path:
            E.ElementTree(tree).write(path, encoding='unicode')

    overlay = E.Element(NS + 'svg', {
        'viewBox': context.get('viewBox'), 'width': context.get('width'),
        'height': context.get('height'), 'preserveAspectRatio': 'none',
    })
    for node in nodes:
        if group == 'framework':
            # Source shaft and head differ by .36 source units; share one axis.
            d = node.get('d', '')
            if d.startswith(('M482.4 529.99', 'M671.04 529.99')):
                node.set('d', d.replace('529.99', '530.35'))
            elif d.startswith('M414 495.45'):
                node.set('d', 'M414 495.45V475.17H627.84M635.04 475.17H813.24V404.04')
            elif d.startswith('M627.84 475.29'):
                node.set('d', d.replace('475.29', '475.17'))
        if node.get('stroke') and not node.get('d', '').endswith('Z'):
            node.set('stroke-linejoin', 'round')
        overlay.append(node)
    E.ElementTree(overlay).write(overlay_path, encoding='unicode')

    # Enlarged SVG crops keep their source connector stubs. Only the lightweight
    # inline raster preview omits this group, because the page draws it once.
    for path in modules:
        tree = trees[path]
        target = tree
        if group == 'framework':
            target = next(n for n in tree if n.get('clip-path', '').startswith('url(#original-framework-'))
        zoom = E.SubElement(target, NS + 'g', {'id': 'zoom-connectors'})
        zoom.extend(copy.deepcopy(nodes))
        E.ElementTree(tree).write(path, encoding='unicode')

    if update_html:
        html_path = ROOT / 'index.html'
        html = html_path.read_text()
        asset = overlay_path.relative_to(ROOT).as_posix()
        html = re.sub(r'<img\b[^>]*\bclass="flow-connectors"[^>]*\bsrc="' + re.escape(asset) + r'"[^>]*>\n?', '', html)
        context_asset = context_path.relative_to(ROOT).with_suffix('').as_posix()
        pattern = r'(<img\b[^>]*\bsrc="' + re.escape(context_asset) + r'\.(?:svg|webp)"[^>]*>)'
        tag = (f'<img class="flow-connectors" src="{asset}" width="{context.get("width")}" '
               f'height="{context.get("height")}" alt="" aria-hidden="true" loading="lazy" decoding="async">')
        html, count = re.subn(pattern, lambda m: m[1] + '\n' + tag, html)
        assert count == 1, f'Missing context image: {group}'
        html_path.write_text(html)
    return {'group': group, 'vector_paths': len(nodes), 'bytes': overlay_path.stat().st_size}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--group', choices=GROUPS)
    args = parser.parse_args()
    for group in ([args.group] if args.group else GROUPS):
        print(separate_connectors(group))
