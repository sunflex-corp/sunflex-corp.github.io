# Step-based product reading stops

Scope: 48 product pages / 75 story sections (71 three-step, 3 four-step, 1 five-step). See the adjacent inventory JSON. Model selectors, static numbered lists and the home family selector are not product story sequences.

Native scrolling holds each complete card at a stable position. Crossing a step boundary triggers a 320 ms entrance once, rather than leaving text partway through a scrubbed transition. When scrolling stops, ScrollTrigger settles to that interval's reading position (180 ms delay; 180–380 ms snap; inertia prediction disabled). First/last boundaries release into normal page scrolling. Numeric tabs and arrow/Home/End keyboard controls remain available. Native touch scroll is not canceled or intercepted.

Mobile typography/spacing and image heights fit a complete scene. Oversized text or very short viewports retain natural-height tab fallback, as does prefers-reduced-motion. The standalone CCTV story follows the same behavior and rebuilds on width changes.

## Fresh verification

- Chrome layout audit: all 74 shared sections pinned at 390×844, 360×740 and 1280×900, with the complete stage within its available height.
- Healthcare heart band: real browser scroll 01→02→03→02; settled opacity 1; third stage releases into the following section.
- SafeBridge: all four steps; concrete curing: all five steps and Home keyboard return.
- Reduced motion: one normal-flow selected panel per section, no forced pinning.
- CCTV: mobile and desktop pinning, actual scroll 01→02→03→02; 700×390 natural-flow fallback; restoration to 390×844; reduced-motion fallback.
- Previous flicker regression: all 47 shared-flow product pages pass initial and explicit refresh probes.
- Content/cache/dependency validation (60 shared pages), standalone CCTV release/rebuild validation, navigation regression and JavaScript syntax checks pass.

Browser checks use Chrome responsive viewports and native scroll actions, not a physical Android/iOS device. Extremely fast scrolling may cross more than one native-scroll interval; we do not trap or suppress the user's scrolling.
