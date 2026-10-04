"""Apply D quality images only to their named section, preserving all other markup."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]

def apply_quality_d(text,slug):
    records=json.loads((ROOT/'data/product-scene-overrides.json').read_text())
    for key,record in records.items():
        if not re.fullmatch(re.escape(slug)+r'-d-[1-6]-20261004',key):
            continue
        section=re.search(r'<section\b[^>]*\bid="'+re.escape(record['section'])+r'"[^>]*>.*?</section>',text,re.S)
        if not section and record['section']=='top':
            # Source-based generation identifies the hero before the top anchor is added.
            section=re.search(r'<section\b[^>]*\bdata-product-hero(?:="[^"]*")?[^>]*>.*?</section>',text,re.S)
        if not section:
            raise ValueError(f'Missing D section: {slug}/{record["section"]}')
        source_stem=record['reference'].rsplit('-',1)[0]+'-'
        target_stem=record['asset'].rsplit('-',1)[0]+'-'
        variants=record['variants']
        def picture(match):
            content=match[0]
            if source_stem not in content and target_stem not in content:
                return content
            def tag(m):
                value=m[0]
                avif='type="image/avif"' in value
                ext='avif' if avif else 'webp'
                choices=sorted([v for v in variants if v['format']==ext],key=lambda v:v['width'])
                if not choices:raise ValueError(f'No {ext} for {key}')
                attrs={'srcset':', '.join(f'{v["asset"]} {v["width"]}w' for v in choices)}
                if value.startswith('<img'):
                    attrs.update(src=record['asset'],width=str(record['width']),height=str(record['height']))
                return re.sub(r'(?<![\w:-])(src|srcset|width|height)="([^"]*)"',lambda a:f'{a[1]}="{attrs[a[1]]}"' if a[1] in attrs else a[0],value)
            return re.sub(r'<(?:source|img)\b[^>]*>',tag,content)
        region=re.sub(r'<picture\b[^>]*>.*?</picture>',picture,section[0],flags=re.S)
        text=text[:section.start()]+region+text[section.end():]
    return text

if __name__=='__main__':
    records=json.loads((ROOT/'data/product-scene-overrides.json').read_text())
    slugs={key.rsplit('-d-',1)[0] for key in records if re.search(r'-d-[1-6]-20261004$',key)}
    for slug in sorted(slugs):
        path=ROOT/f'products/{slug}/index.html'
        old=path.read_text();new=apply_quality_d(old,slug)
        if new!=old:path.write_text(new);print(f'Updated D image: {slug}')
