# conftest.py
import pytest

@pytest.fixture(autouse=True)
def disable_http_cache(page, browser_name):
    """
    Disable browser cache for every test.
    - Chromium: via CDP (true cache disable)
    - Firefox/WebKit: add request headers to force revalidation/no-store
    """
    if browser_name == "chromium":
        cdp = page.context.new_cdp_session(page)
        cdp.send("Network.enable")
        cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
        yield
        return

    # For firefox/webkit: install a catch-all route that adds no-cache headers
    def _no_cache(route, request):
        headers = dict(request.headers)
        headers["Cache-Control"] = "no-cache, no-store, max-age=0"
        headers["Pragma"] = "no-cache"
        headers["Expires"] = "0"
        route.continue_(headers=headers)

    # Register AFTER your specific mocks so it acts as a fallback
    page.context.route("**/*", _no_cache)
    try:
        yield
    finally:
        page.context.unroute("**/*", _no_cache)
