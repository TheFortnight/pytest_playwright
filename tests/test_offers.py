import re
import pytest
import time
from playwright.sync_api import Page, Error

def test_example(page: Page) -> None:
    # 1. (Optional) explicitly revoke any granted permission
    #    In Playwright, permissions are only granted if you call grant_permissions(),
    #    so you don’t need to revoke—but you can be explicit:
    page.context.grant_permissions([], origin="https://staging.portal.phrm.tech/catalog/antibiotiki")

    # 2. Navigate
    page.goto("https://staging.portal.phrm.tech/catalog/antibiotiki")

    # 3. Try to get geolocation, catch the PERMISSION_DENIED error
    error_code = page.evaluate(
        """() => new Promise(resolve => {
             navigator.geolocation.getCurrentPosition(
               () => resolve('OK'),
               e => resolve(e.code)    // code === 1 for PERMISSION_DENIED
             );
           })"""
    )
    # PERMISSION_DENIED has code = 1
    assert error_code == 1

    # 4. Now your site flow:
    page.get_by_role("link", name=" в 1070 аптеках ").click()
    page.get_by_role("button", name="Списком").click()
    time.sleep(100)
    
