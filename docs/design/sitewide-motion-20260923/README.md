# Sitewide motion rollout — 2026-09-23

## Scope

Extend the approved mobile CCTV motion direction to the remaining 60 published pages: 47 product detail pages plus the home, catalogue, solution, company, support, contact, privacy and 404 pages. With standalone CCTV, total coverage is 61 pages and all 48 products. Redirect documents are excluded.

The change preserves every existing page's content, images, links, structured data and input controls. No new assets, product claims, or manual motion toggle are added. Existing downloaded Blender renders remain intact.

## Motion ownership

- Locally hosted GSAP 3.15.0 / ScrollTrigger and Lenis 1.3.26 are reused from the approved CCTV release.
- Shared runtime owns product flow transitions. Legacy controllers remain available as fallback if vendor loading fails.
- CSS sticky positions the frame; ScrollTrigger controls child opacity, 24px entry / 14px exit and 1.035→1 image scale. Scrub smoothing is 0.6s. Tabs and arrow/Home/End keys select chapters.
- Mobile, reduced motion and insufficient viewport height use ordinary-height tabs. Hidden panels are inert and excluded from accessibility navigation; moving away from a focused panel transfers focus to its tab.
- General entrances use 28–42px movement, 0.55–1.15s duration and power3 easing. Sticky ancestors and form controls are not translated. Desktop wheel smoothing is disabled on the inquiry page.
- Home story uses ScrollTrigger instead of its previous independent animation loop. Home solution chapters keep their accessibility controller and add restrained image settling.
- OS reduced-motion preference remains honored, without a visible toggle.
- Both page generators apply an idempotent shared asset injector with content-hash URLs. Standalone CCTV remains its approved independent design.

## Acceptance and evidence

- 61 actual Chrome route checks at desktop 1078×738 and mobile 390×844: initialized runtime, no horizontal overflow, single selected flow tab where present. Mobile shared flows use tab mode. Raw records: `browser-routes.json`.
- Bodycam desktop: clicking chapter 02 settles at opacity 1 with chapters 01/03 opacity 0 and aria-hidden. Sticky frame fits the viewport.
- Bodycam mobile: pointer chapter selection, End key, and secondary magnetic-cradle tab work. One visible flow panel.
- Runtime switch to OS reduced motion preserves selected chapter and changes to tab mode. Home has no pinned story/family state and no hidden headings. Test overrides restored.
- Home family 03 selects Solar Respond; settled inactive panels are fully transparent.
- Catalogue search for 바디캠 returns one product. Contact test input stays visible and retains value; no form was submitted.
- Company section anchor reaches its target. Representative desktop and mobile views were visually inspected.
- `test-site-motion.py`: all 60 documents preserve exact source text except owned tags/root marker/known script cache keys; script order, hashes, idempotence and standalone exclusion pass.
- Existing product-flow and product-motion tests pass for the retained fallback controllers. These tests do not substitute for the new GSAP browser checks.
- Infographic release contract passes: 47 infographic pages / 141 figures, 27 context renders, plus independent CCTV release contract.

## Limits

Chrome responsive emulation is not physical-device FPS or touch-performance testing. Cross-document native View Transition cancellation messages occurred during viewport switching/rapid route navigation (`Viewport size changed`, `opt-in disabled`); no GSAP exception was observed. Existing cross-document fallback behavior is unchanged.
