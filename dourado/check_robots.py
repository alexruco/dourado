# start_sitemaps.py
from urllib.parse import urljoin, urlparse, urlunparse
import requests
from utils import log_error, log_success, remove_duplicates
from virginia import check_page_availability

def fetch_robots_txt(url):
    """
    Fetches the content of the robots.txt file from the specified URL.
    
    Args:
    url (str): The URL of the site to fetch the robots.txt file from.

    Returns:
    str: The content of the robots.txt file, or None if the fetch failed.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    parsed_url = urlparse(url)
    robots_url = urljoin(parsed_url.geturl(), '/robots.txt')
    log_success(f"Fetching robots.txt from {robots_url}")
    
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            return response.text
        else:
            log_error(f"Failed to fetch robots.txt: Status code {response.status_code}")
            return None
    except requests.RequestException as e:
        log_error(f"Failed to fetch robots.txt: {e}")
        return None

def ensure_https(url):
    """
    Ensures that the URL uses the https scheme.

    Args:
    url (str): The URL to check and modify if necessary.

    Returns:
    str: The modified URL with https scheme.
    """
    parsed_url = urlparse(url)
    if parsed_url.scheme != 'https':
        parsed_url = parsed_url._replace(scheme='https')
        url = urlunparse(parsed_url)
    return url

def extract_sitemaps_from_robots(robots_txt):
    """
    Extracts sitemap URLs from the content of a robots.txt file.
    
    Args:
    robots_txt (str): The content of the robots.txt file.

    Returns:
    list: A list of sitemap URLs found in the robots.txt file.
    """
    sitemaps = []
    lines = robots_txt.splitlines()
    log_success(f"Total lines in robots.txt: {len(lines)}")
    for line in lines:
        line = line.strip()
        log_success(f"Processing line: '{line}'")
        if line.lower().startswith('sitemap:'):
            sitemap_url = line.split(':', 1)[1].strip()
            sitemap_url = ensure_https(sitemap_url)
            sitemaps.append(sitemap_url)
            log_success(f"Found sitemap: {sitemap_url}")
    log_success(f"#start_sitemaps.py/extract_sitemaps_from_robots => sitemaps: {sitemaps}")
    return sitemaps if sitemaps else []

def check_sitemaps_availability(sitemaps):
    """
    Checks the availability of each sitemap URL.
    
    Args:
    sitemaps (list): List of sitemap URLs to check.

    Returns:
    list: A list of tuples where each tuple contains a sitemap URL and a boolean indicating its availability.
    """
    sitemap_availability = []
    for sitemap in sitemaps:
        is_available = check_page_availability(sitemap)
        sitemap_availability.append((sitemap, is_available))
        log_success(f"#start_sitemaps.py/check_sitemaps_availability => sitemap: {sitemap}, available: {is_available}")
    return sitemap_availability

# Example usage
if __name__ == "__main__":
    robots_txt_url = 'vivamelhor.pt'
    robots_txt = fetch_robots_txt(robots_txt_url)
    if robots_txt:
        log_success(f"Fetched robots.txt content:\n{robots_txt}")
        sitemaps = extract_sitemaps_from_robots(robots_txt)
        sitemap_availability = check_sitemaps_availability(sitemaps)
        print(sitemap_availability)
    else:
        log_error("Failed to retrieve robots.txt content.")
