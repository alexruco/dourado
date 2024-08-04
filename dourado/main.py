from start_sitemaps import consolidate_sitemaps
from sitemap_crawler import crawl_sitemaps
from pages_from_sitemap import crawl_sitemaps_for_pages
from virginia import check_page_availability
from utils import normalize_url, log_success, log_error
from sitemap_validator import validate_sitemap, fetch_sitemap
from check_robots import check_robots, extract_sitemaps_from_robots

def website_sitemaps(website_url):
    log_success(f"#main.py => website_url:{website_url}")
    
    encoded_url = normalize_url(url=website_url)
    log_success(f"#main.py => encoded_url:{encoded_url}")

    if not check_page_availability(url=encoded_url):
        return encoded_url
    else:
        start_sitemaps = consolidate_sitemaps(url=website_url)
        log_success(f"#main.py => start_sitemaps:{start_sitemaps}")

        sitemaps_list = crawl_sitemaps(sitemaps=start_sitemaps)
        log_success(f"#main.py => sitemaps_list:{sitemaps_list}")

        sitemaps_status = []
        for sitemap_url in sitemaps_list:
            is_available = check_page_availability(sitemap_url)
            availability_status = 'available' if is_available else 'unavailable'
            validity = 'unavailable' if not is_available else 'invalid'
            if is_available:
                sitemap_content = fetch_sitemap(sitemap_url)
                is_valid = validate_sitemap(sitemap_content) if sitemap_content else False
                validity = 'valid' if is_valid else 'invalid'
            sitemaps_status.append({
                'url': sitemap_url,
                'availability': availability_status,
                'validity': validity
            })
        log_success(f"#main.py => sitemaps_status:{sitemaps_status}")

        return sitemaps_status

def pages_from_sitemaps(website_url):
    """
    Collects the valid and available sitemaps, crawls them for pages, and returns the result.
    
    Args:
    website_url (str): The URL of the website to get sitemaps for.

    Returns:
    list: A list of all page URLs found in the valid and available sitemaps.
    """
    sitemaps_status = website_sitemaps(website_url)
    valid_available_sitemaps = [sitemap['url'] for sitemap in sitemaps_status if sitemap['availability'] == 'available' and sitemap['validity'] == 'valid']
    log_success(f"#main.py => valid_available_sitemaps: {valid_available_sitemaps}")

    pages = crawl_sitemaps_for_pages(valid_available_sitemaps)
    log_success(f"#main.py => pages: {pages}")
    
    return pages

def robots_exists(website_url):
    robots_txt = check_robots(url=website_url)
    if(robots_txt):
        return True
    else:
        return False

def valid_sitemaps_robots(website_url):
    robots_txt_url = check_robots(url=website_url)
    if not robots_txt_url:
        return False  # Return False if robots.txt is not available
    
    sitemaps_from_robots = extract_sitemaps_from_robots(robots_txt_url)
    
    for sitemap in sitemaps_from_robots:
        if sitemap[1] == 'available' and sitemap[2] == 'valid':  # Access tuple elements by index
            return True  # Return True if at least one sitemap is available and valid
    
    return False  # Return False if no valid and available sitemaps are found

# Example usage
website = 'https://mysitefaster.com/'
print(f"#main eu: valid_sitemaps_robots:{valid_sitemaps_robots(website_url=website)}")
print(f"#main eu: website_sitemaps:{website_sitemaps(website_url=website)}")
print(f"#main eu:pages_from_sitemaps:{pages_from_sitemaps(website_url=website)}")
print(f"#main eu:robots_exists:{robots_exists(website_url=website)}")
