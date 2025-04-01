"""
Tests for the files utility module.
"""

import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
from urllib.parse import urlparse

from .files import read_file, scrape_url, read_content

project_prefix = "python/sqirvy_cli/sqirvy_cli"


class TestReadFile(unittest.TestCase):
    """Tests for the read_file function."""

    @patch("builtins.open", new_callable=mock_open, read_data="test content")
    def test_read_file_success(self, mock_file):
        """Test reading a file successfully."""
        result = read_file("test.txt")
        self.assertEqual(result, "test content")
        mock_file.assert_called_once_with("test.txt", "r", encoding="utf-8")

    @patch("builtins.open", side_effect=FileNotFoundError("No such file"))
    def test_read_file_not_found(self, mock_file):
        """Test handling of a file that doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            read_file("nonexistent.txt")
        mock_file.assert_called_once_with("nonexistent.txt", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="test\x00content")
    def test_read_file_non_printable_chars(self, mock_file):
        """Test handling of a file with non-printable characters."""
        # create a file with non-printable characters
        mock_data = "test\x00content"
        m = mock_open(read_data=mock_data)
        with patch("builtins.open", m):
            self.assertRaises(ValueError, read_file, "test.txt")


class TestScrapeUrl(unittest.TestCase):
    """Tests for the scrape_url function."""

    @patch("requests.get")
    def test_scrape_url_success(self, mock_get):
        """Test scraping a URL successfully."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <head>
                <title>Test Page</title>
                <style>body { color: red; }</style>
            </head>
            <body>
                <script>console.log('hello');</script>
                <div>Test Content</div>
                <p>  More  Content  </p>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        result = scrape_url("https://example.com")
        self.assertIn("Test Content", result)
        self.assertIn("More\nContent", result)
        self.assertNotIn("console.log", result)  # Script should be removed
        self.assertNotIn("color: red", result)  # Style should be removed
        mock_get.assert_called_once_with("https://example.com", timeout=30)

    @patch("requests.get", side_effect=Exception("Connection error"))
    def test_scrape_url_connection_error(self, mock_get):
        """Test handling of connection errors."""
        with self.assertRaises(Exception) as context:
            scrape_url("https://examlsdkjfoseoinsfbnple.com")
        self.assertIn("Error fetching URL", str(context.exception))
        mock_get.assert_called_once_with(
            "https://examlsdkjfoseoinsfbnple.com", timeout=30
        )


class TestReadContent(unittest.TestCase):
    """Tests for the read_content function."""

    def test_read_content_mixed_sources(self):
        """Test reading from mixed sources (files and URLs)."""

        p = os.getcwd()
        sources = [
            f"{p}/{project_prefix}/utils/file1.txt",
            "https://example.com",
        ]
        result = read_content(sources)

    def test_read_content_all_files(self):
        """Test reading from multiple files."""
        # Setup mocks
        p = os.getcwd()
        sources = [
            f"{p}/{project_prefix}/utils/file1.txt",
            f"{p}/{project_prefix}/utils/file2.txt",
        ]
        result = read_content(sources)

        self.assertEqual(result, ["file1 content", "file2 content"])

    def test_read_content_all_urls(self):
        """Test reading from multiple URLs."""

        sources = ["https://example.com", "https://example.org"]
        result = read_content(sources)
        self.assertIn("Example", result[0])
        self.assertIn("Example", result[1])


if __name__ == "__main__":
    unittest.main()
