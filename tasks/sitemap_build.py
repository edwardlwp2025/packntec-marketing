# tasks/sitemap_build.py
import time
from pathlib import Path

DOMAIN = "https://www.packntec.com"
OUT    = Path("reports/sitemap.xml")

URLS = [
    f"{DOMAIN}/",
    f"{DOMAIN}/products",
    f"{DOMAIN}/contact-us",
    # TODO: add more product/category URLs here
]

def run():
    now = time.strftime("%Y-%m-%d")
    items = "\n".join(
        f"<url><loc>{u}</loc><lastmod>{now}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>"
        for u in URLS
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n' \
          f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(xml, encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    run()
