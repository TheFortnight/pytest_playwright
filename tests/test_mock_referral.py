# tests/test_mock_by_location.py
import time, json
from playwright.sync_api import Page, Route, Request, expect

def test_mock_by_location(page: Page):
    pattern = "**/api/api_254/marketing/referral/users/about*"

    # OFF initially: earlier /about calls pass through
    mock_active = {"on": False}

    def handle_about(route: Route, request: Request):
        # ---- PRE-FLIGHT (OPTIONS) ----
        if request.method == "OPTIONS":
            # Playwright normalizes header names to lowercase
            origin      = request.headers.get("origin", "*")
            acr_method  = request.headers.get("access-control-request-method", "GET")
            acr_headers = request.headers.get("access-control-request-headers", "")
            return route.fulfill(
                status=204,
                headers={
                    "Access-Control-Allow-Origin": origin,
                    "Access-Control-Allow-Methods": acr_method,
                    "Access-Control-Allow-Headers": acr_headers,
                    "Access-Control-Max-Age": "600",
                    # If your fetch sends cookies/credentials, echo the origin and add:
                    # "Access-Control-Allow-Credentials": "true",
                    "Vary": "Origin",
                },
            )

        # ---- AFTER ACTIVATION -> FULFILL THE REAL GET ----
        if mock_active["on"] and request.method == "GET":
            origin = request.headers.get("origin", "*")
            body = {
                "is_referrer": False,
                "is_referral": True,
                "has_linked_referral_code": True,
            }
            return route.fulfill(
                status=200,
                content_type="application/json",
                headers={
                    "Access-Control-Allow-Origin": origin,
                    # If credentials are in use, also:
                    # "Access-Control-Allow-Credentials": "true",
                    "Vary": "Origin",
                },
                body=json.dumps(body),
            )

        # ---- BEFORE ACTIVATION (or non-GET) -> PASS THROUGH ----
        route.continue_()

    # One route for both OPTIONS and GET (order-safe)
    page.context.route(pattern, handle_about)

    page.goto("https://phrm-16901.dev.portal.phrm.tech/?referral_code=48e9ad0a-0cd4-4e39-ba67-01781d8aabc5")

    # keep your timing
    time.sleep(35)

    # flip ON only after the input exists
    codeInput = page.locator('.dialog .code-dialog__code-box input')
    codeInput.first.wait_for(state="visible")
    mock_active["on"] = True  # <— now the *last four* (and any later) /about reqs will be mocked

    # type your code (unchanged style)
    codeInput.nth(0).fill('2')
    codeInput.nth(1).fill('5')
    codeInput.nth(2).fill('0')
    codeInput.nth(3).fill('8')
    codeInput.nth(4).fill('1')

    time.sleep(160)  # unchanged
    expect(page.locator('.dialog')).to_be_visible()
