# tasks/crawl_audit.py
import pandas as pd, requests, lxml.html as LH
from urllib.parse import urljoin

PAGES = [
    "https://www.packntec.com/",         # always safe
    "https://www.packntec.com/contact-us",  # guess; OK if 404 (we log it)
    # add more real URLs later (About, Products, etc.)
]

UA = {'User-Agent': 'packntec-bot/1.0 (+site audit)'}

def fetch(url):
    try:
        r = requests.get(url, timeout=20, headers=UA, allow_redirects=True)
        return r.text if r.status_code < 400 else "", r.status_code
    except Exception as e:
        return "", f"ERR:{type(e).__name__}"

def audit(url):
    html, status = fetch(url)
    title = h1 = desc = canon = ""
    broken = 0

    if isinstance(status, int) and status < 400 and html:
        doc  = LH.fromstring(html)
        title = (doc.xpath('//title/text()') or [''])[0].strip()
        h1    = (doc.xpath('//h1/text()') or [''])[0].strip()
        meta  = doc.xpath("//meta[translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='description']/@content")
        desc  = meta[0].strip() if meta else ''
        canon = (doc.xpath("//link[@rel='canonical']/@href') or [''])[0]

        # check internal links quickly
        for href in doc.xpath("//a/@href"):
            if href.startswith(('#','mailto:','tel:')): 
                continue
            test = urljoin(url, href)
            try:
                rr = requests.head(test, timeout=10, allow_redirects=True)
                if rr.status_code >= 400: broken += 1
            except:
                broken += 1

    return dict(
        url=url, http_status=status,
        title=title, h1=h1, meta_description=desc,
        canonical=canon, broken_links=broken
    )

def run(out_csv="reports/seo_audit.csv"):
    rows = [audit(u) for u in PAGES]
    df = pd.DataFrame(rows)
    df.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv}")

if __name__ == "__main__":
    run()
