# start_sitemaps.py
from urllib.parse import urljoin
import requests
from check_robots import check_robots
from utils import log_error, log_success, remove_duplicates
from virginia import check_page_availability
from check_robots import extract_sitemaps_from_robots

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
    log_success(f"#start_sitemaps.py/common_sitemap_filenames => sitemaps:{sitemaps}")
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
    log_success(f"#start_sitemaps.py/consolidate_sitemaps => sitemaps:{sitemaps}")
    if sitemaps:
        log_success(f"Found sitemaps: {sitemaps}")
    else:
        log_error("No sitemaps found")

    return sitemaps


# Example usage
url = 'https://mysitefaster.com'
found_sitemaps = consolidate_sitemaps(url)
