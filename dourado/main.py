#main.py

from start_sitemaps import consolidate_sitemaps
from sitemap_crawler import crawl_sitemaps
from virginia import check_page_availability
from utils import normalize_url, log_success
from check_robots import check_robots

def website_sitemaps(website_url):
    log_success(f"#main.py => website_url:{website_url}")
    
    encoded_url = normalize_url(url = website_url)
    log_success(f"#main.py => encoded_url:{encoded_url}")

    if not check_page_availability(url=encoded_url):
        return encoded_url
    else:
        start_sitemaps = consolidate_sitemaps(url=website_url)
        log_success(f"#main.py => start_sitemaps:{start_sitemaps}")

        sitemaps_list = crawl_sitemaps(sitemaps = start_sitemaps)
        log_success(f"#main.py => sitemaps_list:{sitemaps_list}")
      
        return sitemaps_list
    
# Example usage
website = 'https://mysitefaster.com/'
log_success(website_sitemaps(website_url = website))  