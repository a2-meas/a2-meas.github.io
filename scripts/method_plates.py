"""Shape-aligned SVG backplates for the original A²-WLA artwork."""
import copy
import xml.etree.ElementTree as E
from pathlib import Path
from action_model_layout import ROW_SHIFT, QWEN_SHIFT, CONTEXT_SHIFT, HISTORY_RIGHT, CONTEXT_LEFT, CONTEXT_RIGHT

NS='{http://www.w3.org/2000/svg}'

def plate_svg(item, root):
    letter=item['letter'];x,y,r,b=item['bounds']
    svg=E.Element('svg',{'class':'flow-plate','viewBox':f'{x} {y} {r-x} {b-y}','aria-hidden':'true','focusable':'false'})
    shapes=[]
    # Copy original rounded outer paths rather than approximating their corners.
    if letter in ('c','d'):
        tree=E.parse(root/'assets/figures/method/action-model-d.svg').getroot()
        prefix='M134.28 649.77' if letter=='c' else 'M770.04 649.77'
        original=next(e for e in tree.iter() if e.get('d','').startswith(prefix))
        shapes.append(E.Element('path',{'d':original.get('d'),'transform':original.get('transform')}))
    def rect(a,c,w,h,rx=3):
        shapes.append(E.Element('rect',{'x':str(a),'y':str(c),'width':str(w),'height':str(h),'rx':str(rx)}))
    if letter=='a':rect(3,240+ROW_SHIFT,HISTORY_RIGHT-3,164,5)
    elif letter=='a-detail':rect(3,463,1078,141,5)
    elif letter=='b':rect(349.5,301.7+QWEN_SHIFT,141.8,76.3,4)
    elif letter=='c-current':rect(CONTEXT_LEFT,328+CONTEXT_SHIFT,CONTEXT_RIGHT-CONTEXT_LEFT,51,3)
    elif letter=='d':
        rect(782.2,390.2,174.3,35.3,3)
        rect(980,389,95,56,3)
    ident='plate-'+letter
    defs=E.SubElement(svg,'defs');clip=E.SubElement(defs,'clipPath',{'id':ident,'clipPathUnits':'userSpaceOnUse'})
    for shape in shapes:clip.append(copy.deepcopy(shape))
    g=E.SubElement(svg,'g',{'clip-path':f'url(#{ident})'})
    for shape in shapes:shape.set('class','plate-fill');g.append(shape)
    return E.tostring(svg,encoding='unicode')


def correction_clip_svg(item, root):
    letter=item['letter']; x,y,r,b=item['bounds']
    source=E.parse(root/item['asset']).getroot()
    prefix='M27 20H1173' if letter=='a' else 'M27 360H1173'
    original=next(e for e in source.iter() if e.get('d','').startswith(prefix))
    import re
    values=[float(v) for v in re.split('[, ]+',re.search(r'matrix\(([^)]+)',original.get('transform'))[1])]
    a,c,d,f,tx,ty=values
    transform=f'matrix({a/(r-x)} {c/(b-y)} {d/(r-x)} {f/(b-y)} {(tx-x)/(r-x)} {(ty-y)/(b-y)})'
    return '<svg class="flow-clip-defs" width="0" height="0" aria-hidden="true"><defs><clipPath id="correction-'+letter+'-clip" clipPathUnits="objectBoundingBox"><path d="'+original.get('d')+'" transform="'+transform+'"/></clipPath></defs></svg>'
