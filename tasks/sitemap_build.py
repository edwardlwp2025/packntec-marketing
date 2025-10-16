# tasks/sitemap_build.py
from pathlib import Path
from time import strftime

URL_LIST = Path("reports/urls.txt")
OUT = Path("reports/sitemap.xml")

def main():
    urls = []
    if URL_LIST.exists():
        urls = [u.strip() for u in URL_LIST.read_text(encoding="utf-8").splitlines() if u.strip()]
    if not urls:
        urls = ["https://www.packntec.com/"]

    today = strftime("%Y-%m-%d")
    items = "\n".join(
        f"<url><loc>{u}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>"
        for u in urls
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n' \
          f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(xml, encoding="utf-8")
    print(f"Wrote {OUT} with {len(urls)} URLs")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
