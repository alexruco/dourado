from setuptools import setup, find_packages

setup(
    name='dourado',
    version='0.1.0',
    description='A tool for crawling, validating, and extracting page URLs from website sitemaps.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alex Ruco',
    author_email='alex@ruco.pt',
    url='https://github.com/alexruco/dourado',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'beautifulsoup4',
        'lxml'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'dourado=dourado.main:main',
        ],
    },
)
