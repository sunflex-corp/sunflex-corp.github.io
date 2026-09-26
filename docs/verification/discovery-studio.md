# Catalog and support presentation verification

2026-09-26. Scope: `/products/` and `/cases/` only.

The catalog now uses a twelve-column exhibition opening and labeled, color-coded product-family controls. Support uses three unequal graphic panels, direct contact links, and a FAQ/contact layout. New SVG symbols are original decorative navigation cues. Existing product images, descriptions, URLs, support answers and business contact data are preserved. Existing GSAP/ScrollTrigger runtimes are reused; no framework or runtime dependency is added.

Reference decisions: [AXIS](https://www.axis.com/products) for catalog grouping, [Apple Support](https://support.apple.com/ko-kr) for purpose-first navigation, [Floema](https://www.cssdesignawards.com/sites/floema/49313/) for product-led editorial composition, [Gufram](https://www.awwwards.com/sites/gufram) for asymmetric product exhibition. No third-party visual assets were copied.

Validation:

- Chrome at 360, 390, 768, 1024 and 1440px: both routes have no horizontal overflow; one H1; no failed loaded images.
- Category controls work with Enter and show 17/14/7/10 products. Reset restores all 48.
- Search matches visible copy; empty state, reset and combined URL filter restoration work.
- FAQ empty-state reset restores all four questions and input focus. Native disclosure works with keyboard.
- Fresh JavaScript-disabled document retains products and native FAQ disclosure. Reduced motion disables the decorative scroll tween.
- Poster keyboard focus is visible and triggers the corresponding decorative interaction.
- Final visual review corrections: mobile product captions are 12px/18px, 36px tall, top-aligned and wrap by Korean word; support SVGs use 0.65 opacity and a stronger stroke.
- `check-site-studio.py`, `check-product-studio.py`, `test-cctv-motion-release.py`, `node --check assets/sunflex-v2/discovery-studio.js`, and `git diff --check` passed.

These checks do not constitute WCAG certification or real-device performance measurement. Telephone calls and email sending were not exercised; the existing tel/mailto behavior is preserved.
