"""Preserve the 2026-10-04 B replacements in the affected product pages.

Only media attributes inside the named later sections change. Earlier images,
copy, classes and source MIME types remain intact. Inspectcut is intentionally
absent because its earlier benefit image no longer repeats the editing desk.
"""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEMENTS = {
    'safebridge': {
        'safebridge-training-timeline': {
            'img/3d/office-training-briefing': (1, 2,),
        },
    },
    'safety-box': {
        'control-screen': {
            'img/3d/office-integrated-review': (1,),
        },
    },
    'smart-beacon': {
        'beacon-flow': {
            'img/3d/construction-site-entry-warning': (1,),
        },
    },
    'tilt-acceleration-sensor': {
        'tilt-decision-record': {
            'img/3d/context-record-review': (1, 2,),
        },
    },
    'tower-crane-hook-collision': {
        'detail-4': {
            'img/3d/construction-tower-crane-operation': (1,),
        },
    },
    'wireless-emergency-broadcast': {
        'broadcast-reach-line': {
            'img/3d/context-broadcast-planning': (1, 2,),
        },
    },
    'wireless-network': {
        'network-signal-path': {
            'img/3d/context-network-connection': (1,),
        },
    },
    'worker-access-gate': {
        'access-gate-rhythm': {
            'img/3d/construction-site-entry-warning': (1,),
        },
    },
    'worker-attendance-card': {
        'attendance-card-flow': {
            'img/3d/construction-site-entry-warning': (1,),
        },
    },
    'concrete-curing': {
        'curing-rail': {
            'img/3d/industrial-concrete-record': (1, 3),
            'img/3d/context-record-review': (2, 4),
        },
    },
    'healthcare-heart-band': {
        'band-functions': {
            'media/product-scenes/healthcare-heart-band-wearing-20260923': (1,),
        },
    },
    'hook-bottom-camera': {
        'highlights': {'img/pd/hookfit-3d-01': (1,)},
        'hook-checkpoints': {'img/pd/hookcp-3d-01': (1,)},
    },
    'iot-mist': {
        'dust-gate': {'img/3d/industrial-pipe-inspection': (1,)},
    },
    'led-logo-light': {
        'night-route-plan': {'img/3d/context-site-lighting': (1,)},
    },
    'lte-anemometer': {
        'vertical-wind-section': {'img/3d/construction-tower-crane-operation': (1,)},
    },
    'mobile-bodycam': {
        'bodycam-film': {'media/derived/product-mobile-bodycam-problem': (1,)},
    },
}


def apply_repeated_scenes_b(text, slug):
    if slug not in PLACEMENTS:
        return text
    records = json.loads((ROOT / 'data/product-scene-overrides.json').read_text())
    for section_id, families in PLACEMENTS[slug].items():
        section = re.search(r'<section\b[^>]*\bid="' + re.escape(section_id)
                            + r'"[^>]*>.*?</section>', text, re.S)
        if not section:
            continue
        scenes = {
            n: records[f'{slug}-{section_id}-{n}-20261004']
            for numbers in families.values() for n in numbers
        }
        stems = {n: re.sub(r'-\d+\.webp$', '', scene['asset'])
                 for n, scene in scenes.items()}
        aliases = {}
        for old, numbers in families.items():
            aliases['/' + old] = numbers
            if old.startswith('img/3d/'):
                aliases['/media/external-renders/' + old.rsplit('/', 1)[1]] = numbers
        occurrence = {old: 0 for old in aliases}

        def replace_tag(match):
            tag = match[0]
            # Recognize an already reviewed asset by identity, independently of
            # how many legacy images are still present in this section.
            number = next((n for n, stem in stems.items() if stem in tag), None)
            old = next((stem for stem in aliases if stem in tag), None)
            if number is None:
                if old is None:
                    return tag
                numbers = aliases[old]
                number = numbers[min(occurrence[old], len(numbers) - 1)]
            scene, new_stem = scenes[number], stems[number]

            def replace_url(match_url):
                url = match_url[0]
                if not any(stem in url for stem in (*aliases, *stems.values())):
                    return url
                size = re.search(r'-(480|640|768|1280|1536|1600|1920|2560)\.(webp|avif)(?:\?[^\s,]*)?$', url)
                if size:
                    width, ext = size[1], size[2]
                else:
                    width, ext = str(scene['width']), 'webp'
                return f'{new_stem}-{width}.{ext}'

            def replace_attr(attr):
                name, value = attr[1], attr[2]
                if name in ('src', 'href', 'xlink:href', 'srcset'):
                    value = re.sub(r'/[^\s,\"]+', replace_url, value)
                elif name == 'alt':
                    value = escape(scene['alt'], quote=True)
                else:
                    value = str(scene[name])
                return f'{name}="{value}"'

            result = re.sub(r'(?<![\w:-])(srcset|src|xlink:href|href|alt|width|height)="([^"]*)"',
                            replace_attr, tag)
            # All <source>s in a picture share the following <img>'s scene.
            if old and re.match(r'<(?:img|image)\b', tag):
                occurrence[old] += 1
            return result

        region = re.sub(r'<(?:source|img|image)\b[^>]*>', replace_tag, section[0])
        text = text[:section.start()] + region + text[section.end():]
    return text


if __name__ == '__main__':
    for slug in PLACEMENTS:
        path = ROOT / 'products' / slug / 'index.html'
        before = path.read_text()
        after = apply_repeated_scenes_b(before, slug)
        if after != before:
            path.write_text(after)
            print(f'Updated later sections: {slug}')
