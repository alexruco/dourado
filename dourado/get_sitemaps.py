from urllib.parse import urljoin
import requests

def extract_sitemaps_from_robots(robots_txt):
    sitemaps = []
    for line in robots_txt.splitlines():
        if line.strip().lower().startswith('sitemap:'):
            sitemaps.append(line.split(':', 1)[1].strip())
    return sitemaps if sitemaps else False

def common_sitemap_filenames(url):
    common_filenames = [
        'sitemap.xml', 
        'sitemap-index.xml', 
        'sitemap1.xml', 
        'sitemap1-index.xml'
    ]
    sitemaps = []
    for filename in common_filenames:
        sitemap_url = f"{url.rstrip('/')}/{filename}"
        response = requests.head(sitemap_url)
        if response.status_code == 200:
            sitemaps.append(sitemap_url)
    return sitemaps

