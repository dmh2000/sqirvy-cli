"""
Utility functions for file and URL operations.
"""

import os
from urllib.parse import urlparse
import string
import requests
from bs4 import BeautifulSoup


def read_file(filename):
    """
    Read a file and return its contents as a string.

    Args:
        filename (str): Path to the file to read

    Returns:
        str: Contents of the file

    Raises:
        FileNotFoundError: If the file does not exist
        Exception: If the file contains non-printable characters
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        # Check if content contains only printable characters
        printable_set = set(string.printable)
        if not all(char in printable_set for char in content):
            raise ValueError(f"File {filename} contains non-printable characters")

        return content
    except ValueError as e:
        print(f"File {filename} contains non-printable characters {e}")
        raise
    except FileNotFoundError as e:
        print(f"File {filename} not found {e}")
        raise
    except Exception as e:
        raise Exception(f"Error reading file {filename}: {str(e)}")


def scrape_url(url):
    """
    Fetch and parse a URL, extracting human-readable text.

    Args:
        url (str): URL to fetch and parse

    Returns:
        str: Extracted text content from the URL

    Raises:
        Exception: If the URL cannot be fetched or parsed
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()

        # Get text
        text = soup.get_text()

        # Break into lines and remove leading/trailing space
        lines = (line.strip() for line in text.splitlines())

        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

        # Drop blank lines
        text = "\n".join(chunk for chunk in chunks if chunk)

        return text
    except Exception as e:
        raise Exception(f"Error fetching URL {url}: {str(e)}")


def read_content(sources):
    """
    Read content from a list of sources, which can be local files or URLs.

    Args:
        sources (list): List of strings that can be filenames or URLs

    Returns:
        list: List of strings containing the content of each source
    """
    results = []

    for source in sources:
        # Check if the source is a URL
        parsed = urlparse(source)
        if parsed.scheme and parsed.netloc:  # Has both scheme and domain
            # It's a URL
            content = scrape_url(source)
            results.append(content)
        else:
            # It's a local file
            content = read_file(source)
            results.append(content)

    return results
