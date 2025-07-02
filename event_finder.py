from playwright.async_api import Playwright, async_playwright
from urllib import parse
from core import *


class EventFinder:
    DEFAULT_TIMEOUT = 45000
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
            self.error(f"Error in find_links_in_guichelive: {e}")
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
            page.set_default_timeout(EventFinder.DEFAULT_TIMEOUT)
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
            venue = (
                await page.locator("div#gw_cover>div>div>div>h5").nth(0).inner_text()
            )
            service_fee = (
                await page.locator("div#gw_cover>div>div>div>p>i>span")
                .nth(0)
                .inner_text()
            )
            sections_top_list = page.locator("div#exibe_ingressos>div>div>div>ul")
            tickets = list()
            sections = list()
            for sect in await sections_top_list.all():
                list_items = sect.locator("li")
                await list_items.nth(0).click()  # Click to expand section
                for item in range(
                    1, await list_items.count()
                ):  # Skip the first item which is the section header
                    ticket_info_str = await list_items.nth(item).locator("div>div").nth(0).inner_text()
                    ticket_info = Core.split_ticket_infos(ticket_info_str)
                    price = Core.get_price_info(
                        ticket_info[ticket_info.index("Valor:") + 1]
                        if "Valor:" in ticket_info
                        else ""
                    )
                    tickets.append(
                        {
                            "name": (
                                ticket_info[ticket_info.index("Ingresso:") + 1]
                                if "Ingresso:" in ticket_info
                                else ""
                            ),
                            "batch": (
                                ticket_info[ticket_info.index("Lote:") + 1]
                                if "Lote:" in ticket_info
                                else ""
                            ),
                            "price_str": (
                                ticket_info[ticket_info.index("Valor:") + 1]
                                if "Valor:" in ticket_info
                                else ""
                            ),
                            "price": price["price"],
                            "currency": price["currency"],
                            "observation": price["observation"],
                        }
                    )
                section_name = await sect.locator("li>div>h5>b").nth(0).inner_text()
                section_description = (
                    await sect.locator("li>div>h6").nth(0).inner_text()
                    if await sect.locator("li>div>h6").count() > 0
                    else "n/a"
                )
                sections.append(
                    {
                        "name": section_name,
                        "description": section_description,
                        "tickets": tickets,
                    }
                )
            event = {
                Core.get_timestamp(): {
                    "name": name,
                    "date": date,
                    "entrance_times": entrance_times_str,
                    "venue": venue,
                    "service_fee": service_fee,
                    "sections": sections,
                }
            }
            await browser.close()
            return event
        except Exception as e:
            self.error(f"Error in get_event_info_guichelive: {e}")
            return {}

    def page_links(self) -> set:
        return self.links

    def error(self, message) -> None:
        print(f"Error parsing HTML: {message}")
        pass
