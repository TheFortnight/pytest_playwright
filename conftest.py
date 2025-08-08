# conftest.py
import pytest

@pytest.fixture(scope="session")
def playwright_browser_launch_args(playwright_browser_launch_args):
    # disable the geolocation feature entirely in all browsers
    playwright_browser_launch_args["args"] = (
        playwright_browser_launch_args.get("args", [])
        + ["--disable-features=Geolocation"]
    )
    return playwright_browser_launch_args

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    • Never grant geolocation
    • Block service workers
    """
    # 1. Don’t grant any geolocation permission
    browser_context_args["permissions"] = []

    # 2. Block service workers so they can’t intercept requests
    browser_context_args["service_workers"] = "block"

    return browser_context_args

@pytest.fixture(autouse=True)
def disable_http_cache(page):
    """
    For every page, open a CDP session and disable the network cache.
    """
    cdp = page.context.new_cdp_session(page)
    cdp.send("Network.enable")
    cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
    yield
