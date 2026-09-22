# Infographic balance correction — 2026-09-22

Baseline production: a8c86235852f05712703ae20e85fa7c61a6ea455.

## Corrected defects

- The icon selector had higher specificity than the full scene selector. It forced all 16 subject-scene SVGs to 40 × 42 pixels. The icon rule now explicitly excludes large scene SVGs and uses zero-specificity matching for the SVG type.
- 19 two-card comparisons, 18 document/control layouts, seven timelines and five signal routes receive compact-width alignment rules. Unnecessary forced 400–440px diagram minimum heights are removed.
- Wind and environment scenes use actual source-supported measurement, alert and equipment-management content instead of placeholder dashes and generic status words.
- Vehicle entry and wind frames have explicit callout anchors. LED guidance distinguishes the projection unit and indicated passage.
- Four focused Blender renders use 4:3 frames with matching overlays and intrinsic image dimensions; wind uses one shared image/marker canvas to crop only empty side space.
- Five technical wearable diagrams use 13px HTML A/B/C pins instead of shrinking 12px SVG text on a 1000-unit drawing.
- The compact gas model screen shows the four source-supported gases as HTML, without fabricated readings.

## Evidence limits

Static CSS cascade checks cover 144 scenes at graphic widths of 360, 540 and 720 pixels. They resolve selector priority and relevant width queries; they are not a browser screenshot, a full CSS layout engine or a certification of visual quality. Browser access remains denied by managed policy verification. Blender image files are inspected separately.

## Per-product coverage

Every row is structurally checked; actual browser rendering remains pending.

| Product | 01 | 02 | 03 |
| --- | --- | --- | --- |
| ai-broadcast | language | dual | field-broadcast |
| mobile-cctv | Blender 16:9 | route | Blender 16:9 |
| mobile-bodycam | bodycam-view | timeline | records |
| hook-bottom-camera | Blender 4:3 | Blender 16:9 | dual |
| chatgpt-cctv | image | document | review |
| safety-box | hub | dashboard | dual |
| site-cms | Blender 16:9 | route | Blender 16:9 |
| led-logo-light | Blender 16:9 | lanes | projected-guidance |
| vehicle-entry-alert | Blender 16:9 | dual | gate-flow |
| co2-temp-humidity | metrics | threshold | chart |
| iot-mist | Blender 16:9 | Blender 16:9 | control |
| lte-anemometer | Blender 4:3 | flow | wind-readout |
| smart-environment-board | Blender 16:9 | environment-readout | environment-control |
| compact-gas-detector | Blender 4:3 | flow | chart |
| gas-alarm | Blender 16:9 | dual | threshold |
| tilt-acceleration-sensor | Blender 16:9 | flow | chart |
| fire-detection | Blender 4:3 | route | alert |
| ir3-flame-detector | Blender 4:3 | flow | compare |
| wireless-emergency-broadcast | Blender 16:9 | route | compare |
| digital-radio | group | dual | hub |
| tbm-solution | dual | Blender 16:9 | document |
| ai-equipment-collision | zone-scan | image | dual |
| opening-open-close-sensor | Blender 16:9 | Blender 16:9 | dual |
| equipment-approach-alarm | zone-scan | dual | zone-response |
| tower-crane-hook-collision | Blender 16:9 | language | crane-zone |
| emergency-signal-location | Blender 16:9 | location | alert |
| hazard-area-broadcast | hazard-boundary | document | field-layout |
| pedestrian-collision-prevention | corner-plan | corner-alert | dual |
| alcohol-detection | gate-check | flow | review |
| smart-beacon | location | dashboard | records |
| wireless-network | network-cutaway | hub | dual |
| power-assist-suit | Technical SVG + HTML | Technical SVG + HTML | review |
| smart-safety-hook | Blender 16:9 | Blender 16:9 | dual |
| smart-helmet | Blender 16:9 | Blender 16:9 | dashboard |
| smart-airbag | Technical SVG + HTML | Technical SVG + HTML | review |
| worker-attendance-card | credential | records | review |
| worker-access-gate | authentication | access-gate | records |
| healthcare-heart-band | Technical SVG + HTML | threshold | alert |
| ai-quick-risk-assessment | image | document | review |
| ai-risk-assessment-review | document | compare | review |
| ai-safety-index | hub | metrics | dashboard |
| ai-subcontractor-safety | records | timeline | document |
| ai-drone-inspection | Blender 16:9 | location | document |
| inspectcut | timeline | image | compare |
| ai-similar-accident-alert | document | records | dual |
| safebridge | education-room | language | records |
| iot-small-tower-crane | Blender 16:9 | Blender 16:9 | dual |
| concrete-curing | Blender 16:9 | chart | review |

## Independent persona review

Claude Code 2.1.259, exact model `claude-sonnet-5`, effort `high`, read-only tools. The review packet includes all 48 product compositions, 31 render assets, site-wide HTML inventory (116 files), and 27 additional diagram candidates. The completed review covered every product and render. Its P0/P1 findings were individually checked; the correction disposition below records the implementation and evidence limits.

## Review disposition

- Blank displays: compact-gas uses source-supported O₂/CO/CH₄/H₂S HTML symbols, TBM uses a readable HTML training-content panel, gas-alarm uses Blender sensing/warning symbols. No invented readings or performance figures.
- Missing numbered connections: eight scenes now have manually reviewed object anchors, two numbered pins and matching captions. Every one of the 31 Blender scenes has matching pin/caption counts.
- Semantic icons: CO₂/temperature/humidity, dust/noise/vibration and environment/attendance/CCTV are distinct. All 19 comparison pairs have product-specific icons; driver and pedestrian use different shapes.
- Incorrect shared hub text: wireless AP uses mesh-network connection language; safety-index uses data integration language.
- Consecutive AI scenes: 02 remains a report draft; 03 is a separate three-step review chain. Quick risk assessment now includes the source's risk-level field.
- Duplicated fire alert label and repeated bodycam record icons were corrected. False link arrows were already hidden by CSS and are now removed from the markup too.
- Wind's camera icon was replaced with a wind symbol. The hook monitor uses a purpose-built landing/load view.
- CMS's three informative process images now have descriptions and captions, retained by the apply script after a rebuild.
- Reported duplicate diagrams in wind/bodycam/gate were checked against complete DOM: wind/gate are nested parent/child selections, while bodycam has two different diagrams. They were not duplicate rendered copies, so no content was deleted.
- Optional low-confidence installation context observations (LED mount, vehicle gate posts) remain concept illustrations. Existing captions already distinguish them from actual installation drawings. The adjacent equipment-warning summary remains a concise two-target text diagram; the three main scenes supply its detailed illustrations.

## Verification

- 48 products / 144 scenes / 31 referenced render images; actual intrinsic dimensions and matching callouts verified.
- 432 static cascade cases at graphic widths 360/540/720, including all 16 previously collapsed SVG scenes.
- Benefits, source revision, scrolling, navigation, motion, editorial interaction and site behavior regression checks passed.
- Original surrounding content is preserved, with an explicit narrow exception and exact assertion for the three CMS descriptive additions.
- Final assets are inspected as image files. Browser-rendered spacing, clipping and device screenshots are still unverified because browser access is denied by the managed policy check. No browser QA pass is claimed.

Editable Blender corrections are retained in the working design directory as four `*-focused.blend` and two `*-detailed.blend` files; originals are preserved. The production repository ships the rendered assets and HTML/CSS.
