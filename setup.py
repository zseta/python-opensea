#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = ['requests>=2.26.0']

test_requirements = ['pytest>=3', ]

setup(
    author="Attila Toth",
    author_email='hello@attilatoth.dev',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
        
    ],
    description="Python 3 wrapper for the OpenSea NFT API",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='opensea',
    maintainer='Attila Toth',
    maintainer_email='hello@attilatoth.dev',
    name='opensea-api',
    packages=find_packages(include=['opensea', 'opensea.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/zseta/python-opensea',
    project_urls={
        'Documentation': 'https://opensea-api.attilatoth.dev',
        'Source': 'https://github.com/zseta/opensea'
    },
    version='0.1.2',
    zip_safe=False,
)
