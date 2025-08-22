# tests/test_mock_by_location.py
import time
import json
from playwright.sync_api import Page, Route, expect

def test_mock_by_location(page: Page):
    # 1. Register the mock before any navigation or clicks
    def handle_route(route: Route):

        mock_body = {"is_referrer":False,"is_referral":True,"has_linked_referral_code":False}

        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_body)
        )

    page.context.route(
        "**/api/api_254/marketing/referral/users/about",
        lambda route, request: handle_route(route)
    )

    # 2. Navigate and click, *waiting* for the mocked network call
    
    with page.expect_response("**/api/api_254/marketing/referral/users/about") as resp_info:
        page.goto("https://phrm-16544.dev.portal.phrm.tech/")
       # page.get_by_role("link", name="Аптеки").click()

    # 3. Assert that the response came from our mock
    time.sleep(60)  # Optional: wait to visually confirm the mock is displayed
    response = resp_info.value
    assert response.status == 200
    data = response.json()
    #assert data["elements"][0]["title"] == "MOCK!!!"

    # 4. Wait for your UI to show the mocked data
    #    (adjust selector to whatever your app renders)
    
    expect(page.locator('.dialog')).to_be_visible()
    
