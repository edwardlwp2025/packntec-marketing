from datetime import date
from xml.etree.ElementTree import Element, SubElement, ElementTree
from pathlib import Path

def build_sitemap():
    today = date.today().isoformat()
    urls = [
        "https://www.packntec.com/",
        "https://www.packntec.com/about-us",
        "https://www.packntec.com/contact-us",
        "https://www.packntec.com/products",
        "https://www.packntec.com/blog",
    ]

    # Build XML structure
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for loc in urls:
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = loc
        SubElement(url, "lastmod").text = today
        SubElement(url, "changefreq").text = "weekly"
        SubElement(url, "priority").text = "0.7"

    # Output file
    Path("reports").mkdir(exist_ok=True)
    output_path = Path("reports/sitemap.xml")

    # Write formatted XML
    tree = ElementTree(urlset)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    print(f"✅ Sitemap successfully written to {output_path}")

if __name__ == "__main__":
    build_sitemap()
