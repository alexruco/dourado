# pages_from_sitemap.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import log_error, log_success, normalize_url, is_content_page

def extract_pages_from_sitemap(sitemap_url):
    """
    Extracts all page URLs from a given sitemap URL.
    
    Args:
    sitemap_url (str): The URL of the sitemap to parse.

    Returns:
    list: A list of page URLs found in the sitemap.
    """
    page_urls = []
    try:
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            loc_tags = soup.find_all('loc')
            for loc in loc_tags:
                page_urls.append(loc.text.strip())
            log_success(f"Extracted {len(page_urls)} URLs from sitemap {sitemap_url}")
        else:
            log_error(f"Failed to fetch sitemap {sitemap_url}: Status code {response.status_code}")
    except requests.RequestException as e:
        log_error(f"Failed to fetch sitemap {sitemap_url}: {e}")

    return page_urls

def crawl_sitemaps_for_pages(sitemaps):
    """
    Crawls a list of sitemaps to extract all page URLs.
    
    Args:
    sitemaps (list): List of sitemap URLs to crawl.

    Returns:
    list: A list of tuples where each tuple contains a page URL and the sitemap URL it was found in.
    """
    all_page_urls = set()
    page_sitemap_pairs = []
    
    for sitemap_url in sitemaps:
        #sitemap_url = normalize_url(sitemap_url)
        
        page_urls = extract_pages_from_sitemap(sitemap_url)
        log_success(f"Found {len(page_urls)} URLs in sitemap {sitemap_url}")
        
        filtered_page_urls = list(filter(is_content_page, page_urls))
        log_success(f"Filtered down to {len(filtered_page_urls)} content pages in sitemap {sitemap_url}")
        
        for page_url in filtered_page_urls:
            if page_url not in all_page_urls:
                all_page_urls.add(page_url)
                page_sitemap_pairs.append((page_url, sitemap_url))
        
        log_success(f"Accumulated {len(all_page_urls)} unique pages so far.")

    log_success(f"Found {len(all_page_urls)} pages in total.")
    return page_sitemap_pairs

# Example usage
if __name__ == "__main__":
    sitemap = ['https://mysitefaster.com/post-sitemap.xml']
    pages = crawl_sitemaps_for_pages(sitemap)
    print(pages)
