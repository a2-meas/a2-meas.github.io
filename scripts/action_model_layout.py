"""Space the source-vector history row and keep its connectors on one axis."""
import xml.etree.ElementTree as E

NS = '{http://www.w3.org/2000/svg}'
ROW_SHIFT = 12
ROW_AXIS = (316.81 + 369.35) / 2 + ROW_SHIFT
QWEN_SHIFT = ROW_AXIS - (301.7 + 377.99) / 2
CONTEXT_SHIFT = ROW_AXIS - (333.726 + 349.56) / 2
OFFSETS = {'a': ROW_SHIFT, 'b': QWEN_SHIFT, 'c-current': CONTEXT_SHIFT}
HISTORY_RIGHT = 329
CONTEXT_LEFT, CONTEXT_RIGHT = 508.22, 598


def space_history_row(root):
    """Translate original groups, retaining their glyphs, images and clip paths.

    Inter-module arrows are returned separately so they stay sharp and are drawn
    once, even while the independently highlighted module images are blurred.
    Original report PDFs are never modified.
    """
    container = next(n for n in root.iter() if any(
        ''.join(c.get('data-text', '') for c in child.iter()) == 'Observation history'
        for child in n))
    children = list(container)

    def label_index(text):
        matches = [i for i, child in enumerate(children)
                   if ''.join(c.get('data-text', '') for c in child.iter()) == text]
        assert matches, f'Missing source label: {text}'
        return matches[0]

    def translate(child, dy):
        wrapper = E.Element(NS + 'g', {'transform': f'translate(0 {dy:g})'})
        i = list(container).index(child)
        container.remove(child)
        wrapper.append(child)
        container.insert(i, wrapper)

    for child in children[label_index('Observation history'):label_index('Visual tokens') + 1]:
        translate(child, ROW_SHIFT)
    qwen_start = next(i for i, child in enumerate(children) if any(
        n.get('d', '').startswith('M477 355.77') for n in child.iter()))
    for child in children[qwen_start:label_index('2B parameters') + 1]:
        translate(child, QWEN_SHIFT)
    for label in ('Predicted latent action', 'Policy inference'):
        translate(children[label_index(label)], ROW_SHIFT)
    token_start = next(i for i, child in enumerate(children) if any(
        n.get('d', '').startswith('M642.96 313.36') for n in child.iter()))
    for child in children[token_start:label_index('Current context') + 1]:
        translate(child, CONTEXT_SHIFT)
    # Qwen's original embedded logo occurs later in the PDF paint order.
    logo = next(child for child in children if any(
        n.tag == NS + 'g' and '375.06,317.17799' in n.get('transform', '')
        for n in child.iter()))
    translate(logo, QWEN_SHIFT)
    instruction = children[label_index('F'):]
    assert ''.join(c.get('data-text', '') for n in instruction for c in n.iter()) == 'Full task instruction'
    for child in instruction:
        translate(child, ROW_SHIFT)

    def path_start(prefix):
        matches = [n for n in root.iter() if n.get('d', '').startswith(prefix)]
        assert len(matches) == 1, f'Expected one original arrow: {prefix}'
        return matches[0]

    def remove_path(prefix):
        node = path_start(prefix)
        parent = next(p for p in root.iter() if node in list(p))
        parent.remove(node)

    # Earlier → Current remains part of the history artwork.
    earlier = path_start('M170.28 393.39')
    earlier.set('transform', f'translate(0 {ROW_SHIFT}) ' + earlier.get('transform', ''))

    def right_arrow(start, end, color):
        y = ROW_AXIS
        return E.Element(NS + 'path', {
            'd': f'M{start:g} {y-.5:g}H{end-3:g}V{y+.5:g}H{start:g}Z '
                 f'M{end-4:g} {y-2:g}L{end:g} {y:g}L{end-4:g} {y+2:g}Z',
            'fill': color})

    remove_path('M277.56 322.14')
    # Center the input arrow on the front encoder panel as well.
    container.append(right_arrow(150.06, 193.08, '#608f98'))
    for prefix in ('M446.76 322.14', 'M548.78 361.32',
                   'M618.84 322.14', 'M712.44 322.14', 'M243.72 241.98'):
        remove_path(prefix)
    shared = [right_arrow(HISTORY_RIGHT + 1.5, 349.5, '#608f98'),
              right_arrow(491.34, CONTEXT_LEFT, '#6485a5'),
              right_arrow(CONTEXT_RIGHT + 1.5, 642.54, '#6485a5')]
    x, top = (349.5 + 491.34) / 2, 205.26
    qwen_top, qwen_bottom = 301.7 + QWEN_SHIFT, 377.99 + QWEN_SHIFT
    shared.append(E.Element(NS + 'path', {
        'd': f'M{x-.5:g} {top+3:g}V{qwen_top:g}H{x+.5:g}V{top+3:g}Z '
             f'M{x-2:g} {top+4:g}L{x:g} {top:g}L{x+2:g} {top+4:g}Z',
        'fill': '#6485a5'}))
    x, bottom = 420.42, 420.44 + ROW_SHIFT
    shared.extend([
        E.Element(NS + 'path', {
            'd': f'M116.22 {bottom:g}H{x:g}V{qwen_bottom+3:g}',
            'fill': 'none', 'stroke': '#948980', 'stroke-width': '1',
            'stroke-linejoin': 'round'}),
        E.Element(NS + 'path', {
            'd': f'M{x-2:g} {qwen_bottom+4:g}L{x:g} {qwen_bottom:g}L{x+2:g} {qwen_bottom+4:g}Z',
            'fill': '#948980'})])
    return shared


def spaced_bounds(letter, bounds):
    x, y, r, b = bounds
    dy = OFFSETS.get(letter, 0)
    return x, y + dy, r, b + dy
