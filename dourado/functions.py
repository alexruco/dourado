# functions.py
import requests

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
    print(message)
    
def log_error(message):
    print(message)
    
