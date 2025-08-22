# conftest.py
import os
import pytest

# OPTIONAL: if you saved a state that clicks “Никогда не определять” once:
STATE_PATH = "state_never_allow.json"  # create with a one-time helper if you want

@pytest.fixture(scope="session")
def playwright_browser_launch_args(playwright_browser_launch_args):
    # Chromium: remove Geolocation feature entirely
    args = playwright_browser_launch_args.get("args", [])
    playwright_browser_launch_args["args"] = args + ["--disable-features=Geolocation"]
    return playwright_browser_launch_args

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # 1) Never grant geolocation permission
    browser_context_args["permissions"] = []

    # 2) Block service workers (prevents SW from intercepting/memoizing network)
    browser_context_args["service_workers"] = "block"

    # 3) (Optional) persist site choice “Never allow” across runs
    if os.path.exists(STATE_PATH):
        browser_context_args["storage_state"] = STATE_PATH

    return browser_context_args

@pytest.fixture(autouse=True)
def disable_http_cache(page, browser_name):
    """
    Disable browser cache for every test:
    - Chromium: real cache disable via CDP
    - Firefox/WebKit: force no-cache headers on all requests
    """
    if browser_name == "chromium":
        cdp = page.context.new_cdp_session(page)
        cdp.send("Network.enable")
        cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
        yield
        return

    def _no_cache(route, request):
        headers = dict(request.headers)
        headers["Cache-Control"] = "no-cache, no-store, max-age=0"
        headers["Pragma"] = "no-cache"
        headers["Expires"] = "0"
        route.continue_(headers=headers)

    page.context.route("**/*", _no_cache)
    try:
        yield
    finally:
        page.context.unroute("**/*", _no_cache)
