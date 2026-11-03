# A²-MEAS academic homepage

English static website for **Toward the Era of Agentic Embodied Intelligence**.
HTML, CSS and vanilla JavaScript; no npm installation, build framework, external fonts or database.
Chinese handoff and privacy/deployment instructions: [HANDOFF.md](HANDOFF.md).

## Run locally

Requires Python 3. In this folder:

```sh
python3 scripts/serve.py --port 4173
```

Open http://127.0.0.1:4173. On macOS use `Preview.command`; on Windows with Python Launcher use `Preview.bat`.
The server binds to localhost and supports byte-range video seeking. Use HTTP rather than opening
`index.html` as a local file: browsers typically block the JSON inventory under `file://`.
The three coffee fallback buttons open a closable in-page player, including in local-file mode.

## Current content

- Title and institutions on the cover; contributors grouped at the end.
- Overview, four Method diagrams, real-world demonstrations, BEHAVIOR/RoboTwin results,
  independent training-efficiency section, BibTeX and contributors.
- Coffee full-task video first, then two independent grasp-correction experiments.
- Short-horizon gallery: twelve tasks in a draggable elliptical chain, ten available videos and two pending parcel tasks.
- Available foreground previews autoplay muted. Each task opens native video controls in a closable dialog.
- Framework and Method stages advance every1.5seconds after entering the viewport.
  Method ends with all modules highlighted for10seconds. Pointer/focus activates manual selection.
- Original PDF vector figures are cropped at source; connectors remain intact. Tables are editable HTML.
- No video synchronization or global play/pause switch. Behind-the-scenes video remains unavailable.

## Edit and regenerate

| Purpose | File |
| --- | --- |
| Content, tables, authors, resource links | `index.html` |
| Appearance | `site.css` |
| Interactions | `site.js` |
| Media list and pending entries | `data/videos.json` |
| Citation | `data/citation.bib` and the matching HTML block |
| Copy provenance | `data/site-copy-notes.json`, `data/method-notes.json` |

Prepared web assets are included. No regeneration is needed for preview or deployment.
For optional figure regeneration install PyMuPDF; for video re-encoding install ffmpeg or imageio-ffmpeg.
Original PDF crops are in `figure/`, source logos in `logo/`. Full-size original videos in `demo/` and
`Tech Report/` are intentionally excluded from Git and handoff archives; keep a separate source-media backup.

```sh
python3 scripts/extract_figures.py
python3 scripts/extract_method_modules.py
python3 scripts/build_method_layout.py
python3 scripts/create_cover_ribbons.py
```

Do not regenerate media unless the original input videos are present.

## Package without publishing

```sh
python3 scripts/package_site.py
python3 scripts/package_site.py --mode handoff
```

The first command writes a minimal static deployment to `dist/`.
The second writes a runnable source handoff and ZIP in `output/handoff/`.
Packages include only video/poster files referenced by the media inventory, with SHA-256 checksums.
They exclude original video directories, temporary files, credentials and screenshots.

All runtime URLs are relative; `dist/` supports a future `https://OWNER.github.io/REPO/` deployment.
These commands do not upload, deploy, enable Pages or change repository visibility.

## Hosting account connections

The source is backed up in the private repository `laihh88/a2meas-homepage`.
Private online preview: https://a2meas-preview-laihh88.pages.dev/
Cloudflare Pages project: `a2meas-preview-laihh88`.
Access protects both the production hostname and all deployment subdomains. Visitors
must use an approved email address and a one-time PIN. The session lasts24hours.
Anonymous checks confirmed that the homepage, deployment URL, PDF and video URLs
redirect to Access login. Only the owner's supplied email is currently approved.
Add colleague emails to the `Approved project viewers` policy; no GitHub write access is needed.

For Cloudflare's25MiB asset limit, `scripts/prepare_cloudflare.py` creates a separate
hosting copy under `output/cloudflare-private/site`. It re-encodes only oversized
videos and preserves the main assets. Requires imageio-ffmpeg. The normal `dist/`
retains the original web copies for later GitHub Pages deployment.
Keep the existing Access application `A2-MEAS private preview` in place during updates.
After preparing the hosting copy, an authenticated maintainer can deploy with:

```sh
wrangler pages deploy output/cloudflare-private/site --project-name a2meas-preview-laihh88 --branch main
```

GitHub pushes do not automatically deploy the website. The hosting authentication
credentials are stored outside this repository. GitHub Pages has not been enabled.

## Private preview before publication

Keep the GitHub repository private. A private repository alone does not restrict access to ordinary
GitHub Pages websites. Use an authenticated preview host or an existing internal/VPN server.
Organization-private GitHub Pages requires a suitable Enterprise Cloud organization.
Protect direct PDF/media URLs as well as HTML. Hosting credentials stay out of source control.
See [HANDOFF.md](HANDOFF.md) for access-controlled preview and later public deployment.

Design decisions and historical changes are recorded in `DESIGN.md`, `design-contract.md` and
`implementation-handoff.md`. Some early historical entries describe superseded layouts.
