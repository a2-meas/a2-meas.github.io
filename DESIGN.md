# A²-MEAS project page

## 1. Visual Theme & Atmosphere
An English academic project page whose layout is led by the user’s ABot reference. Per the user’s latest direction: an ivory background, centered research title, soft apricot and sage-green moving ribbons, restrained translucent controls, and long-form scientific sections. The original paper and real experiments supply the imagery.

## 2. Color
Background #f7f8f3; secondary surface #ffffff; primary text #263c35; secondary text #5e7066; quiet borders rgba(49,76,53,.17); orange accent #aa572f; pale apricot and sage-green decorative ribbons. Preserve original colors inside paper figures on light panels. Use orange sparingly for emphasis and recovery annotations.

## 3. Typography
Use system sans-serif fonts without a network font dependency. Desktop title up to 64px, weight 500, line-height 1.18 and tracking -0.025em; section titles up to56px; section introductions20px / 1.75. A²-MEAS appears within the heading, followed by a colon, at the same size and weight as the paper title. The full heading uses a static copper–olive–forest–teal text gradient, with plain-text and forced-colors fallbacks. This follows the title hierarchy observed on LDA and OpenVLA. Scientific names use A²-MEAS and A²-WLA consistently. Mobile title 32–44px, body 16px. Separate components within institutional affiliations with English commas. Author superscript colors consistently identify AutoLab 1 (green), Anyverse 2 (orange), core contributor * (muted plum), project leader † (muted gold) and the corresponding-author envelope (slate blue), repeated in the affiliation and contribution labels.

## 4. Spacing & Grid
Content maximum width1200px, introduction maximum width920px. Desktop side gutters 48px, mobile 20px. Sections use 96–120px vertical spacing. Ready A²-WLA demonstrations use a three-column grid, then two columns on tablets and one on phones. Correction is two columns on desktop; coffee is full-width.

## 5. Layout & Composition
Order: title, author list, corresponding-author note, affiliations and paper links; overview and framework figure; method and action-model figure; grouped real-world tasks; two correction demonstrations; full coffee sequence; results; citation. Contributor roles are marked in the hero author block only. A light orange-and-green animated ribbon composition replaces ABot’s third-party dynamic background. It is decorative, never a substitute for experimental evidence. No main promotional video is currently available.

## 6. Components
Compact in-page navigation; rectangular translucent resource links; SVG figures faithfully exported from the five supplied figure/ PDFs, with captions and click-to-enlarge dialogs; native video players with custom poster overlays and real durations; accessible scene filters; complete editable HTML benchmark tables with pale sage headers, restrained rules and apricot numeric emphasis; contributor lists; copyable BibTeX. No nonfunctional resource links. Unavailable videos have an honest compact release state instead of fabricated thumbnails.

## 7. Motion & Interaction
Animate only large composited ribbon transforms, slowly. Honor prefers-reduced-motion, and provide a background-motion toggle. No autoplay audio or eager loading of every video. Videos load on explicit playback; pause other videos when one starts. Dialogs use native focus handling. Smooth anchor scrolling is disabled for reduced motion.

## 8. Voice & Brand
Use the supplied technical report's exact title, affiliations and contributor roles. Copy is concise, evidence-based and in English. Cite figure/table/page provenance in relevant captions. Distinguish the full correction interface from the real-robot history-conditioned Adapter. Keep provisional tabletop results qualified and public-set results labeled.

## 9. Anti-patterns
Do not invent results, author order, missing videos, model links, conference acceptance, or publication dates. No borrowed ABot logos, images, paper text or Spline scene. No purple glow, stock photography, oversized feature-card wall, fake video playback, or animated backgrounds behind body text. Do not show calculated recovery estimates as measured trials.

Hero information scale: desktop author names 20px, superscripts 15px with weight-700 colored symbols, legend 13px and affiliations 16px. Mobile names 16px, superscripts 12px, legend 12px and affiliations 13px. Keep all names intact and allow wrapping with enough vertical space.

