#!/usr/bin/env python3
"""Build a local, dependency-free gallery for every raster/vector image in the clean bundle."""
from pathlib import Path
from html import escape
from urllib.parse import quote
from os.path import relpath

ROOT = Path(__file__).resolve().parents[2]
# ``01_FIGURES/final`` contains the deliverable figure assets; the gallery is
# only a browser index and is kept beside them under ``01_FIGURES/gallery``.
PRESENTATION = ROOT / "01_FIGURES" / "final"
OUT = ROOT / "01_FIGURES" / "gallery" / "index.html"
EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif"}
SKIP_PARTS = {"gallery", "regenerated_output"}


def image_files():
    files = []
    for path in PRESENTATION.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        if any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files, key=lambda p: str(p.relative_to(ROOT)).lower())


def main():
    OUT.parent.mkdir(exist_ok=True)
    cards = []
    for path in image_files():
        href = quote(relpath(path, OUT.parent))
        label = path.stem.replace("_", " ")
        source = path.relative_to(ROOT).as_posix()
        cards.append(f'''<article class="card" data-search="{escape((label+' '+source).lower())}">
  <a class="thumb" href="{href}" target="_blank"><img src="{href}" loading="lazy" alt="{escape(label)}"></a>
  <h2>{escape(path.name)}</h2>
  <p>{escape(source)}</p>
  <a href="{href}" target="_blank">Open full resolution</a>
</article>''')
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Ria Formosa — scientific bundle image gallery</title><style>
body{{font-family:Arial,sans-serif;margin:28px;background:#f4f7fb;color:#172b4d}}h1{{margin-bottom:4px}}#search{{width:min(680px,95%);padding:11px;border:1px solid #9aa9bd;border-radius:6px;font-size:16px}}#count{{color:#47607e}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}}.card{{background:white;border-radius:10px;padding:12px;box-shadow:0 1px 5px #bbc5d180;overflow-wrap:anywhere}}.thumb{{display:flex;height:190px;align-items:center;justify-content:center;background:#fff;border:1px solid #d9e0ea}}img{{max-width:100%;max-height:100%;object-fit:contain}}h2{{font-size:16px;margin:10px 0 6px}}p{{font-size:12px;color:#52657e;min-height:32px}}a{{color:#005bb5;font-weight:bold;text-decoration:none}}</style></head><body>
<h1>Ria Formosa — scientific bundle image gallery</h1><p id="count">{len(cards)} images. Each card heading is the exact filename in the bundle. Click a thumbnail to inspect the original file.</p>
<input id="search" placeholder="Search by figure name or folder…" autofocus><div class="grid" id="grid">{''.join(cards)}</div>
<script>const q=document.querySelector('#search'),cards=[...document.querySelectorAll('.card')],count=document.querySelector('#count');q.oninput=()=>{{let n=0,s=q.value.toLowerCase();cards.forEach(c=>{{let v=c.dataset.search.includes(s);c.style.display=v?'':'none';n+=v}});count.textContent=`${{n}} images shown`;}};</script>
</body></html>'''
    OUT.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT} with {len(cards)} images")


if __name__ == "__main__":
    main()
