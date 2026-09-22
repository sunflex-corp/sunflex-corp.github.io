# Product infographic integration — 2026-09-22

## Scope and sequence

1. Replace only the three benefit visuals on each of the 48 supported product pages with the reviewed HTML/SVG/Blender compositions.
2. Preserve the surrounding copy, detail anchors, original specifications, navigation, contact links and the existing scroll controller. Keep diagram CSS inside a dedicated namespace and use container-based rules for the embedded width.
3. Integrate the generated fragments with the existing page generator so rebuilding cannot silently restore the old diagrams.
4. Verify 144 panels, source language examples, local media, SVG IDs, keyboard/scroll behavior, and preservation of all content outside the visuals. Obtain an independent diff review.
5. Publish through the existing GitHub Pages master branch, wait for the build, and verify public URLs and selected desktop/mobile screens where browser policy permits.

## Acceptance

- 48 product pages × 3 distinct scene keys; no draft navigation embedded.
- All captions remain HTML and all image markers use the same 16:9 or 4:3 frame as the render.
- Every existing benefit title, description, detail link and other page section remains present.
- All styles are scoped; long content remains readable through the existing reading-mode fallback.
- Static/function checks pass and deployment status is successful.
- Report browser evidence separately: local Browser Use access was denied; source/DOM tests do not certify layout.

## Recovery

The pre-release production revision is d4e1f83d7780eb623295d0e7cef36b487b38364a. A release regression can be reverted with a new commit restoring this change's files, without force-pushing or overwriting concurrent updates.