Hero background bounds: the ambient orange/sage layer expands to 1320px on desktop, wider than the 1080px author list and 1160px centered content. Its height follows the hero. Avoid returning to a fixed 900px desktop background after increasing text size.

Report figure captions: Figures 12, 8 and 9 embed artwork-only SVGs cropped from original PDF coordinates, retaining original paths, photographs, legends and labels. Explanations are selectable HTML figcaptions with title, panel text and a restrained protocol note; expanded views repeat the HTML below the image. No screenshot assets or additional PDF entry links.

Evaluation hierarchy: one BEHAVIOR subsection holds Tables 5–7; one RoboTwin 2.0 subsection holds Table 8; Training efficiency holds Figures 8/9. Native jump links beneath the shared results title use the existing orange/sage control style, minimum 44px height, visible focus and an active-location indicator. Keep all tables visible and preserve complete original captions/data.

Project leaders Chao Liang and Zhipeng Zhang carry a muted-gold † superscript, distinct from the existing affiliation, core-contributor and corresponding-author symbols, with a matching Project leader legend.

Corresponding-author marker: a small blue-gray envelope SVG beside Zhipeng Zhang links to mailto:zhipengzhang@sjtu.edu.cn. The role legend repeats the envelope; the icon link has an accessible email label, a 24px minimum hit area and visible keyboard focus.

Institution logo placement: original AutoLab and Anyverse Dynamics SVGs appear only in the hero, below affiliations and before the introduction/resource buttons. Center the row with a44px desktop/28px mobile gap. Preserve intrinsic aspect ratios and original colors; AutoLab height78px desktop/64px mobile, Anyverse62px/52px. No footer or body-section repetitions.

Latest logo placement supersedes the previous hero placement: the header’s upper-left brand group contains the A²-MEAS wordmark followed by the original AutoLab and Anyverse SVGs. A subtle vertical separator distinguishes institutions from project identity. Use compact proportional logos (44px/34px desktop,38px/28px phone). Mobile brand row sits above navigation controls; compact Sections navigation starts at1100px.

Latest caption direction supersedes report-length captions: display no Table/Figure numbering. Each table panel has a short title and a concise14px evaluation-metadata row, outside its horizontal-scrolling area. Preserve original cells and row/column structure. Figure captions use an18px title beside a single15px summary on desktop, stacked17px/14px on mobile. Expanded views use the toolbar title once and only the brief summary underneath. Preserve material measured/calculated and independent-configuration qualifications without fine-print paragraphs.

Contact interaction: the envelope next to Zhipeng Zhang is the sole Copy email button, with a44px hit area, keyboard focus and inline live feedback. No contact dialog, mailto action or duplicate lower author section. If clipboard access is blocked, show and select the full address for manual copying.

Copy-success feedback is a compact Email copied bubble above the envelope, dismissed after1.8seconds. It never prints the email address on success or changes the hero layout.

Section scale: Method, A²-WLA, Real World, Correction and Coffee use stronger typography:14px section labels,56px section headings,18px model labels,36px model heading and20px introductions on desktop;38px headings/17px introductions on phones. Method explanations and video group/caption text scale with this hierarchy. The complete brand/navigation bar is fixed at top on all viewports, with an ivory94% background and subtle blur. Native anchors reserve112px desktop/144px mobile space so content clears the header.

Latest hierarchy supersedes the prior centered Method stack: use METHOD28px desktop/24px phone, then one concise section heading and four aligned numbered blocks (A²-WLA action model, Grounded correction interface, Correction supervision, Execution and recovery). Each uses one36px desktop/28px phone heading with its original full-width diagram. Avoid separate marketing taglines and duplicate figure labels. All orange category labels are doubled to28/24px and use concise navigation names. Original result/recovery figures retain only a short title below; remove the three protocol-summary paragraphs and the coffee full-sequence/duration caption line. Expanded figure dialogs have no empty description block.

