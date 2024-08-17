# dourado/check_robots.py
from dourado.utils import log_error, log_success, ensure_https
import requests
from urllib.parse import urljoin, urlparse
from virginia import check_page_availability
from dourado.sitemap_validator import fetch_sitemap, validate_sitemap
from dourado.sitemap_crawler import crawl_sitemaps

def check_robots(url):
    """
    Checks the robots.txt file for the site and returns the URL if found.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    parsed_url = urlparse(url)
    robots_url = urljoin(parsed_url.geturl(), '/robots.txt')
    log_success(f"Fetching robots.txt from {robots_url}")
    
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            return robots_url
        else:
            log_error(f"Failed to fetch robots.txt: Status code {response.status_code}")
            return None
    except requests.RequestException as e:
        log_error(f"Failed to fetch robots.txt: {e}")
        return None
    
def sitemap_indicated_on_robots(url):
    """
    Checks if at least one sitemap is indicated in the robots.txt file of the given website.

    Args:
    url (str): The URL of the website.

    Returns:
    bool: True if at least one sitemap is indicated in the robots.txt file, False otherwise.
    """
    # Get the robots.txt URL
    robots_url = check_robots(url)
    if not robots_url:
        return False
    
    # Extract sitemaps from the robots.txt file
    sitemaps = extract_sitemaps_from_robots(robots_url)
    
    # Return True if there is at least one sitemap, otherwise False
    return bool(sitemaps)

def extract_sitemaps_from_robots(robots_url):
    """
    Extracts sitemap URLs from the robots.txt file at the given URL, and checks their availability and validity.
    
    Args:
    robots_url (str): The URL of the robots.txt file.

    Returns:
    list: A list of tuples containing sitemap URLs, availability, and validity status.
    """
    sitemaps = []
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            robots_txt = response.text
            lines = robots_txt.splitlines()
            log_success(f"Total lines in robots.txt: {len(lines)}")
            for line in lines:
                line = line.strip()
                log_success(f"Processing line: '{line}'")
                if line.lower().startswith('sitemap:'):
                    sitemap_url = line.split(':', 1)[1].strip()
                    sitemap_url = ensure_https(sitemap_url)
                    is_available = check_page_availability(sitemap_url)
                    availability_status = 'available' if is_available else 'unavailable'
                    validity = "unavailable"
                    if is_available:
                        sitemap_content = fetch_sitemap(sitemap_url)
                        is_valid = validate_sitemap(sitemap_content, robots_url) if sitemap_content else False
                        validity = "valid" if is_valid else "invalid"
                    sitemaps.append((sitemap_url, availability_status, validity))
                    log_success(f"Found sitemap: {sitemap_url}, availability: {availability_status}, validity: {validity}")
        else:
            log_error(f"Failed to fetch robots.txt: Status code {response.status_code}")
    except requests.RequestException as e:
        log_error(f"Failed to fetch robots.txt: {e}")
    log_success(f"#check_robots.py/extract_sitemaps_from_robots => sitemaps: {sitemaps}")
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
    website_url = 'https://mysitefaster.com'
    if sitemap_indicated_on_robots(website_url):
        print("Sitemap is indicated in robots.txt")
    else:
        print("No sitemap indicated in robots.txt")