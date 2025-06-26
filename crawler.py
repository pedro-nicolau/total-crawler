from urllib.request import urlopen
from link_finder import LinkFinder
from core import Core

# Crawler class to manage the crawling process
# It initializes the project, manages the queue and crawled URLs, and handles the crawling logic
class Crawler:
    # Class variables to store project details and state
    base_url = ''
    core = None
    crawled_file = ''
    domain_name = ''
    project_name = ''
    queue_file = ''
    crawled = set()  # Set to store URLs that have been crawled
    queue = set()  # Set to store URLs to be crawled'

    # Initialize the Crawler with project name, base URL, and domain name
    # This method sets up the core functionality and initializes the project directories and files
    def __init__(self, project_name, base_url, domain_name):
        Crawler.core = Core()
        Crawler.project_name = project_name
        Crawler.base_url = base_url
        Crawler.domain_name = domain_name
        Crawler.queue_file = f'{project_name}/queue.txt'
        Crawler.crawled_file = f'{Crawler.project_name}/crawled.txt'
        self.boot()

    # Initialize the crawler by creating project directories and files
    # This method is called when the crawler is instantiated
    def boot(self):
        Crawler.core.create_project_dir(self.project_name)
        Crawler.core.create_data_files(self.project_name, self.base_url)
        Crawler.queue = self.core.file_to_set(self.queue_file)
        Crawler.crawled = self.core.file_to_set(self.crawled_file)

    # This method is called to start the crawling process
    def crawl_page(self, thread_name, page_url):
        if page_url not in Crawler.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Crawler.queue)) + ' | Crawled ' + str(len(Crawler.crawled)))
            self.add_links_to_queue(Crawler.gather_links(page_url))
            Crawler.queue.remove(page_url)
            Crawler.crawled.add(page_url)
            self.update_files()

    # This method gathers links from a given page URL
    # It uses the LinkFinder class to parse the HTML and extract links
    def gather_links(self, page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode('utf-8')
            finder = LinkFinder(self.base_url, page_url)
            finder.feed(html_string)
            return finder.page_links()
        except Exception as e:
            print(f'Error: {e}')
            return set()

    # This method adds links to the queue if they are not already present
    # It checks against both the queue and crawled sets to avoid duplicates
    def add_links_to_queue(self, links):
        for link in links:
            if link not in self.queue and link not in self.crawled:
                Crawler.queue.add(link)
                Crawler.core.append_to_file(self.queue_file, link)

    # This method adds links to the queue, ensuring they are valid and not duplicates
    def add_links_to_queue(self, links):
        for url in links:
            if url in Crawler.queue:
                continue
            if url in Crawler.crawled:
                continue
            if Crawler.domain_name not in url:
                continue
            Crawler.queue.add(url)
    
    # This method updates the queue and crawled files with the current state of the sets
    # It writes the contents of the queue and crawled sets to their respective files
    def update_files(self):
        Crawler.core.set_to_file(Crawler.queue, Crawler.queue_file)
        Crawler.core.set_to_file(Crawler.crawled, Crawler.crawled_file)
        print('Files updated: Queue and Crawled')