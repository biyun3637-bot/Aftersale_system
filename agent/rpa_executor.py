"""RPA execution node. Uses Playwright + system Chrome."""

import asyncio, os as _o

from typing import Optional



class RpaResult:

    def __init__(self):

        self.success = False

        self.screenshot_path = None

        self.extracted_data = {}

        self.error = ""



def get_default_mock_data(order_id):

    r = RpaResult()

    r.success = True

    r.extracted_data = {
        "order_id": order_id,
        "tracking_number": "RPA-TRAC-001",
        "status": "In Transit",
    }

    return r



def _mock_page():

    base = _o.path.dirname(_o.path.abspath(__file__))

    return _o.path.abspath(_o.path.join(

        base, "..", "rpa", "mock_pages", "shopify_order.html"))



async def execute_rpa(order_id, page_path=""):

    result = RpaResult()

    base = _o.path.dirname(_o.path.abspath(__file__))

    ss_dir = _o.path.join(base, "..", "static")

    _o.makedirs(ss_dir, exist_ok=True)

    try:

        from playwright.async_api import async_playwright

        async with async_playwright() as p:

            browser = await p.chromium.launch(channel="chrome", headless=True)

            page = await browser.new_page()

            target = page_path or _mock_page()

            url = "file:///" + _o.path.abspath(target).replace("\\", "/")

            await page.goto(url, timeout=15000)

            await page.wait_for_selector("#order-id", timeout=10000)

            async def _g(s): el = await page.query_selector(s); return await el.inner_text() if el else ""

            result.extracted_data["order_id"] = await _g("#order-id")

            result.extracted_data["tracking_number"] = await _g("#tracking-number")

            result.extracted_data["status"] = await _g("#order-status")

            ss = _o.path.join(ss_dir, "rpa_" + order_id + ".png")

            await page.screenshot(path=ss, full_page=True)

            result.screenshot_path = ss

            await browser.close()

            result.success = True

    except Exception as e:

        result.error = str(e)

    return result