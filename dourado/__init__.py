# my_python_module/__init__.py

"""
My Python Module
================

Checks the existence of robots.txt in a website; the presence of a valid sitemap 
on robots.txt; a full list of sitemaps; a list of webpages and sitemaps where they are found 

"""

__version__ = "0.1.0"

from .check_robots import check_robots


__all__ = [
    "some_function",
    "package_function"
]
