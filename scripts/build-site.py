#!/usr/bin/env python3
"""Canonical build. Preserve equivalent serialization to keep reviews focused."""
from pathlib import Path
import subprocess,sys
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
pages=[ROOT/'index.html',ROOT/'404.html']+[p for d in ['company','cases','contact','privacy','products','solutions'] for p in (ROOT/d).rglob('index.html')]
before={p:p.read_text() for p in pages}
subprocess.run([sys.executable,str(ROOT/'scripts/generate-solar-site.py')],cwd=ROOT,check=True)
for p,original in before.items():
    current=p.read_text()
    if current != original and BeautifulSoup(current,'html.parser').prettify()==BeautifulSoup(original,'html.parser').prettify():
        p.write_text(original)
print('Build complete; run python3 scripts/check-site-studio.py for published content and route checks.')
