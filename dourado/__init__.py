# my_python_module/__init__.py

"""
My Python Module
================

Checks the existence of robots.txt in a website; the presence of a valid sitemap 
on robots.txt; a full list of sitemaps; a list of webpages and sitemaps where they are found 

"""

__version__ = "0.1.0"

# __init__.py

from .check_robots import (
    check_robots,
    consolidate_sitemaps,
    extract_sitemaps_from_robots,
)
from .start_sitemaps import (
    common_sitemap_filenames,
    consolidate_sitemaps,
)
from .sitemap_crawler import (
    extract_sitemaps_from_content,
    crawl_sitemaps,
)
from virginia import (
    check_page_availability,
)
from .utils import (
    normalize_url,
    log_success,
    log_error,
)
from .sitemap_validator import (
    validate_sitemap,
    fetch_sitemap,
)
from .main import (
    website_sitemaps,
    get_valid_available_sitemaps,
    valid_sitemaps_robots,
)
