import re
import pytest
import time
from playwright.sync_api import Page, Error

def test_example(page: Page) -> None:
    
    page.set_viewport_size({"width": 450, "height": 600})  # Overrides default
    page.context.grant_permissions([], origin="https://staging.portal.phrm.tech/catalog/antibiotiki")
    page.context.grant_permissions([], origin="https://expero.ru/catalog/antibiotiki")

    # 2. Navigate
    page.goto("https://expero.ru/catalog/antibiotiki")
    
    page.locator('body .gtm-points_of_sale').nth(0).click()
    #time.sleep(5)
    page.get_by_role("button", name=" Круглосуточные ").click()
    time.sleep(10)
    
