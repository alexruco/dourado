
# collect_sitemaps.py

from get_sitemaps import extract_sitemaps_from_robots, common_sitemap_filenames
from check_robots import check_robots
from functions import log_error, log_success
import requests

def collect_sitemaps(url):
    sitemaps = []

    robots_url = check_robots(url)
    if robots_url:
        response = requests.get(robots_url)
        if response.status_code == 200:
            robots_txt = response.text
            sitemaps.extend(extract_sitemaps_from_robots(robots_txt))

    sitemaps.extend(common_sitemap_filenames(url))

    # Remove duplicates
    sitemaps = list(set(sitemaps))

    if sitemaps:
        log_success(f"Found sitemaps: {sitemaps}")
    else:
        log_error("No sitemaps found")

    return sitemaps
# Example usage
url = 'https://ruco.pt'
print(collect_sitemaps(url))
