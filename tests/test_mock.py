# tests/test_mock_by_location.py
import time
import json
from playwright.sync_api import Page, Route, expect

def test_mock_by_location(page: Page):
    # 1. Register the mock before any navigation or clicks
    def handle_route(route: Route):

        mock_body = {
        "pagination": {
            "count": 5,
            "total_count": 30,
            "page": 1,
            "total_pages": 3,
            "next_page": {
                "page": 2,
                "take": 10,
                "skip": 10
            }
        },
        "elements": [
            {
                "id": 7861,
                "title": "MOCK!!!",
                "location": {
                    "full_address": "г. Москва, ул. Маршала Бирюзова, 16",
                    "short_address": "г. Москва, ул. Маршала Бирюзова, 16",
                    "region": "г. Москва",
                    "area": "",
                    "city": "г. Москва",
                    "city_district": "",
                    "settlement": None,
                    "street": "ул. Маршала Бирюзова",
                    "house": "16",
                    "block": "",
                    "entrance": "",
                    "floor": "",
                    "flat": "",
                    "office": "",
                    "metro": None,
                    "index": "",
                    "latitude": 55.79491,
                    "longitude": 37.491789
                },
                "schedule": {
                    "is_simple": True,
                    "timezone": "Europe/Moscow",
                    "weekly": {
                        "is_working_only_on_weekdays": False,
                        "is_working_day_and_night": True,
                        "is_working_without_lunch": True,
                        "lunch_start_at": 0,
                        "lunch_end_at": 0,
                        "working_start_at": 0,
                        "working_end_at": 1439
                    },
                    "sunday": {
                        "is_working_day_and_night": True,
                        "is_working_without_lunch": True,
                        "is_day_off": False,
                        "lunch_start_at": 0,
                        "lunch_end_at": 0,
                        "working_start_at": 0,
                        "working_end_at": 1439
                    },
                    "monday": {
                        "is_working_day_and_night": True,
                        "is_working_without_lunch": True,
                        "is_day_off": False,
                        "lunch_start_at": 0,
                        "lunch_end_at": 0,
                        "working_start_at": 0,
                        "working_end_at": 1439
                    },
                    "tuesday": {
                        "is_working_day_and_night": True,
                        "is_working_without_lunch": True,
                        "is_day_off": False,
                        "lunch_start_at": 0,
                        "lunch_end_at": 0,
                        "working_start_at": 0,
                        "working_end_at": 1439
                    },
                    "wednesday": {
                        "is_working_day_and_night": True,
                        "is_working_without_lunch": True,
                        "is_day_off": False,
                        "lunch_start_at": 0,
                        "lunch_end_at": 0,
                        "working_start_at": 0,
                        "working_end_at": 1439
                    },
                    "thursday": {
                        "is_working_day_and_night": True,
                        "is_working_without_lunch": True,
                        "is_day_off": False,
                        "lunch_start_at": 0,
                        "lunch_end_at": 0,
                        "working_start_at": 0,
                        "working_end_at": 1439
                    },
                    "friday": {
                        "is_working_day_and_night": True,
                        "is_working_without_lunch": True,
                        "is_day_off": False,
                        "lunch_start_at": 0,
                        "lunch_end_at": 0,
                        "working_start_at": 0,
                        "working_end_at": 1439
                    },
                    "saturday": {
                        "is_working_day_and_night": True,
                        "is_working_without_lunch": True,
                        "is_day_off": False,
                        "lunch_start_at": 0,
                        "lunch_end_at": 0,
                        "working_start_at": 0,
                        "working_end_at": 1439
                    },
                    "days_off": []
                },
                "contacts": {
                    "emails": [],
                    "phones": [],
                    "links": []
                },
                "booking": {
                    "maximum_booking_time_in_minutes": 2880,
                    "maximum_booking_time_from_next_day_in_minutes": 0
                },
                "possibilities": {
                    "has_cash_payment": False,
                    "has_card_payment": False
                },
                "images": {
                    "main": None,
                    "other": []
                },
                "branding": {
                    "logo": (
                        "https://cdn.phrm.tech:443/files/b08fa833-d1dc-4095-8793-"
                        "02a504a4feca.png?file_id=12747210&hash=0D90AE2178FE11E5A45"
                        "BC2B530D7C967&min_width=50&max_width=2800&min_height=50&max_"
                        "height=2800&min_pixel_ratio=1&max_pixel_ratio=4&formats=png%2cwebp"
                    )
                }
            }
        ]
    }

        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_body)
        )

    page.context.route(
        "**/api/api_240/partners/pharmacies/by_location/**",
        lambda route, request: handle_route(route)
    )

    # 2. Navigate and click, *waiting* for the mocked network call
    
    with page.expect_response("**/api/api_240/partners/pharmacies/by_location/**") as resp_info:
        page.goto("https://staging.portal.phrm.tech/pharmacies")
       # page.get_by_role("link", name="Аптеки").click()

    # 3. Assert that the response came from our mock
    time.sleep(5)  # Optional: wait to visually confirm the mock is displayed
    response = resp_info.value
    assert response.status == 200
    data = response.json()
    assert data["elements"][0]["title"] == "MOCK!!!"

    # 4. Wait for your UI to show the mocked data
    #    (adjust selector to whatever your app renders)
    
    expect(page.get_by_text("MOCK!!!")).to_be_visible()
    
