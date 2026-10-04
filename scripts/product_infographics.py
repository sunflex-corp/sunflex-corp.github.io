"""Reviewed, self-contained benefit figures used by the existing site generator."""
import json
from pathlib import Path
from product_scene_assets import apply_benefit_scene_overrides
ROOT=Path(__file__).resolve().parents[1]
FIGURES=apply_benefit_scene_overrides(json.loads((ROOT/'data/product-infographics.json').read_text()))
def figure(slug,step):
    figures=FIGURES.get(slug)
    return figures[step] if figures else None
