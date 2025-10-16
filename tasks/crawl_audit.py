# tasks/crawl_audit.py
import pandas as pd, requests, lxml.html as LH
from urllib.parse import urljoin

PAGES = [
    "https://www.packntec.com/",
    "https://www.packntec.com/products",
    "https://www.packntec.com/contact-us",
]

def fetch(url):
    r = requests.get(url, timeout=20, headers={'User-Agent':'packntec-bot/1.0'})
    r.raise_for_status()
    return r.text

def audit(url):
    html = fetch(url)
    doc  = LH.fromstring(html)
    title = (doc.xpath('//title/text()') or [''])[0].strip()
    h1    = (doc.xpath('//h1/text()') or [''])[0].strip()
    meta  = doc.xpath("//meta[translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='description']/@content")
    desc  = meta[0].strip() if meta else ''
    canon = (doc.xpath("//link[@rel='canonical']/@href") or [''])[0]
    broken = 0
    for href in doc.xpath("//a/@href"):
        if href.startswith(('#','mailto:','tel:')): 
            continue
        test = urljoin(url, href)
        try:
            rr = requests.head(test, timeout=10, allow_redirects=True)
            if rr.status_code >= 400: broken += 1
        except: broken += 1
    return dict(url=url, title=title, h1=h1, meta_description=desc, canonical=canon, broken_links=broken)

def run(out_csv="reports/seo_audit.csv"):
    rows = [audit(u) for u in PAGES]
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    print(f"Wrote {out_csv}")

if __name__ == "__main__":
    run()
