import asyncio
from core import *
from event_finder import EventFinder
from urllib.parse import urlparse


# Crawler class to manage the crawling process
# It initializes the project, manages the queue and crawled URLs, and handles the crawling logic
class Crawler:
    # Class variables to store project details and state
    ### These variables are shared across all instances of the Crawler class
    base_url = ""
    core = Core
    crawled_file = ""
    domain_name = ""
    events_file = ""
    project_name = ""
    queue_file = ""
    crawled = set()  # Set to store URLs that have been crawled
    queue = set()  # Set to store URLs to be crawled'
    events = {}  # Dictionary to store events found during crawling

    # Initialize the Crawler with project name, base URL, and domain name
    # This method sets up the core functionality and initializes the project directories and files
    def __init__(self, project_name: str, base_url: str, domain_name: str):
        Crawler.core = Core()
        Crawler.project_name = project_name
        Crawler.base_url = base_url
        Crawler.domain_name = domain_name
        Crawler.queue_file = f"{Crawler.project_name}/queue.txt"
        Crawler.crawled_file = f"{Crawler.project_name}/crawled.txt"
        Crawler.events_file = f"{Crawler.project_name}/events.json"
        self._boot()

    # Initialize the crawler by creating project directories and files
    # This method is called when the crawler is instantiated
    def _boot(self) -> None:
        Crawler.core.create_project_dir(self.project_name)
        Crawler.core.create_data_files(self.project_name, self.base_url)
        Crawler.queue = self.core.file_to_set(self.queue_file)
        Crawler.crawled = self.core.file_to_set(self.crawled_file)

    @staticmethod
    def add_event_to_events(event: dict) -> None:
        if event:
            for k in event:
                Crawler.events[k] = event[k]

    # This method adds links to the queue, ensuring they are valid and not duplicates
    # It checks against both the queue and crawled sets to avoid duplicates
    @staticmethod
    def add_links_to_queue(links: set) -> None:
        for url in links:
            if url in Crawler.queue:
                continue
            if url in Crawler.crawled:
                continue
            # Parse the netloc of the URL and compare with the domain name
            try:
                netloc = urlparse(url).netloc
                # Remove 'www.' prefix for comparison
                netloc = netloc.replace("www.", "")
                domain = Crawler.domain_name.replace("www.", "")
                if not netloc.endswith(domain):
                    continue
            except Exception:
                continue
            Crawler.queue.add(url)
            Crawler.core.append_to_file(Crawler.queue_file, url)

    # This method is called to start the crawling process 
    # It processes the queue, gathers event links from first page, and store links in the queue
    @staticmethod
    def crawl_first_page(thread_name: str, page_url: str) -> None:
        if page_url not in Crawler.crawled:
            print(thread_name + " now crawling " + page_url)
            print(
                "Queue "
                + str(len(Crawler.queue))
                + " | Crawled "
                + str(len(Crawler.crawled))
            )
            links = asyncio.run(Crawler.gather_links(page_url))
            print(f"Found {len(links)} links on {page_url}")
            Crawler.add_links_to_queue(links)
            Crawler.queue.remove(page_url)
            Crawler.crawled.add(page_url)
            Crawler.update_files()

    # This method is called to crawl a specific page URL
    # It retrieves the event information from the page and updates the crawled and queue sets also the events dictionary
    # It uses the EventFinder class to parse the HTML and extract event details
    @staticmethod
    def crawl_page(thread_name: str, page_url: str) -> None:
        if page_url not in Crawler.crawled:
            print(thread_name + " now crawling " + page_url)
            print(
                "Queue "
                + str(len(Crawler.queue))
                + " | Crawled "
                + str(len(Crawler.crawled))
            )
            event = asyncio.run(Crawler.get_event(JobTypes.GUICHELIVE, page_url))
            Crawler.add_event_to_events(event)
            Crawler.queue.remove(page_url)
            Crawler.crawled.add(page_url)
            Crawler.update_files(True)

    # This method gathers links from a given page URL
    # It uses the EventFinder class to parse the HTML and extract links
    @staticmethod
    async def gather_links(page_url: str) -> set:
        try:
            finder = EventFinder(Crawler.base_url, page_url)
            await finder.find_events(JobTypes.GUICHELIVE)
            return finder.page_links()
        except Exception as e:
            print(f"Error (gather_links): {e}")
            return set()

    # This method retrieves event information from a given page URL
    # It uses the EventFinder class to parse the HTML and extract event details
    @staticmethod
    async def get_event(job_type: JobTypes, page_url: str) -> dict:
        try:
            finder = EventFinder(Crawler.base_url, page_url)
            return await finder.get_event_info(job_type, page_url)
        except Exception as e:
            print(f"Error (get_event): {e}")
            return dict()

    # This method updates the queue and crawled files with the current state of the sets
    # It writes the contents of the queue and crawled sets to their respective files
    @staticmethod
    def update_files(has_event: bool = False) -> None:
        Crawler.core.set_to_file(Crawler.queue, Crawler.queue_file)
        Crawler.core.set_to_file(Crawler.crawled, Crawler.crawled_file)
        if has_event:
            Crawler.core.dict_to_file(Crawler.events, Crawler.events_file)
            print("Files updated: Queue, Crawled and Events")
            return
        print("Files updated: Queue and Crawled")
