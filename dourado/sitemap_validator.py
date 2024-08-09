import requests
import xml.etree.ElementTree as ET
from dourado.utils import log_error, log_success

def fetch_sitemap(url):
    """
    Fetches the content of the sitemap from the specified URL.
    
    Args:
    url (str): The URL of the sitemap to fetch.

    Returns:
    str: The content of the sitemap, or None if the fetch failed.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            log_error(f"Failed to fetch sitemap: Status code {response.status_code} - URL: {url}")
            return None
    except requests.RequestException as e:
        log_error(f"Failed to fetch sitemap: {e} - URL: {url}")
        return None

def validate_sitemap(sitemap_content, sitemap_url):
    """
    Validates the sitemap content as XML.
    
    Args:
    sitemap_content (str): The content of the sitemap to validate.
    sitemap_url (str): The URL of the sitemap being validated.

    Returns:
    bool: True if the sitemap is valid XML, False otherwise.
    """
    try:
        # Attempt to parse the sitemap content
        ET.fromstring(sitemap_content)
        log_success(f"Sitemap is valid XML - URL: {sitemap_url}")
        return True
    except ET.ParseError as e:
        log_error(f"Sitemap is invalid XML: {e} - URL: {sitemap_url}")
        return False

# Example usage
if __name__ == "__main__":
    sitemap_url = 'https://mysitefaster.com/sitemap_index.xml'
    sitemap_content = fetch_sitemap(sitemap_url)
    if sitemap_content:
        log_success(f"Fetched sitemap content from {sitemap_url}:\n{sitemap_content[:200]}...")  # Log only the first 200 characters
        is_valid = validate_sitemap(sitemap_content, sitemap_url)
        if is_valid:
            log_success("Sitemap validation passed.")
        else:
            log_error("Sitemap validation failed.")
    else:
        log_error("Failed to retrieve sitemap content.")
