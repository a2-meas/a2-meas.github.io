// Build small display copies from the original SVG artwork.
// The source SVGs remain unchanged and are used for chart enlargements.
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require('sharp');
const root = path.resolve(__dirname, '..');

(async () => {
  const figuresPath = path.join(root, 'data/figure-previews.json');
  const figures = JSON.parse(await fs.readFile(figuresPath, 'utf8'));
  for (const name of ['training-systems', 'training-throughput']) {
    const source = `assets/figures/${name}.svg`;
    const preview = `assets/figures/${name}.webp`;
    const input = await fs.readFile(path.join(root, source));
    const width = 2400;
    const viewBox = /viewBox="([^"]+)"/.exec(input.toString())[1].split(/[, ]+/).map(Number);
    const output = await sharp(input, { density: 72 * width / viewBox[2] })
      .resize({ width }).webp({ lossless: true, effort: 6 }).toBuffer();
    await fs.writeFile(path.join(root, preview), output);
    const record = { source, preview, sourceBytes: input.length, previewBytes: output.length, width };
    const index = figures.findIndex(item => item.source === source);
    if (index < 0) figures.push(record);
    else figures[index] = record;
    console.log(`${name}: ${input.length} → ${output.length} bytes (lossless WebP, ${width}px)`);
  }
  await fs.writeFile(figuresPath, JSON.stringify(figures, null, 2) + '\n');

  const logoInput = await fs.readFile(path.join(root, 'assets/logos/autolab.svg'));
  // Four physical pixels for each pixel of the largest 44px header height.
  const logo = await sharp(logoInput, { density: 144 }).resize({ height: 176 })
    .webp({ lossless: true, effort: 6 }).toBuffer();
  await fs.writeFile(path.join(root, 'assets/logos/autolab.webp'), logo);
  const sourcesPath = path.join(root, 'assets/logos/sources.json');
  const sources = JSON.parse(await fs.readFile(sourcesPath, 'utf8'));
  Object.assign(sources.find(item => item.id === 'autolab'), {
    asset: 'assets/logos/autolab.webp', original_asset: 'assets/logos/autolab.svg',
    operation: 'lossless 176px-high display raster from original cropped SVG; original retained',
    displayBytes: logo.length
  });
  await fs.writeFile(sourcesPath, JSON.stringify(sources, null, 2) + '\n');
  console.log(`AutoLab: ${logoInput.length} → ${logo.length} bytes (lossless WebP, 176px high)`);
})().catch(error => { console.error(error); process.exitCode = 1; });
