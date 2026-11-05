#!/usr/bin/env python3
"""Extract original vector regions; remove full-page white paint, not internal whites."""
import argparse, json, re, copy
from pathlib import Path
import xml.etree.ElementTree as ET
import pymupdf
from action_model_layout import space_history_row, spaced_bounds
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/figures/method'; OUT.mkdir(exist_ok=True)
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
# Bounds in original PDF coordinates; original text and glyphs are preserved.
GROUPS=[
 ('action-model','figure/action-model-renew.pdf',[
  ('a','Motion-aware visual history','green',(3,240,343,405)),
  ('a-detail','Motion-aware history encoder — detail','green',(3,463,1081,604)),
  ('b','Task interpretation with Qwen3-VL','orange',(344,296,496,383)),
  ('c','Multiview future-context prediction','teal',(3,3,608,242)),
  ('c-current','Current-context tokens','teal',(500,328,640,379)),
  ('d','Continuous action generation','blue',(642,3,1081,449))]),
 ('correction-interface','figure/figure3.pdf',[
  ('a','Encode grounded context once','orange',(8,8,501,145)),
  ('b','Correct the action flow at every step','blue',(8,151.5,501,353))]),
 ('correction-training','figure/figure4.pdf',[
  ('a','Causal proposal','orange',(11,12,117,245)),
  ('b','Mine deviations','blue',(125,12,262,245)),
  ('c','Ground, annotate & assemble','green',(266,12,496,258))]),
 ('execution-recovery','figure/figure5.pdf',[
  ('a','Nominal execution','blue',(6,4,503,91)),
  ('b','Stop & ground','orange',(6,97,158,295)),
  ('c','Regenerate from fresh state','blue',(166,97,332,282)),
  ('d','Check, act & verify','green',(344,97,503,282)),
  ('e','Log and update the recovery query','purple',(158,285.5,399,309))])]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--group',choices=[item[0] for item in GROUPS])
args=parser.parse_args()
records=json.loads((OUT/'sources.json').read_text()) if args.group else []
if args.group:
 records=[item for item in records if item['group']!=args.group]
