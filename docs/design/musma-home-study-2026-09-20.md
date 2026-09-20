# MUSMA reference study and SUNPLEX homepage simplification

Reference: https://musma.net/ (user-corrected domain). Inspected in visible Chrome from hero through footer, including the intermediate pinned-scroll states, upward-scroll header return, hardware category switching and detailed descriptions. Public HTML and the page bundle were read to distinguish final layouts from transitional states. No MUSMA assets or source code were incorporated.

## Observed structure

| Order | Reference section | Design / interaction observation |
|---|---|---|
| 1 | Hero | Full viewport video, transparent overlaid navigation, large left-aligned sentence, short supporting line, downward cue. |
| 2 | Business | Two business directions, orange/blue distinction, centered introduction, generous space and staged entry. |
| 3 | Safety brand | Large brand lettering becomes an image mask, expands into a full scene, then reveals brief copy and one detail link. |
| 4 | DX | Light title interlude into image-led content; category selection changes the description. |
| 5 | Hardware | Dark section, primary category and secondary device selectors; image beside a description and application tags. |
| 6 | Performance | Four large numerical facts with short labels on a subtle technical background. |
| 7 | Clients | A restrained horizontal logo strip. |
| 8 | News | Three image-led cards, date/source, short text and one detail action. |
| 9 | Contact / footer | One centered inquiry action, followed by a compact company/navigation footer on a contrasting light surface. |

The header is transparent at the top, disappears when scrolling down and returns with a dark translucent background when scrolling up. Inspection confirmed long pinned sequences on the reference (several viewport heights), rather than many independent content blocks.

## SUNPLEX adaptation

The homepage now has four main sections instead of seven. Main text fell from 1,736 to 641 characters as measured with BeautifulSoup `get_text(' ', strip=True)`; this includes nonvisual slide descriptions and the word in the reveal mask.

1. Full viewport existing three-image sequence, concise headline and a single Solar link. One-row transparent header replaces the two-row home header.
2. Four selectable Solar families in one region. An original SVG Solar word mask expands to reveal an existing SUNPLEX scene once; selections change the image, description and product-family link.
3. Three representative products and an all-products link.
4. One inquiry section, secondary company/support links and a quieter footer.

Long installation guidance, repeated industry introductions and resource lists now remain on their dedicated pages. No numerical performance claims, client logos or news were invented to mimic MUSMA. Existing image assets and the SUNPLEX design palette remain in use. A short reveal inside the Solar image replaces long pinned scroll sequences, keeping the page compact.

## Scope and verification

Home-only CSS and JavaScript keep all 65 non-home HTML pages byte-for-byte unchanged. Carousel controls, pause, keyboard interaction, reduced motion and no-JS fallback remain. The header stays visible during keyboard focus and while the mobile menu is open. The photo is visible without JavaScript and the mask is disabled for reduced motion.

Checks: 66-route static validation; product source preservation; carousel tests including a homepage without the old diagram pause button; header direction/focus/menu tests; reveal completion, manual override and reduced-motion tests. Visible Chrome: transparent desktop hero, downward hide/upward return, Record photo/copy switch, 320px and 390px mobile with no horizontal overflow or broken loaded images, mobile menu and Alert selection. Publication is verified separately against the matching GitHub Pages commit.
