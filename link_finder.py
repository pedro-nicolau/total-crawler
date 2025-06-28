from playwright.async_api import Playwright, async_playwright
from urllib import parse

class LinkFinder():
    def __init__(self, base_url, page_url):
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    async def find_events_guichelive(self) -> None:
        async with async_playwright() as playwright:
            await self.find_in_guichelive(playwright)

    async def find_in_guichelive(self, playwright: Playwright) -> None:
        try:
            browser = await playwright.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://www.guichelive.com.br/")
            await page.get_by_text("Aceitar Todos").click()
            await page.get_by_role("button", name="CARREGAR MAIS EVENTOS").click()
            anchors = await page.locator('a.text-reset').all()
            for a in anchors:
                value = await a.get_attribute('href')
                print(f'Found link: {value}')
                url = parse.urljoin(self.base_url, value)
                self.links.add(url)
            await browser.close()
        except Exception as e:
            self.error(f'Error in find_in_guichelive: {e}')
            return

    def page_links(self) -> set:
        return self.links

    def error(self, message) -> None:
        print(f'Error parsing HTML: {message}')
        pass