Real-world hierarchy supersedes the three parallel demo sections. One Real-World Manipulation section uses report section5.4 headings: Short-Horizon Tasks, then Long-Horizon Pour-Over Coffee Preparation. Coffee contains the full task and nested Grasp Correction and Step Completion videos/figure. Use three quick jumps under the shared heading, matching result-jump controls. Header uses one Real-World Demos entry, plus Overview, Method and Results. Remove invented demo taglines and redundant caption/scene prose. Scene headings areh4 and task cards h5; correction cards h5 under its h4. Citation names use the screenshot's Given Family spelling and order, joined by BibTeX and.

Latest user-selected real-world ordering: coffee full task first, coffee grasp correction immediately after it, then short-horizon A²-WLA tasks. Match the quick-jump order. The correction subsection remains nested under coffee rather than becoming a parallel experiment setting.

Latest curated task inventory supersedes18-task/15-video gallery notes: display12 selected tasks,10 available clips, scene counts3/4/1/2/2. Remove study supplies, jewelry, plug insertion, container–lid matching, meatball transfer and label attachment from the display manifest. Use count-aware symmetric grids: Study3across, Bedroom2×2, Living room centered maximum700px, Kitchen2across; Entryway2equal pending tiles. Scene headings and task captions are centered; phones stack cards. Coffee-first order and benchmarks remain unchanged.

Overview stages are now three equal interactive cards. Default stage01 uses warm ivory/apricot with a copper border; the other two use darker sage surfaces. Pointer enter highlights that card exclusively; focus and touch/click provide equivalent selection. Leaving the group restores the focused card or the first default, and focus leaving the group follows the pointer or resets to the first. Native buttons expose pressed state, titles and descriptions; no content changes or layout movement. Desktop3columns; phones stack. Reduced-motion preference disables color/shadow transitions.

Short-horizon filmstrip (2026-11-02): supersedes scene grids/filter controls. Single viewport-wide horizontal row;320–360px desktop tiles,82vw phone tiles,18/14px gaps. Original16:9 videos remain uncropped, compact15/14px task captions below. Native horizontal overflow with proximity snapping,44px centered previous/pause/next controls and endpoint states; no automatic slide advancement. Default muted looping playback for visible clips only; offscreen/tab-hidden pause, per-clip pause, global pause, reduced-motion paused default.12 curated tasks remain in manifest order including2 pending tiles.

Elliptical chain revision (2026-11-02): supersedes the horizontal filmstrip. Near arc six full-opacity previews, far arc six scaled/blurred posters, thin sage ellipse; one phase drives all transforms. Desktop stage530px/phone430px, responsive original16:9 cards, no automatic rotation. Two44px wraparound arrows; pointer drag/horizontal wheel/keyboard navigation. Independent video dialog reuses each video node, native media controls plus individual toggle; no global pause action. Hero now leads into a large quiet research-question section based on PDFintroductionp1/p3, with teal emphasis ongoal-directedbehavior.

Center emphasis revision (2026-11-02): foreground scale now peaks continuously at1.40 in the near-arc center, decreasing smoothly to about0.72 at the edges. Ring stage560pxdesktop/470pxphone prevents enlarged captions clipping. Add one15px click-to-enlarge hint. Remove modal duplicated Play/Pause footer; only native video controls remain during successful playback, with hidden error-only retry feedback. Question wording retains sustain after the user’s correction.

Method heading alignment (2026-11-02): use centered section heading, max1060pxh2 with auto inline margins. This matches Overview while preserving the four left-aligned method stages.

Idle principle rotation (2026-11-02): keep original three equal cards and color surfaces. Cycle the active card every2seconds while visible/idle; mouse/pen hover or keyboard focus-visible pauses, leaving restarts2second dwell from current card. Offscreen/hidden/reduced-motion suppress timers. Do not add motion to geometry or repeated live announcements.

