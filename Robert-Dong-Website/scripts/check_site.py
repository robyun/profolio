"""Check generated pages and local links: python scripts/check_site.py _site /al-folio."""

from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.bad_meta = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and "<" in attrs.get("content", ""):
            self.bad_meta = True
        for key in ("href", "src"):
            if attrs.get(key):
                self.urls.append(attrs[key])


def check(root, base):
    root = root.resolve()
    base = base.rstrip("/")
    failures = []
    for route in ("index.html", "research/index.html", "publications/index.html", "cv/index.html", "404.html"):
        if not (root / route).is_file():
            failures.append(f"Missing page: {route}")
    for page in root.rglob("*.html"):
        markup = page.read_text(encoding="utf-8")
        if any(text in markup for text in ("Albert Einstein", "you@example.com", "Write your biography here", "example_pdf.pdf")):
            failures.append(f"Demo content: {page.relative_to(root)}")
        links = Links()
        links.feed(markup)
        if links.bad_meta:
            failures.append(f"HTML in metadata: {page.relative_to(root)}")
        for url in links.urls:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = unquote(parsed.path)
            if path.startswith("/"):
                if base and not (path == base or path.startswith(base + "/")):
                    failures.append(f"Link misses base path in {page.relative_to(root)}: {url}")
                    continue
                target = root / path.removeprefix(base).lstrip("/")
            else:
                target = page.parent / path
            if not target.is_file() and not (target / "index.html").is_file():
                failures.append(f"Broken link in {page.relative_to(root)}: {url}")
    pdf = root / "assets/pdf/robert-dong-cv.pdf"
    if not pdf.is_file() or not pdf.read_bytes().startswith(b"%PDF-"):
        failures.append("Missing or invalid CV PDF")
    if failures:
        raise SystemExit("\n".join(sorted(set(failures))))
    print(f"Passed: required pages, local links/assets, CV PDF, and demo-content check ({base or '/'}).")


if __name__ == "__main__":
    check(Path(sys.argv[1] if len(sys.argv) > 1 else "_site"), sys.argv[2] if len(sys.argv) > 2 else "")
