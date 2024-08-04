import requests
from urllib.parse import urljoin
from lxml import etree
from utils import log_success, log_error

def extract_sitemaps_from_content(content):
    """
    Extracts sitemap URLs from the given content of a sitemap or robots.txt.
    
    Args:
    content (str): The content to parse.

    Returns:
    list: A list of sitemap URLs found in the content.
    """
    sitemaps = []
    try:
        parser = etree.XMLParser(recover=True)
        root = etree.fromstring(content.encode('utf-8'), parser)
        # Check for <sitemap> tags in sitemap index files
        sitemap_tags = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap')
        for sitemap in sitemap_tags:
            loc_tag = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc_tag is not None:
                sitemaps.append(loc_tag.text.strip())
    except etree.XMLSyntaxError as e:
        log_error(f"Failed to parse XML content: {e}")
    
    return sitemaps

def crawl_sitemaps(sitemaps, depth=5):
    """
    Crawls a list of sitemaps to discover nested sitemaps up to a given depth.
    
    Args:
    sitemaps (list): List of initial sitemap tuples to crawl (URL, availability, validity).
    depth (int): The maximum depth to crawl for nested sitemaps.

    Returns:
    list: A list of all discovered sitemap URLs.
    """
    discovered_sitemaps = set(sitemap[0] for sitemap in sitemaps)
    log_success(f"crawl_sitemaps discovered_sitemaps: {discovered_sitemaps}")
    to_crawl = [sitemap[0] for sitemap in sitemaps]
    current_depth = 0

    while to_crawl and current_depth < depth:
        next_to_crawl = []
        for sitemap_url in to_crawl:
            log_success(f"crawl_sitemaps.py sitemap_url: {sitemap_url}")
            try:
                response = requests.get(sitemap_url)
                if response.status_code == 200:
                    new_sitemaps = extract_sitemaps_from_content(response.text)
                    log_success(f"new_sitemaps: {new_sitemaps}")

                    for new_sitemap in new_sitemaps:
                        full_url = urljoin(sitemap_url, new_sitemap)
                        log_success(f"full_url: {full_url}")

                        if full_url not in discovered_sitemaps:
                            discovered_sitemaps.add(full_url)
                            next_to_crawl.append(full_url)
            except requests.RequestException as e:
                log_error(f"Failed to crawl {sitemap_url}: {e}")

        to_crawl = next_to_crawl
        current_depth += 1

    return list(discovered_sitemaps)

# Example usage
if __name__ == "__main__":
    initial_sitemaps = [('https://mysitefaster.com/sitemap_index.xml', 'available', 'valid')]
    all_sitemaps = crawl_sitemaps(initial_sitemaps)
    log_success(all_sitemaps)
