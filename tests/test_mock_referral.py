# tests/test_mock_by_location.py
import time, json
from playwright.sync_api import Page, Route, Request, expect

def test_mock_by_location(page: Page):
    pattern = "**/api/api_254/marketing/referral/users/about"

    page.goto("https://phrm-16901.dev.portal.phrm.tech/?referral_code=48e9ad0a-0cd4-4e39-ba67-01781d8aabc5")
    time.sleep(20)  # keep your timing

    codeInput = page.locator('.dialog .code-dialog__code-box input')
    codeInput.first.wait_for(state="visible")

    # --- register AFTER the field appears, on the PAGE (not context) ---
    def handle_about(route: Route, request: Request):
        # Let real server answer the preflight
        if request.method == "OPTIONS":
            return route.continue_()

        # Mock only GET (the actual call)
        if request.method == "GET":
            origin = request.headers.get("origin") or "https://phrm-16901.dev.portal.phrm.tech"
            body = {
                "is_referrer": True,
                "is_referral": True,
                "has_linked_referral_code": True,
            }
            body_str = json.dumps(body)
            return route.fulfill(
                status=500,
                content_type="application/json; charset=utf-8",
                headers={
                    # CORS for credentialed requests
                    "Access-Control-Allow-Origin": origin,
                    "Access-Control-Allow-Credentials": "true",
                    "Vary": "Origin",
                    # (optional) expose headers if your client reads them
                    # "Access-Control-Expose-Headers": "mds-protocol-version,trace-id",
                    "Content-Length": str(len(body_str)),  # some stacks expect it
                },
                body=body_str,
            )

        # Anything else just goes through
        route.continue_()

    page.route(pattern, handle_about)  # <-- page-level, registered late

    # enter the code (unchanged)
    codeInput.nth(0).fill('2')
    codeInput.nth(1).fill('5')
    codeInput.nth(2).fill('0')
    codeInput.nth(3).fill('8')
    codeInput.nth(4).type('1')  # use type() so key events fire if needed

    time.sleep(160)  # unchanged
    expect(page.locator('.dialog')).to_be_visible()
