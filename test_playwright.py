import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        print("正在打开页面...")
        await page.goto("https://example.com")
        print("标题:", await page.title())
        await page.screenshot(path="example.png")
        print("截图已保存")
        await page.wait_for_timeout(3000)
        await browser.close()
        print("完成")


asyncio.run(main())
