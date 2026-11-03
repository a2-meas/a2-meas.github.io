"""Original diagonal folded ribbons, tiled seamlessly for rightward motion."""
from pathlib import Path
OUT=Path(__file__).resolve().parent.parent/'assets/backgrounds';OUT.mkdir(exist_ok=True)
# One period contains four orange/green pairs. Original gradients are retained.
svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1056 1000" preserveAspectRatio="none">
<defs>
 <linearGradient id="orange">
  <stop stop-color="#e9c39b" stop-opacity="0"/>
  <stop offset=".07" stop-color="#ecc299" stop-opacity=".14"/>
  <stop offset=".28" stop-color="#e1a776" stop-opacity=".25"/>
  <stop offset=".8" stop-color="#e5b88b" stop-opacity=".44"/>
  <stop offset=".98" stop-color="#f1d6bb" stop-opacity=".67"/>
  <stop offset="1" stop-color="#fff9ef" stop-opacity=".95"/>
 </linearGradient>
 <linearGradient id="green">
  <stop stop-color="#adc8a8" stop-opacity="0"/>
  <stop offset=".2" stop-color="#9dbd9b" stop-opacity=".19"/>
  <stop offset=".8" stop-color="#96b596" stop-opacity=".44"/>
  <stop offset=".98" stop-color="#d5e3cb" stop-opacity=".67"/>
  <stop offset="1" stop-color="#faffee" stop-opacity=".95"/>
 </linearGradient>
 <pattern id="ribbons" width="264" height="1000" patternUnits="userSpaceOnUse" patternTransform="matrix(1 0 .8 1 0 0)">
  <rect width="132" height="1000" fill="url(#orange)"/>
  <rect x="132" width="132" height="1000" fill="url(#green)"/>
 </pattern>
</defs>
<rect width="1056" height="1000" fill="url(#ribbons)"/>
</svg>'''
(OUT/'cover-ribbons.svg').write_text(svg)
print('Seamless original diagonal ribbon pattern:1056px = 4 × 264px')
