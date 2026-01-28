"""Pytest configuration and shared fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def data_path():
    """Return the path to the test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def get_data_file(data_path):
    """Return a function to get full path to a data file."""

    def _get_data_file(filename):
        return str(data_path / filename)

    return _get_data_file
