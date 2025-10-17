# tasks/crawl_audit.py  (SAFE: never fails job on 404/timeouts)
import requests, pandas as pd, lxml.html as LH
from urllib.parse import urljoin
from pathlib import Path

# Start small; we can add more pages later
PAGES = [
    "https://www.packntec.com/",
    # add real pages that exist on your site as you confirm them
]

UA = {"User-Agent": "packntec-bot/1.0 (+site audit)"}

def fetch(url):
    try:
        r = requests.get(url, timeout=20, headers=UA, allow_redirects=True)
        # DON'T raise_for_status — we log status instead
        return (r.text if r.status_code < 400 else ""), r.status_code
    except Exception as e:
        return "", f"ERR:{type(e).__name__}"

def audit(url):
    html, status = fetch(url)
    title = h1 = desc = canon = ""
    broken = 0
    if isinstance(status, int) and status < 400 and html:
        doc  = LH.fromstring(html)
        title = (doc.xpath('//title/text()') or [''])[0].strip()
        h1    = (doc.xpath('//h1//text()') or [''])[0].strip()
        meta  = doc.xpath("//meta[translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='description']/@content")
        desc  = (meta[0] if meta else "").strip()
        can   = doc.xpath("//link[@rel='canonical']/@href")
        canon = (can[0] if can else "").strip()
        # quick internal link check (non-blocking)
        for href in doc.xpath("//a/@href")[:50]:
            if not href or href.startswith(('#','mailto:','tel:')): 
                continue
            try:
                test = urljoin(url, href)
                rr = requests.head(test, timeout=8, allow_redirects=True)
                if rr.status_code >= 400: broken += 1
            except:
                broken += 1
    return dict(url=url, http_status=status, title=title, h1=h1,
                meta_description=desc, canonical=canon, broken_links=broken)

def run(out_csv="reports/seo_audit.csv"):
    rows = [audit(u) for u in PAGES]
    Path("reports").mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    print(f"Wrote {out_csv} for {len(PAGES)} page(s)")

if __name__ == "__main__":
    run()
