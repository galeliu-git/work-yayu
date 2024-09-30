import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.zhipin.com/")
    page.goto("https://www.zhipin.com/chengdu/?seoRefer=index")
    page.get_by_placeholder("搜索职位、公司").click()
    page.get_by_placeholder("搜索职位、公司").fill("贷款")
    page.get_by_placeholder("搜索职位、公司").press("Enter")
    page.get_by_role("link", name="").click()
    page.get_by_role("link", name="").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
