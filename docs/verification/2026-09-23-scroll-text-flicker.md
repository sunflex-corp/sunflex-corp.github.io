# Scroll text flicker fix

Base: 5b357c420f2706eed320902edbdec23d633dd2df

A pending heading could become fully visible during ScrollTrigger's nested refresh/revert, then reset to opacity 0 and y 28 when entering. Fixed-value scrub timelines no longer invalidate on refresh; entrance tweens initialize eagerly with lazy:false. Geometry refresh and responsive rebuilding remain enabled. Shared-engine secondary tabs now have one opacity/transform animation owner.

## Browser evidence

Chrome, local release source, 1280 × 900:
- Before: co2-temp-humidity had 10/10 below-viewport headings incorrectly visible, both initially and after refresh.
- After: 47 shared-flow product pages, 458 pending headings, zero incorrectly visible headings initially or after refresh.
- Bodycam: 11 headings sampled after scrolling; final opacity 1 / transform none; no sampled completed-to-hidden regression.
- Bodycam desktop: 01/02/03 forward and reverse; three mounting tabs; selected panels settle and legacy CSS animation is none.
- Bodycam 390 × 844: all six tabs settle to opacity 1 / transform none; resized back to desktop.
- Standalone CCTV: 01/02/03 and return to 01 smoke tested.
- Home: brand copy completes at opacity 1 and zero translation.

The checks sample computed styles; they do not claim exhaustive frame capture on every device. Full-page screenshots alone are insufficient for this issue.

Reproduction: run `python3 scripts/serve-motion-regression.py`; open the printed loopback URL in Chrome at 1280 × 900. Do not scroll until the fixed bottom report is complete. Both checks must have pending > 0, visible = 0, and no failures. The probe is only injected on the local /__motion__/ route, not production HTML.

## Automated checks

Passed: test-site-motion.py against the base above (60 shared pages retain exact content, asset order and cache keys); test-cctv-motion-release.py; test-product-navigation.cjs; JavaScript syntax checks; Python probe compilation; git diff --check.

Existing baseline failures, verified against the base commit:
- test-home-simple.cjs lacks document.documentElement in its fixture, raising TypeError at the existing shared-engine check.
- test-product-revision.py expects the old data-story-revision marker on mobile CCTV; the previously shipped standalone redesign has no such marker.

These obsolete test assumptions are outside the flicker fix and were not represented as passes.
