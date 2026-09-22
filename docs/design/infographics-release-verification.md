# Product infographic release verification

Date: 2026-09-22
Baseline: d4e1f83d7780eb623295d0e7cef36b487b38364a

## Scope

48 existing product pages; 144 benefit visuals replaced. The surrounding product titles, descriptions, detail links, original specifications, contact links and navigation are preserved. 31 Blender renders (1600 × 900 WebP, 2,992,690 bytes combined), 5 technical SVG layouts and 108 HTML/SVG diagrams are embedded in the existing scroll controller. Each product retains its distinct accent. No draft navigation or draft application script is shipped.

## Passed checks

- `test-product-infographics.py`: all 48 pages, 144 unique scene keys, 31 referenced media files, accessible group names and image alternatives, unique IDs, valid internal anchors and ARIA controls. Canonical DOM outside the targeted graphics and new stylesheets is identical to the baseline. Encoding name case is normalized for BeautifulSoup serialization.
- `test-product-benefits.py`: all 47 standard product stories / 141 panels, responsive media and retained references.
- `test-product-revision.py`: all 48 original product stories and detail content, CMS stages and proof sources.
- `test-product-flow.cjs`: forward/reverse transitions, 3/4/5 steps, keyboard focus, reduced motion and overflow reading fallback.
- `test-product-navigation.cjs`: anchor offsets, deep-link delegation, modified links and reduced motion.
- `test-product-motion.cjs`: bounded image movement, mobile amplitude, frame batching, idle cancellation and hidden-page suspension.
- `test-product-editorial.cjs`: model selection, keyboard wrapping, comparison, deep links and short-screen fallback.
- `test-solar-site.cjs`: catalog filters, URL restore, gallery state, FAQ search and inquiry prefill.
- Both page-generation paths retain their new visual fragments (47 standard products plus the special pedestrian story).
- CSS AST inspection: all 525 selectors are scoped to the product benefit sections, with 14 named container queries for the actual graphic width.
- All 31 WebP images are 1600 × 900. Markers, connecting lines and image pixels use one aspect ratio.
- `git diff --check` passes.

## Browser evidence

Local file/localhost Browser Use was denied by the tool's URL policy. No alternate browser driver or indirect workaround was used. The checks above validate source structure and behavior, not actual browser rendering. Public post-deployment evidence is recorded separately when available.

## Release gate

Independent read-only review completed: no blocking code, DOM, asset, namespace or generator-persistence defect found. The reviewer independently reran the infographic, benefit and revision checks. Actual browser rendering remains outside that review. Production deployment verification is pending.
