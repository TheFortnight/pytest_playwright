# tests/test_mock_by_location.py
import time, json
from playwright.sync_api import Page, Route, Request, expect

def test_mock_by_location(page: Page):
    

    def handle_about(route: Route):
        # Let real server answer the preflight
       # if request.method == "OPTIONS":
       #     return route.continue_()
        body = {
                "is_referrer": True,
                "is_referral": True,
                "has_linked_referral_code": True,
            }
        
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(body)
        )

    

    page.goto("https://phrm-16901.dev.portal.phrm.tech/?referral_code=48e9ad0a-0cd4-4e39-ba67-01781d8aabc5")
    #time.sleep(15)  # keep your timing

    codeInput = page.locator('.dialog .code-dialog__code-box input')
    codeInput.first.wait_for(state="visible")

    
    page.context.route(
            '**/api/api_254/marketing/referral/users/about',
            lambda route, request: handle_about(route)
        )  


        

    

    # enter the code (unchanged)
    codeInput.nth(0).fill('2')
    codeInput.nth(1).fill('5')
    codeInput.nth(2).fill('0')
    codeInput.nth(3).fill('8')
    codeInput.nth(4).type('1')  # use type() so key events fire if needed

    #time.sleep(15)  # unchanged
    expect(page.locator('body .dialog').first).to_be_visible(timeout=50000)
    expect(page.locator('.dia')).to_be_visible(timeout=50000)
    
