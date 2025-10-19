from datetime import date
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from pathlib import Path

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough = tostring(elem, encoding="utf-8")
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ")

def build_sitemap():
    today = date.today().isoformat()
    urls = [
        "https://www.packntec.com/",
        "https://www.packntec.com/about-us",
        "https://www.packntec.com/contact-us",
        "https://www.packntec.com/products",
        "https://www.packntec.com/blog",
    ]

    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for loc in urls:
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = loc
        SubElement(url, "lastmod").text = today
        SubElement(url, "changefreq").text = "weekly"
        SubElement(url, "priority").text = "0.7"

    xml_str = prettify(urlset)
    Path("reports").mkdir(exist_ok=True)
    Path("reports/sitemap.xml").write_text(xml_str, encoding="utf-8")
    print("✅ Sitemap built successfully!")

if __name__ == "__main__":
    build_sitemap()
