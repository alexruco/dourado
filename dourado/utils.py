# utils.py
from urllib.parse import urlparse, urlunparse

def remove_duplicates(input_list):
    """
    Removes duplicate records from a list while preserving the original order.
    
    Args:
    input_list (list): The list from which to remove duplicates.

    Returns:
    list: A new list with duplicates removed.
    """
    seen = set()
    output_list = []
    for item in input_list:
        if item not in seen:
            seen.add(item)
            output_list.append(item)
    return output_list

def log_success(message):
    #print(message)
    silence = "is golden"

def is_content_page(url):
    content_extensions = (
        '.php', '.pdf', '.html', '.htm', '.asp', '.aspx', '.jsp', '.jspx',
        '.cgi', '.pl', '.cfm', '.xml', '.json', '.md', '.txt'
    )
    media_extensions = (
        '.jpg', '.jpeg', '.gif', '.webp', '.png', '.bmp', '.svg', '.ico',
        '.tif', '.tiff', '.mp4', '.mkv', '.webm', '.mp3', '.wav', '.ogg',
        '.avi', '.mov', '.wmv', '.flv', '.swf', '.m4a', '.m4v', '.aac',
        '.3gp', '.3g2', '.midi', '.mid', '.wma', '.aac', '.ra', '.ram', 
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', 
        '.ods', '.odp'
    )
    if any(url.lower().endswith(ext) for ext in content_extensions):
        return True
    if any(url.lower().endswith(ext) for ext in media_extensions):
        return False
    return True

def log_error(message):
    print(message)

def normalize_url(url):
    """
    Normalizes a URL by adding 'https://' if no scheme is present,
    and ensuring the URL is properly formatted.
    
    Args:
    url (str): The URL to normalize.

    Returns:
    str: The normalized URL.
    """
    parsed_url = urlparse(url)
    
    # Add 'https://' if no scheme is present
    if not parsed_url.scheme:
        parsed_url = urlparse(f'https://{url}')
    
    # Ensure the netloc is set properly
    if not parsed_url.netloc:
        parsed_url = urlparse(f'https://{parsed_url.path}')
    
    # Rebuild the URL ensuring correct structure
    normalized_url = urlunparse(parsed_url._replace(path='', query='', fragment=''))
    
    return normalized_url

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