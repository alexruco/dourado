# check_robots.py

from urllib.parse import urljoin
from functions import check_url, log_error, log_success
import requests


def check_robots(url):
    # Ensure the URL has a scheme (http or https)
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    if not check_url(url):
        log_error(f"Cannot check robots.txt because the URL is not reachable: {url}")
        return False

    # Construct the robots.txt URL
    robots_url = urljoin(url, '/robots.txt')

    try:
        # Send a GET request to the robots.txt URL
        response = requests.get(robots_url)

        # Check if the robots.txt file exists
        if response.status_code == 200:
            log_success(f'robots.txt found at {robots_url}')
            return robots_url
        elif response.status_code == 404:
            log_error(f'robots.txt not found at {robots_url}')
            return False
        else:
            log_error(f'Unexpected status code ({response.status_code}) when checking {robots_url}')
            return False
    except requests.RequestException:
        log_error('Error checking robots.txt')
        return False

# Example usage
url = 'smartcursos.mycustom.page'
check_robots(url)
