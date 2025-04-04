"""
Pytest configuration for sqirvy_cli tests.
"""

import pytest
import sys
import os

# Add project root to the Python path so we can import the package
# This ensures tests can be run from any directory
@pytest.fixture(scope="session", autouse=True)
def setup_path():
    """Add project root to Python path."""
    # Get the project root directory
    project_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), 
            "..", 
            ".."
        )
    )
    
    # Add to Python path if not already there
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)