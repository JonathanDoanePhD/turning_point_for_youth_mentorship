"""Build the GitHub Pages site: copy website/ to an output folder and point links to project documents at GitHub.

The website links to documents with relative paths (../docs/..., ../manuscripts/...), which work when browsing the repository
but not on GitHub Pages, where only the website is served. This rewrites those links to the files' rendered views on GitHub.
Standard library only (runs in the Pages workflow without installing anything).

Usage: python scripts/build_pages.py _site
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_BLOB = "https://github.com/JonathanDoanePhD/turning_point_for_youth_mentorship/blob/main/"
LINK = re.compile(r'(["\'])\.\./((?:docs|manuscripts|crosscheck|outputs|scripts|config|src|tests)/[^"\']*|README\.md|LICENSE)')
TEXT_SUFFIXES = {".html", ".js", ".css"}


def main(out: str) -> None:
    dst = Path(out)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(ROOT / "website", dst)
    n = 0
    for f in dst.rglob("*"):
        if f.suffix in TEXT_SUFFIXES:
            s = f.read_text()
            new, k = LINK.subn(lambda m: m.group(1) + REPO_BLOB + m.group(2), s)
            if k:
                f.write_text(new)
                n += k
    leftovers = [(str(f.relative_to(dst)), m.group(0)) for f in dst.rglob("*") if f.suffix in TEXT_SUFFIXES
                 for m in re.finditer(r'["\']\.\./[^"\']+', f.read_text())]
    assert not leftovers, leftovers
    (dst / ".nojekyll").write_text("")
    print(f"built {dst} ({n} document links rewritten)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "_site")
