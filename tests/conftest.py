import pytest
from playwright.sync_api import Browser

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "permissions": ["geolocation"],
        "geolocation": {"latitude": 37.7749, "longitude": -122.4194},  # San Francisco
        "locale": "id-ID",
    }