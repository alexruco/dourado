# functions.py
import requests

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

def check_url(url):
    try:
        # Send a HEAD request to the main URL
        response = requests.head(url, allow_redirects=True)
        # Check if the URL is reachable
        if response.status_code == 200:
            log_success(f'URL is reachable: {url}')
            return True
        else:
            log_success(f'URL is not reachable: {url} (Status code: {response.status_code})')
            return False
    except requests.RequestException:
        log_success('Website not available')
        return False

def log_success(message):
   silence = "is golden"
   #print(message)
    
def log_error(message):
    print(message)

def encode_urls(text):
    """Encode URLs in the text by replacing 'https://' with 'https_//'."""
    return text.replace('https://', 'https_//')