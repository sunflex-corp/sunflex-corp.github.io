#!/usr/bin/env python3
"""Compatibility entry point: the approved full-site redesign replaces the old protected-page scope."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('check-solar-site.py')),run_name='__main__')
