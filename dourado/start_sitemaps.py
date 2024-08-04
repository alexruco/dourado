import requests
from check_robots import check_robots, extract_sitemaps_from_robots
from utils import log_error, log_success, remove_duplicates

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
            sitemaps.append((sitemap_url, 'available', 'valid'))  # Assuming these common sitemaps are available and valid
    log_success(f"#start_sitemaps.py/common_sitemap_filenames => sitemaps:{sitemaps}")
    return sitemaps

def consolidate_sitemaps(url):
    log_success(f"consolidate_sitemaps url:{url}")
    sitemaps = []

    robots_url = check_robots(url)
    log_success(f"consolidate_sitemaps robots_url:{robots_url}")
    if robots_url:
        sitemaps.extend(extract_sitemaps_from_robots(robots_url))

    sitemaps.extend(common_sitemap_filenames(url))

    # Remove duplicates while preserving order
    unique_sitemaps = list(dict.fromkeys(sitemaps))
    log_success(f"#start_sitemaps.py/consolidate_sitemaps => sitemaps:{unique_sitemaps}")
    if unique_sitemaps:
        log_success(f"start_sitemaps Found sitemaps: {unique_sitemaps}")
    else:
        log_error("No sitemaps found")

    return unique_sitemaps

# Example usage
if __name__ == "__main__":
    url = 'https://vivamelhor.pt'
    found_sitemaps = consolidate_sitemaps(url)
    print(f"start_sitemaps eu:{found_sitemaps}")
