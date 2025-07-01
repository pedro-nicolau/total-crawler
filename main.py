from queue import Queue
from crawler import Crawler
from domain import *

PROJECT_NAME = "guichelive"
HOMEPAGE = "https://www.guichelive.com.br/"
EVENTO_TESTE = "https://www.guichelive.com.br/chitaozinho-e-xororo-campinas_41511"
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + "/queue.txt"
CRAWLED_FILE = PROJECT_NAME + "/crawled.txt"
NUMBER_OF_THREADS = 1
# queue = Queue()
entry = Crawler(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
entry.crawl_first_page('1st', HOMEPAGE)
entry.crawl_page('1st', EVENTO_TESTE)