Section hierarchy (2026-11-02): Evaluation contains only BEHAVIOR and RoboTwin. Training efficiency follows as an independent section with centered INFRASTRUCTURE kicker/h2 and original efficiency figures; include Efficiency in both fixed-header navigation menus.

Header simplification (2026-11-02): remove background pause icon and its grid column. Keep brand left/navigation right on desktop, brand row/right-aligned Sections below on phones, with existing fixed-header height and anchor offsets.

Credits relocation (2026-11-02): remove hero author list/role markers; retain title and institutional lines without orphan affiliation indices. Restore final Authors & contributions after BibTeX with the reference’s centered heading, four ruled label/value rows and centered institutional footer. Stack rows on phone. Move the single email-copy control/tooltip to the corresponding-author row.

Logo/figure/text polish (2026-11-02): institution logo order SJTU→AutoLab→Anyverse; preserve original artwork in cropped SVG viewports. Tighten all8original-PDF figure edges with3pt safety and16pxdesktop/12pxphone frame padding. All4method figures now have concise paper-grounded English explanations; phone explanation spans full text width below number/title. Sources in data/method-notes.json and both SVG sources.json manifests.

Latest bounded revision (2026-11-04): cover autoplays once and retains its last frame; visibility changes must not restart an ended film. Meet A²-MEAS uses 22px desktop / 20px phone type and a compact 40px / 32px gap to the research question. The introduction opens with “What embodied systems co-evolve with foundation models?” and answers directly with grounded A²-MEAS control/recovery copy; the Introducing heading was removed at the user’s latest request. The three orange System/Model/Infra labels now carry the user-supplied full claims, with normal tracking and responsive wrapping; existing navigation names, section h2s, palette and paper artwork remain.

Introduction alignment refinement (2026-11-04): center the research question and answer on the same axis. Desktop question uses two explicit lines; phones use balanced natural wrapping. Answer text has an 800px maximum measure and 22px type (19px on phones). Emphasize only the A²-MEAS name. The user subsequently removed the supporting paragraph beginning “A compact action policy”; retain only the A²-MEAS connects… answer.

After removing the introduction support paragraph, use 20px desktop / 18px mobile question-to-answer spacing. Introduction bottom padding is 32px / 24px, and the immediately following System section has 36px top padding, yielding an approximately 69px / 61px answer-to-claim gap.

Latest content override (2026-11-04): retain only the centered research question; remove the A²-MEAS connects… answer and its unused container/styles. Orange section claims explicitly start with SYSTEM:, MODEL:, and INFRASTRUCTURE: followed by the user-supplied descriptions.

Spacing override: question-to-System claim spacing is now 120px desktop / 88px mobile. Remove the divider only between the research-question section and the immediately following System section.

Infrastructure hierarchy: retain the orange throughput result; the dark h2 reads “From data loading to distributed optimization” to explain the scope of the training optimizations without repeating infrastructure.

Latest local-only revision: Meet A²-MEAS ↓ sits below the centered research question and links to #system. Keep 24px desktop /20px mobile question-to-Meet spacing, followed by 56px /52px to the System claim. No divider. User explicitly requested review before any further upload; this Meet relocation remains local.

Local refinement: hero affiliation text is22px desktop /17px phone. Place Meet48px /40px below the research question and32px before the System claim, keeping overall section height stable. Still local-only pending user review.

Local infrastructure emphasis: use π with semantic subscript0.5; increase only4× to1.55em and use #557b49, a darker text tone in the method panel’s sage-green family. Preserve Throughput (the user withdrew the Throughout correction). Remains local-only.

Renewed diagrams: extract original Form XObjects from renewed report pp4/16 with scripts/extract_renewed_diagrams.py, then rebuild Framework, action-model-only modules/layout, and source-derived WebP previews. Preserve exact source geometry, original links/labels and the existing color/highlight/hover/zoom behavior. Originals and source report remain untouched. Local-only pending user review.
