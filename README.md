# total-crawler
Web crawler for events in other ticket stands websites

## Installation instructions

To run the application locally first install the dependencies:
- Playwright

```bash
 pip install playwright
 playwright install
```

Run the application with:

- Windows:
```bash
& C:/Users/{username}/AppData/Local/Python/pythoncore-{3.14-64 or your version}/python.exe "{installation directory path}/total-crawler/main.py"
```

- Linux, MacOS, and other Unix-like systems:
```bash
& /usr/bin/python3 "{installation directory path}/total-crawler/main.py"
```

## Usage

> **Observation:**  
> This project is currently a Proof of Concept (POC) and has not been officially released. It is intended for experimental and demonstration purposes only. Features and functionality may change significantly before a stable release.  
>  
> **Recommended version:**  
> Python 3.14 or later is recommended for optimal performance and compatibility with the latest features.
>
> **Note:**
> Ensure you have the appropriate permissions to access the target websites. Excessive or unauthorized crawling may violate the terms of service of some sites. Always use this tool responsibly and in compliance with applicable laws and website policies.
>
The application is designed to crawl various ticketing websites to gather event information. Although it currently only supports one.

### Project Structure
- `main.py`: The main entry point for the application.
- `crawler.py`: Contains the logic for crawling and scraping event data.
- `core.py`: Common functions and configuration settings for the crawler, including target URLs and scraping parameters setup:
    - `PROJECT_NAME`: Project and directory name.
    - `HOMEPAGE`: The homepage URL of the target website.
    - `DOMAIN_NAME`: The domain name of the target website.
    - `QUEUE_FILE`: The file to store the URLs to be crawled.
    - `CRAWLED_FILE`: The file to store the URLs that have been crawled.
    - `NUMBER_OF_THREADS`: The number of threads to use for concurrent crawling.
- `event_finder.py`: Contains the logic for finding and extracting event links from the target website and scraping events data from those links.
- `config.json`: Configuration file for global settings, including project name, homepage list, queue and crawled default file names, and number of threads.
- `domain.py`: Contains utility functions for domain name extraction and validation.
