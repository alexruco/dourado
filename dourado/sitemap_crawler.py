# sitemap_crawler.py
import requests
from urllib.parse import urljoin, urlparse
from utils import log_success, log_error, remove_duplicates

def extract_sitemaps_from_content(content):
    sitemaps = []
    for line in content.splitlines():
        if line.strip().lower().startswith('sitemap:'):
            sitemaps.append(line.split(':', 1)[1].strip())
    return sitemaps

def crawl_sitemaps(sitemaps, depth=5):
    discovered_sitemaps = set(sitemaps)
    to_crawl = sitemaps[:]
    current_depth = 0

    while to_crawl and current_depth < depth:
        next_to_crawl = []
        for sitemap_url in to_crawl:
            try:
                response = requests.get(sitemap_url)
                if response.status_code == 200:
                    new_sitemaps = extract_sitemaps_from_content(response.text)
                    log_success(f"sitemap added:{new_sitemaps}")
                    for new_sitemap in new_sitemaps:
                        full_url = urljoin(sitemap_url, new_sitemap)
                        if full_url not in discovered_sitemaps:
                            discovered_sitemaps.add(full_url)
                            log_success(f"sitemap added:{full_url}")
                            next_to_crawl.append(full_url)
            except requests.RequestException as e:
                log_error(f"Failed to crawl {sitemap_url}: {e}")

        to_crawl = next_to_crawl
        current_depth += 1

    return list(discovered_sitemaps)

# Example usage
#initial_sitemaps = ['https://mysitefaster.com/sitemap_index.xml']
#all_sitemaps = crawl_sitemaps(initial_sitemaps)
#print(all_sitemaps)
