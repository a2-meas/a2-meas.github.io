# Implementation handoff

Read DESIGN.md and design-contract.md first. Build a static, dependency-free English site in the existing directory; do not relocate or overwrite source media or the paper.

Use index.html, site.css, site.js, data/videos.json and assets/{figures,posters,videos}. Source scientific content from the supplied PDF. Export all five supplied figure/ PDFs to faithful SVG, retaining the original paths and embedded images. Reproduce benchmark Tables 5–8 as editable HTML with full report text and data, styled to the light orange/sage theme. Generate optimized web copies and poster images for supplied videos; keep full original files intact.

Preserve the academic reference structure with the user’s revised ivory / apricot / sage color direction, 1120px body width, centered title and descriptive figure captions. Ready task videos use 3/2/1 responsive columns, grouped by scene; the two correction clips remain independent, followed by the full coffee video. Fifteen task clips are supplied in demo/; render their actual posters and videos. Keep the three absent entryway clips and behind-the-scenes clip in a compact, truthful release state.

Expose future media additions in data/videos.json. The local server must support byte ranges for video seeking. Use relative URLs throughout so the site works below a GitHub Pages repository prefix. Include README instructions for local preview, media updates and later publication. Validate actual media decoding, navigation, dialogs, filters, clipboard fallback, reduced motion and responsive overflow before handoff.

Latest gallery state:12 curated tasks with10 ready clips. Scene-specific desktop layouts are3/2×2/1centered/2/2pending. Coffee full task and its correction appear before this task gallery. Earlier18-task inventory and correction-before-coffee ordering above are historical.
