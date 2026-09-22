# External Blender scenes and buyer readability

The product benefit illustrations now use 27 Blender compositions in 144 placements across 48 product pages. Twenty additional detail diagrams use the same rendered context imagery with readable HTML explanations. Navigation icons, comparison tables, actual product photos and original specifications remain functional HTML and images.

## Asset policy and records

- All visible scene geometry comes from downloaded free Poly Haven or BlendKit models. No mesh, curve, text-object or icon geometry was authored for this change.
- The final saved Blender scenes contain 295 visible geometry objects; all 295 carry external-source metadata. Camera, lighting, placement, material and framing adjustments provide the presentation.
- `data/external-assets/source-register.json` records acquired sources, free status, licenses and hashes. Downloaded models and packed Blender files stay outside the published site; no credentials or signed download URLs are included.
- `data/external-assets/final-scene-records.json` was extracted from all 27 final Blender files. It records actual object transforms, light energy/size/color/rotation, camera values, exposure, world lighting, render settings and hashes.
- `data/external-render-assets.json` maps each placement to its contextual image and labels. All render images are 1800×1200 WebP; the 27 published files total approximately 1.97 MB.
- When an exact free product model was unavailable, the user approved a scene explaining its use context. These renders are not represented as the product's actual hardware. Original product photography and factual specifications are retained.

## Browser Pro review and implemented changes

Two parallel GPT Pro browser reviews evaluated submitted render images, page screenshots and numeric scene settings. Both returned requests for changes; the changes below were implemented and locally verified. This record does not claim an additional final Pro approval.

- Radio: remove the prominent third-party model identity from the viewing angle; distinguish group, individual and all-group communication with 1+3, 1+1 and 1+3 arrangements; retain an explicit SE-400 context note. Use the reviewed neutral light arrangement.
- CCTV reporting: reduce each phase to two meaningful objects. Show camera + monitor, monitor + clipboard, then clipboard + monitor. Keep the same selected scene through the first two phases and show human review in the third. Use common Key 1250 W / Fill 350 W / Rim 900 W lighting, camera position [3.4, -7.2, 3.4], target [0, 0.15, 0.35], orthographic scale 6.4.
- Separate scene selection, AI draft and manager review in the adjacent Korean copy. Keep the existing three-tab section; captions explain context rather than imply a real service screen.
- On mobile, show the headline and explanation before the render. Keep readable HTML labels and context captions. Use contained images without cropping.

## Buyer-facing improvements

- Mobile CCTV: align S/M/L model cards, communication codes, comparison table, installation explanation, post-move checklist and product-photo gallery.
- Report proof: pair the source screenshot with a readable three-step explanation instead of enlarging a low-resolution screenshot into the full section.
- Shared benefit cards: unify visual and copy columns and dark-card text colors, including wearable-product links.
- Detail explanations: replace drawn diagrams and split dense item strings into readable descriptions, including the safety dashboard, beacon zones, anemometer review, projected guidance and access gate.
- Preserve all four compact gas-detector labels: O₂, CO, CH₄ and H₂S.

## Verification

- `test-product-infographics.py`: 48 pages, 144 external figures, 27 context renders; surrounding content, anchors, controls and language examples preserved; four gas labels present.
- `test-product-revision.py`: revised pages retain primary/operating stories, original-detail access, three CMS phases and four proof sources.
- `test-infographic-cascade.py`: 432 scene/container-width checks. This is a static cascade check, not a browser layout test.
- `test-product-flow.cjs`: forward/reverse flow, dwell, different step counts, short/mobile reading fallback, focus, reduced motion and idle ARIA behavior passed; the flow controller was not changed.
- Visible Chrome inspection at 1532px and 390px checked representative shared cards, model selection/comparison, network table, report proof, gallery, post-move checklist, wearable contrast and dashboard details. No horizontal overflow was observed on checked pages. Temporary viewport overrides were reset.
- Original `data/solar-products` references are unchanged. `git diff --check` passed.

Local screenshots and the full Pro responses are kept in the project workspace's `deployment-evidence/visual-audit-20260922/` directory rather than published in this repository.
