from playwright.async_api import Playwright, async_playwright
from urllib import parse
from core import JobTypes


class EventFinder:
    def __init__(self, base_url, page_url):
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    async def find_events(self, job_type: JobTypes) -> None:
        if job_type == JobTypes.GUICHELIVE:
            async with async_playwright() as playwright:
                await self.find_links_in_guichelive(playwright)
        elif job_type == JobTypes.GUICHEWEB:
            # Implement find_in_guicheweb
            pass
        elif job_type == JobTypes.BALADAPP:
            # Implement find_in_baladapp
            pass
        else:
            raise ValueError(f"Unknown job type: {job_type}")

    async def find_links_in_guichelive(self, playwright: Playwright) -> None:
        try:
            browser = await playwright.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(self.base_url)
            await page.get_by_text("Aceitar Todos").click()
            await page.get_by_role("button", name="CARREGAR MAIS EVENTOS").click()
            anchors = await page.locator("a.text-reset").all()
            for a in anchors:
                value = await a.get_attribute("href")
                print(f"Found link: {value}")
                url = parse.urljoin(self.base_url, value)
                self.links.add(url)
            await browser.close()
        except Exception as e:
            self.error(f"Error in find_in_guichelive: {e}")
            return

    async def get_event_info(self, job_type: JobTypes, page_url: str) -> dict:
        if job_type == JobTypes.GUICHELIVE:
            async with async_playwright() as playwright:
                return await self.get_event_info_guichelive(playwright)
        elif job_type == JobTypes.GUICHEWEB:
            # Implement get_event_info_guicheweb
            pass
        elif job_type == JobTypes.BALADAPP:
            # Implement get_event_info_baladapp
            pass
        else:
            raise ValueError(f"Unknown job type: {job_type}")

    async def get_event_info_guichelive(self, playwright: Playwright) -> dict:
        try:
            browser = await playwright.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(self.base_url)
            await page.get_by_text("Aceitar Todos").click()
            await page.goto(self.page_url)
            name = (
                await page.locator("div#gw_cover>div>div>div>h2.notranslate")
                .nth(0)
                .inner_text()
            )
            date = await page.locator("div#gw_cover>div>div>div>h4").nth(0).inner_text()
            entrance_times_str = (
                await page.locator("div#gw_cover>div>div>div>h6").nth(0).inner_text()
            )
            venue = await page.locator("div#gw_cover>div>div>div>h5").nth(0).inner_text()
            service_fee = await page.locator("div#gw_cover>div>div>div>p>i>span").nth(0).inner_text()
            sections_top_list = await page.locator("div#exibe_ingressos>div>div>div>ul")
            tickets = set()
            for sect in sections_top_list.all():
                list_items = await sect.locator("li")
                # Review following code
                """ for item in list_items.all():
                    ticket_name = await item.locator("span").nth(0).inner_text()
                    ticket_price = await item.locator("span").nth(1).inner_text()
                    tickets.add(f"{ticket_name} - {ticket_price}") """


        except Exception as e:
            self.error(f"Error in get_event_info_guichelive: {e}")
            return {}

    def page_links(self) -> set:
        return self.links

    def error(self, message) -> None:
        print(f"Error parsing HTML: {message}")
        pass
