import threading
from queue import Queue
from crawler import Crawler
from core import PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, NUMBER_OF_THREADS

queue = Queue()
ant = Crawler(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Initialize the crawler with the project name, homepage, and domain name and gather the first page links
ant.crawl_first_page('Entry ant', HOMEPAGE)

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Each queued link is a new job
def create_jobs():
    for link in ant.queue:
        queue.put(link)
    queue.join()
    crawl()

# Check if there are items in the queue and crawl
def crawl():
    queued_links = ant.queue.copy()
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        ant.crawl_page(threading.current_thread().name, url)
        queue.task_done()


create_workers()
crawl()