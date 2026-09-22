# Product design revision — 22 September 2026

## Scope and acceptance

48 product pages share a consistent content width, card spacing, radius hierarchy and responsive infographic frame. All 144 numbered scenes, original product facts, source detail links and keyboard navigation remain available. This revision uses existing 3D renders and targeted HTML/SVG changes; it does not add unverified product specifications.

## Review evidence

Six existing ChatGPT Pro conversations received 48 full-page Chrome captures, 12 detail sheets and code excerpts. The completed responses were recovered after refresh; transient UI errors did not indicate that the analyses had failed. Their suggestions were treated as review input and checked against the implementation and actual browser output.

The original detail sheets included cropped desktop captures. Right-edge clipping in those sheets was not accepted as evidence of a CSS defect. Fresh full browser viewports were used for final desktop review. The Pro reviews are AI feedback, not human certification or HIG conformance certification.

Local evidence directory: `deployment-evidence/visual-audit-20260922/pro-review/` in the parent workspace. Original response files 01–06, desktop-final.json, geometry.json and the verified screenshots record the review. The final pass covers 28 changed scenes at 1200px and 390px after the earlier all-page audit. Static design captures use reduced motion; normal-motion keyboard selection was verified separately on the bodycam page.

## Confirmed corrections

- Removed nested image rounding and replaced the ambiguous global tab-progress rule with an underline on the selected tab.
- Fixed Korean footnote wrapping and dark-diagram text inheriting light-page colours.
- Removed one repeated hook-camera photograph while preserving checkpoint copy.
- Clarified measurement versus speaker output, one-person radio calling, human detection and operator judgment after an alarm.
- Distinguished wearable measurement locations from notification recipients; connected helmet detail and audio output to their labels.
- Matched beacon marker and zone text; reversed warning delivery arrows; replaced the suit part diagram with two labelled motion poses.
- Expressed video range selection, location recording, lifting-information output, curing-record flow and case-to-training reuse directly.
- Removed duplicated inserted components and verified repeat-run stability of all five Pro refinement scripts.

## Verification and limits

Product contracts cover 48 pages / 144 scenes / 29 render assets. CSS cascade checks cover 432 scene-width combinations. Navigation checks cover selection, focus, reduced motion and reading fallback. Shared asset version links are regenerated from the current files.

No new image-generation asset was necessary for the confirmed defects. Existing infographic media totals about 2.95 MB across 31 unique files; this is an asset-size inventory, not a measured LCP or mobile frame-rate claim. No synced source files were changed.
