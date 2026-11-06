// Render lightweight previews from the source-derived SVGs, never screenshots.
// Original SVGs remain the enlargement assets.
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require('sharp');
const root = path.resolve(__dirname, '..');
(async () => {
  const htmlPath = path.join(root, 'index.html');
  let html = await fs.readFile(htmlPath, 'utf8');
  const sources = [...html.matchAll(/<img\b[^>]*\bsrc="(assets\/figures\/(?:method|framework)\/[^".]+)\.(?:svg|webp)"/g)].map(m => m[1]);
  const records = [];
  // Cross-module links remain vectors: rasterizing them reintroduces seams.
  for (const stem of [...new Set(sources)].filter(stem => !/(?:\/|-)connectors$/.test(stem))) {
    const original = await fs.readFile(path.join(root, stem + '.svg'));
    // Enlargements retain connector stubs; inline previews use the shared layer.
    const source = Buffer.from(original.toString().replace(/<g id="zoom-connectors">[\s\S]*?<\/g>/g, ''));
    const text = source.toString();
    const view = /viewBox="([^"]+)"/.exec(text)[1].split(/[, ]+/).map(Number);
    const group = stem.split('/').pop().replace(/-(?:a-detail|c-current|connections|[a-e])$/, '');
    const fullWidth = stem.includes('/framework/') ? 1015.5 : group === 'action-model' ? 1083.5 : 510;
    const width = Math.max(200, Math.round(view[2] * 2200 / fullWidth));
    const output = await sharp(source, { density: Math.max(72, 72 * width / view[2]) })
      .resize({ width }).webp({ quality: 90, alphaQuality: 100, effort: 5 }).toBuffer();
    await fs.writeFile(path.join(root, stem + '.webp'), output);
    records.push({ source: stem + '.svg', preview: stem + '.webp', sourceBytes: original.length, previewBytes: output.length });
    html = html.replaceAll(`src="${stem}.svg"`, `src="${stem}.webp"`);
  }
  html = html.replace(/(<img\b[^>]*\bsrc="assets\/figures\/[^\"]+"[^>]*)(>)/g,
    (all, tag, close) => tag.includes('decoding=') ? all : tag + ' decoding="async"' + close);
  await fs.writeFile(htmlPath, html);
  await fs.writeFile(path.join(root, 'data/figure-previews.json'), JSON.stringify(records, null, 2) + '\n');
  const before = records.reduce((s,r)=>s+r.sourceBytes,0), after = records.reduce((s,r)=>s+r.previewBytes,0);
  console.log(`${records.length} source-derived previews: ${(before/1048576).toFixed(1)} MiB → ${(after/1048576).toFixed(2)} MiB`);
})();
