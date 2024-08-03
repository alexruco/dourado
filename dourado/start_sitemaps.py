# start_sitemaps.py
from urllib.parse import urljoin
import requests
from check_robots import check_robots
from utils import log_error, log_success, remove_duplicates

def extract_sitemaps_from_robots(robots_txt):
    sitemaps = []
    for line in robots_txt.splitlines():
        if line.strip().lower().startswith('sitemap:'):
            sitemaps.append(line.split(':', 1)[1].strip())
    return sitemaps if sitemaps else []

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

def consolidate_sitemaps(url):
    sitemaps = []

    robots_url = check_robots(url)
    if robots_url:
        response = requests.get(robots_url)
        if response.status_code == 200:
            robots_txt = response.text
            sitemaps.extend(extract_sitemaps_from_robots(robots_txt))

    sitemaps.extend(common_sitemap_filenames(url))

    # Remove duplicates while preserving order
    sitemaps = remove_duplicates(sitemaps)
    
    if sitemaps:
        log_success(f"Found sitemaps: {sitemaps}")
    else:
        log_error("No sitemaps found")

    return sitemaps

# Example usage
#url = 'https://mysitefaster.com'
#found_sitemaps = consolidate_sitemaps(url)
