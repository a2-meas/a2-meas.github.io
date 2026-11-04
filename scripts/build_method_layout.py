from pathlib import Path
import re,json
from method_plates import plate_svg, correction_clip_svg
root=Path(__file__).resolve().parent.parent;records=json.loads((root/'assets/figures/method/sources.json').read_text());html=(root/'index.html').read_text()
for group in dict.fromkeys(x['group'] for x in records):
 items=[x for x in records if x['group']==group];w=items[0]['page_width'];h=items[0]['page_height']
 parts=[f'<figure class="method-flow flow-{group}" data-method-flow role="group" aria-label="{group.replace("-"," ")} modules"><div class="flow-canvas" style="aspect-ratio:{w}/{h}">']
 parts.append(f'<img class="flow-connections" src="assets/figures/method/{group}-connections.svg" width="{w}" height="{h}" alt="Original arrows connecting the modules in the paper diagram." loading="lazy">')
 for i,x in enumerate(items):
  a,b,c,d=x['bounds'];pos=f'left:{a/w*100}%;top:{b/h*100}%;width:{(c-a)/w*100}%;height:{(d-b)/h*100}%;'
  plate=plate_svg(x,root) if group=='action-model' else ''
  if group=='correction-interface': parts.append(correction_clip_svg(x,root))
  parts.append(f'''<button type="button" style="{pos}" class="flow-module tone-{x['color']}{' is-active' if x['stage']==items[0]['stage'] else ''}" data-flow-module="{x['letter']}" data-flow-stage="{x['stage']}" data-figure="{x.get('zoom_asset',x['asset'])}" data-caption="{x['title']}" aria-pressed="{'true' if x['stage']==items[0]['stage'] else 'false'}" aria-label="Enlarge module {x['letter']}: {x['title']}">{plate}<img src="{x['asset']}" width="{x['width']}" height="{x['height']}" loading="lazy" alt="Original paper artwork: {x['title']}."><span class="flow-expand" aria-hidden="true">↗</span></button>''')
 parts.append('</div></figure>');pattern=r'<figure class="method-flow flow-'+group+r'".*?</figure>';
 if group=='action-model' and not re.search(pattern,html,flags=re.S):
  pattern=r'<figure class="paper-figure original-figure">\s*<button class="figure-button" data-figure="assets/figures/action-model.svg".*?</figure>'
 html,n=re.subn(pattern,'\n'.join(parts),html,flags=re.S);assert n==1
(root/'index.html').write_text(html)
