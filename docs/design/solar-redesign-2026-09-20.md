# SUNPLEX Solar full-site redesign

## Scope and acceptance

Approved scope: rename the solution family MOVING to Solar and apply a coherent, interactive design to the entire public website. Preserve all 48 product identities, model codes, specifications, diagrams and existing public paths. Company spelling remains SUNPLEX. The existing model name 무빙캠 S/M/L remains unchanged.

The site contains 61 content pages and 5 legacy redirects. Every route uses the same dark palette, Asta Sans type, blue accent, header, footer, spacing, focus treatment and reduced-motion policy.

## Reference research

- Moxion Power, REJOUICE: https://www.awwwards.com/sites/moxion-power (Site of the Day, September 19, 2023). Its official linked archive at https://moxion-preprod.rejouice.io/ was visually inspected. Large industrial imagery, direct product navigation, and restrained copy inform the product/industry structure.
- Lusion v3: CSS Design Awards Website of the Year 2023. Official results also list Moxion Power in the top ten: https://www.cssdesignawards.com/blog/2023-website-of-the-year-winners/394/. Adopt clear motion feedback and large type without heavy WebGL dependencies.
- Zero Tech: https://lusion.co/projects/zero_tech/ documents its interactive technical storytelling and links FWA/Awwwards SOTD recognition. Adopt the idea of a selectable technical diagram, using SUNPLEX's own four functional families and original SVG.

No reference imagery, brand assets, code or proprietary 3D assets were copied.

## Information and interaction

- Solar Detect / 감지 (17), Alert / 경보 (14), Respond / 대응 (7), Record / 기록 (10).
- Product list: requested Korean copy, search and category/function/install/connectivity/process filters, URL state, empty state and reset. Without JS all 48 products remain available.
- Product detail: gallery, sticky section navigation, preserved full source content, related products and a product-prefilled inquiry link.
- Solutions: four families first, followed by existing industry anchors. Family pages combine scene-based introductions with actual product collections.
- Home: existing three-image cinematic carousel plus four selectable Solar diagram states. Pause and reduced motion supported.
- Company/support/contact/privacy: common chapter navigation; support question search; contact preparation steps and product prefill. Contact remains an email draft helper, with no server submission and no claim that an email was sent.
- All pages: keyboard disclosure navigation, section reveal, scroll progress, back-to-top, visible focus and reduced motion. Content is not hidden while awaiting animation.

## Build and maintenance

Run from the repository root:

```sh
python3 scripts/generate-solar-site.py
python3 scripts/check-solar-site.py
node scripts/test-solar-site.cjs
node scripts/test-home-motion.cjs
node scripts/test-sunflex-v2.cjs
```

Python requires BeautifulSoup 4. `generate-sunflex-v2.py` provides corporate templates; the full-site entry point is `generate-solar-site.py`. Do not use legacy menu rebuilding scripts to regenerate the redesigned site.

`data/solar-products/` contains extracted semantic product content. `data/solar-catalog.json` contains taxonomy, facets and gallery metadata. `solar-source-manifest.json` records hashes from baseline b71218a. The release checker compares every original story text node with the migrated sources, then confirms that all text and images remain in generated detail pages. The one-time extractor must not be run during routine content updates.

The old protected-page checker has been replaced by a compatibility entry point to the full-site checker because product redesign is now explicitly authorized.

## Local verification

- All 66 routes: unique IDs, one H1, Korean language, shared CSS, no retired public family labels, valid internal links/anchors/src/srcset and image alt attributes.
- 48 products: original text, model codes, numbers, specification text and images preserved; product-specific contact links present.
- All 66 pages regenerate deterministically.
- Behavior tests: combined filters, empty/reset, deep links/legacy category aliases, history restore, gallery state, Escape focus, FAQ search and inquiry prefill; existing carousel/email-draft tests pass with the fourth Solar state added.
- Visible Chrome verification: 1200px product list; Record filter produces 10 products, combined 위험성평가 search produces 2; product image switching and specification anchors; 390px product detail shows no horizontal overflow or broken loaded images; product inquiry prefill verified without sending email.

## Release

Deployment evidence is recorded after GitHub Pages publishes the matching commit. Existing unrelated untracked planning documents are excluded from this release.
