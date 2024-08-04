# Dourado 🚀

Welcome to **Dourado**! This project is designed to bring info about a website sitemaps.

## Features ✨

- **robots_exists(website_url)**: ✅ Checks if `robots.txt` exists in the website root and returns a boolean.
- **valid_sitemaps_robots(website_url)**: 🔍 Verifies if there is at least one available and valid sitemap in `robots.txt` and returns a boolean.
- **website_sitemaps(website_url)**: 📜 Retrieves and returns a list of all sitemaps from the given website.
- **pages_from_sitemaps(website_url)**: 🌐 Extracts and returns a list of page URLs from the sitemaps of the given website.



## Installation 💻

You can install the package via pip:

```bash
pip install GIT+https://github.com/alexruco/dourado 
Usage 📚

Here's a quick example to get you started:
<!--
```python
from dourado import dourado

# Example usage
website = 'https://mysitefaster.com/'
print(f"valid_sitemaps_robots:{valid_sitemaps_robots(website_url=website)}")
print(f"website_sitemaps:{website_sitemaps(website_url=website)}")
print(f"pages_from_sitemaps:{pages_from_sitemaps(website_url=website)}")
print(f"#robots_exists:{robots_exists(website_url=website)}")

```
-->


## Contributing 🤝

We welcome contributions from the community! Here’s how you can get involved:

1. **Report Bugs**: If you find a bug, please open an issue [here](https://github.com/alexruco/dourado/issues).
2. **Suggest Features**: We’d love to hear your ideas! Suggest new features by opening an issue.
3. **Submit Pull Requests**: Ready to contribute? Fork the repo, make your changes, and submit a pull request. Please ensure your code follows our coding standards and is well-documented.
4. **Improve Documentation**: Help us improve our documentation. Feel free to make edits or add new content.

### How to Submit a Pull Request

1. Fork the repository.
2. Create a new branch: `git checkout -b my-feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin my-feature-branch`.
5. Open a pull request on the original repository.

## Contact information
For any questions or suggestions, please contact:

    Alex Ruco: alex@ruco.pt
    GitHub: https://github.com/alexruco

## Honor
Named in the honor of Fernão Dourado, a famous Portuguese cartographer of the sixteenth century

## License 📄

This project is licensed under the MIT License. Feel free to use, modify, and distribute this software in accordance with the terms outlined in the [LICENSE](LICENSE) file.