for group,source,modules in GROUPS:
 if args.group and group!=args.group: continue
 with pymupdf.open(ROOT/source) as doc:
  page=doc[0]; root=ET.fromstring(page.get_svg_image(text_as_path=True)); removed=0
  for parent in root.iter():
   for node in list(parent):
    d=node.get('d',''); fill=node.get('fill','')
    # Only simple, page-sized white rectangles, never white node fills or glyphs.
    match=re.fullmatch(r'M([\d.\-]+) ([\d.\-]+)H([\d.\-]+)V([\d.\-]+)H([\d.\-]+)Z',d)
    if fill.lower() in ('#ffffff','#fff','white') and match:
     vals=list(map(float,match.groups())); matrix=re.search(r'matrix\(([^)]+)',node.get('transform',''))
     v=[float(x) for x in re.split('[, ]+',matrix[1])] if matrix else [1,0,0,1,0,0]
     if abs((vals[2]-vals[0])*v[0]) >= page.rect.width*.95 and abs((vals[3]-vals[1])*v[3])>=page.rect.height*.95:
      parent.remove(node); removed+=1
  # Render the a→b correction-code connector once on the full diagram. Splitting
  # one original path between independently scaled/blurred modules makes visible
  # kinks at the panel boundary even though the source path is orthogonal.
  shared_connectors=[]
  if group=='action-model':
   shared_connectors=space_history_row(root)
   modules=[(letter,title,color,spaced_bounds(letter,bounds)) for letter,title,color,bounds in modules]
   whole=copy.deepcopy(root)
   for connector in shared_connectors: whole.append(copy.deepcopy(connector))
   ET.ElementTree(whole).write(ROOT/'assets/figures/action-model.svg',encoding='unicode')
  zoom_root=copy.deepcopy(root) if group=='correction-interface' else None
  if group=='correction-interface':
   shared_paths={'M1106 186H1156V419H645V492.2',
                 'M645 502.46 639.87 492.2H650.13L645 502.46Z'}
   for parent in root.iter():
    for child in list(parent):
     if child.get('d') in shared_paths:
      shared_connectors.append(copy.deepcopy(child));parent.remove(child)
   assert len(shared_connectors)==3, 'Expected original connector and arrowhead'
  # Keep the original full diagram outside the module rectangles: connectors and retry.
  ns='{http://www.w3.org/2000/svg}'
  context=copy.deepcopy(root)
  defs=context.find(ns+'defs')
  mask=ET.SubElement(defs,ns+'mask',{'id':'module-holes','maskUnits':'userSpaceOnUse','x':'0','y':'0','width':str(page.rect.width),'height':str(page.rect.height)})
  ET.SubElement(mask,ns+'rect',{'x':'0','y':'0','width':str(page.rect.width),'height':str(page.rect.height),'fill':'white'})
  outlines=[]
  for letter,_,_,(x,y,r,b) in modules:
   if group=='correction-interface':
    prefix='M27 20H1173' if letter=='a' else 'M27 360H1173'
    original=next(e for e in root.iter() if e.get('d','').startswith(prefix))
    shape=ET.Element(ns+'path',{'d':original.get('d'),'transform':original.get('transform'),'fill':'black'})
    mask.append(copy.deepcopy(shape));outlines.append((letter,shape))
   else:
    ET.SubElement(mask,ns+'rect',{'x':str(x),'y':str(y),'width':str(r-x),'height':str(b-y),'fill':'black'})
  content=ET.Element(ns+'g',{'mask':'url(#module-holes)'})
  for child in list(context):
   if child.tag!=ns+'defs': context.remove(child);content.append(child)
  context.append(content)
  for letter,shape in outlines:
   ident='sharp-panel-'+letter
   cp=ET.SubElement(defs,ns+'clipPath',{'id':ident,'clipPathUnits':'userSpaceOnUse'});cp.append(copy.deepcopy(shape))
   line=copy.deepcopy(shape);line.set('fill','none');line.set('stroke','#b6814b' if letter=='a' else '#7298ba');line.set('stroke-width','2')
   sharp=ET.SubElement(context,ns+'g',{'clip-path':'url(#'+ident+')'});sharp.append(line)
  if shared_connectors:
   context.set('preserveAspectRatio','none')
   for connector in shared_connectors:context.append(connector)
  ET.ElementTree(context).write(OUT/f'{group}-connections.svg',encoding='unicode')
  for letter,title,color,bounds in modules:
   x,y,r,b=bounds; node=copy.deepcopy(root)
   node.set('viewBox',f'{x} {y} {r-x} {b-y}'); node.set('width',str(r-x)); node.set('height',str(b-y))
   if group=='correction-interface':node.set('preserveAspectRatio','none')
   if group=='action-model' and letter in ('c','d'):
    for element in node.iter():
     if element.get('fill') in ('#f8fbfa','#fbfcfd'):
      element.set('fill','none')
   asset=f'assets/figures/method/{group}-{letter}.svg'
   ET.ElementTree(node).write(ROOT/asset,encoding='unicode')
   records.append(dict(stage=letter.split('-')[0],group=group,letter=letter,title=title,color=color,source=source,bounds=bounds,width=r-x,height=b-y,asset=asset,removed_page_backgrounds=removed,page_width=page.rect.width,page_height=page.rect.height))
   if group=='action-model':
    records[-1].update(report_source='To_the_Era_of_Agentic_Embodied_Intelligence_renew.pdf',report_page=16)
   if zoom_root is not None:
    zoom=copy.deepcopy(zoom_root)
    zoom.set('viewBox',f'{x} {y} {r-x} {b-y}');zoom.set('width',str(r-x));zoom.set('height',str(b-y));zoom.set('preserveAspectRatio','none')
    zoom_asset=f'assets/figures/method/{group}-{letter}-original.svg'
    ET.ElementTree(zoom).write(ROOT/zoom_asset,encoding='unicode')
    records[-1]['zoom_asset']=zoom_asset
records.sort(key=lambda item: [group[0] for group in GROUPS].index(item['group']))
(OUT/'sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(f'Extracted {len(records)} original vector modules')
