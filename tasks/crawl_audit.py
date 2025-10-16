# tasks/crawl_audit.py
import re, sys, requests, pandas as pd, lxml.html as LH
from urllib.parse import urljoin, urlparse
from collections import deque
from pathlib import Path

START = "https://www.packntec.com/"
MAX_PAGES = 40
UA = {"User-Agent": "packntec-marketing-bot/1.0 (+site audit)"}
SKIP_EXT = re.compile(r"\.(jpg|jpeg|png|gif|webp|svg|mp4|mov|avi|pdf|zip|rar|7z|docx?|pptx?|xlsx?)$", re.I)

def fetch_html(url):
    try:
        r = requests.get(url, timeout=20, headers=UA, allow_redirects=True)
        ct = (r.headers.get("Content-Type") or "").lower()
        if r.status_code < 400 and "text/html" in ct:
            return r.text, r.status_code
        return "", r.status_code
    except Exception as e:
        return "", f"ERR:{type(e).__name__}"

def audit_one(url):
    html, status = fetch_html(url)
    title = h1 = desc = canon = ""
    broken = 0
    if isinstance(status, int) and status < 400 and html:
        doc  = LH.fromstring(html)
        title = (doc.xpath("//title/text()") or [""])[0].strip()
        h1    = (doc.xpath("//h1//text()") or [""])[0].strip()
        meta  = doc.xpath("//meta[translate(@name,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='description']/@content")
        desc  = (meta[0] if meta else "").strip()
        can   = doc.xpath("//link[@rel='canonical']/@href")
        canon = (can[0] if can else "").strip()
        # quick internal link check
        for href in doc.xpath("//a/@href")[:80]:
            if not href or href.startswith(("#","mailto:","tel:")):
                continue
            tgt = urljoin(url, href)
            if SKIP_EXT.search(tgt): 
                continue
            try:
                rr = requests.head(tgt, timeout=8, allow_redirects=True)
                if rr.status_code >= 400: broken += 1
            except:
                broken += 1
    return dict(url=url, http_status=status, title=title, h1=h1,
                meta_description=desc, canonical=canon, broken_links=broken)

def discover(start):
    seen, out = set(), []
    q = deque([start])
    host = urlparse(start).netloc
    while q and len(out) < MAX_PAGES:
        url = q.popleft()
        if url in seen or SKIP_EXT.search(url): 
            continue
        seen.add(url)
        html, status = fetch_html(url)
        out.append(url)
        if isinstance(status, int) and status < 400 and html:
            doc = LH.fromstring(html)
            for h in doc.xpath("//a/@href"):
                if not h or h.startswith(("#","mailto:","tel:")): 
                    continue
                u = urljoin(url, h)
                p = urlparse(u)
                if p.netloc == host and u not in seen and not SKIP_EXT.search(u):
                    q.append(u)
    return out

def main():
    Path("reports").mkdir(parents=True, exist_ok=True)
    urls = discover(START)
    Path("reports/urls.txt").write_text("\n".join(urls), encoding="utf-8")
    rows = [audit_one(u) for u in urls]
    pd.DataFrame(rows).to_csv("reports/seo_audit.csv", index=False)
    print(f"Crawled {len(urls)} pages. Wrote reports/seo_audit.csv and reports/urls.txt")
    return 0  # never fail the job

if __name__ == "__main__":
    sys.exit(main())
