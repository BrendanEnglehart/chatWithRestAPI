"""
Base testing module
"""

from flask import Flask
import pytest


@pytest.fixture
def app():
    """Creates and configures a new Flask application instance for each test."""
    application = Flask(__name__)
    application.config.update(
        {
            "TESTING": True,  # Enables better error reporting during tests
        }
    )
    yield application
