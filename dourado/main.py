from start_sitemaps import consolidate_sitemaps
from sitemap_crawler import crawl_sitemaps
from virginia import check_page_availability
from utils import encode_urls

def website_sitemaps(website_url):
    
    encoded_url = encode_urls(text = website_url)
    if not check_page_availability(url=encoded_url):
        return False
    else:
        start_sitemaps = consolidate_sitemaps(url=website_url)
        sitemaps_list = crawl_sitemaps(sitemaps = start_sitemaps)
        
        return sitemaps_list

# Example usage
website = 'https://vivamelhor.pt/'
print(website_sitemaps(website_url = website))