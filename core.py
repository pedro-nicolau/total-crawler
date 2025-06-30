import os
import json
from enum import Enum

class JobTypes(Enum):
    GUICHELIVE = 'guichelive'
    GUICHEWEB = 'guicheweb'
    BALADAPP = 'baladapp'

# Core functionality for the web crawler
class Core:
    queue = ''
    crawled = ''
    events = ''
    # Initialize the core functionality
    def __init__(self):
        Core.queue = ''
        Core.crawled = ''
        Core.events = ''
    
    # Append data to a file
    # 'data' is a string, 'path' is the file path
    # This function appends data to the end of the file, creating it if it doesn't exist
    @staticmethod
    def append_to_file(path: str, data: str) -> None:
        with open(path, 'at') as f:
            f.write(data + '\n')
            f.close()

    # Create queue and crawled files (if not created)
    @staticmethod
    def create_data_files(project_name: str = '', base_url: str = '') -> None:
        Core.queue = project_name + '/queue.txt'
        Core.crawled = project_name + '/crawled.txt'
        Core.events = project_name + '/events.json'
        # Always write the homepage to the queue file if it is empty
        if not os.path.isfile(Core.queue) or os.path.getsize(Core.queue) == 0:
            Core.write_file(Core.queue, base_url)
            print(f'Created queue file: {Core.queue} with base URL: {base_url}')
        if not os.path.isfile(Core.crawled) or os.path.getsize(Core.crawled) == 0:
            Core.write_file(Core.crawled, '')
            print(f'Created crawled file: {Core.crawled}')
        if not os.path.isfile(Core.events) or os.path.getsize(Core.events) == 0:
            Core.write_file(Core.events, '')
            print(f'Created events file: {Core.events}')
    
    # Each website you crawl is a separate project (folder)
    @staticmethod
    def create_project_dir(directory: str) -> None:
        if not os.path.exists(directory):
            print('Creating project ' + directory)
            os.makedirs(directory)
        else:
            print('Project ' + directory + ' already exists')

    # Delete file contents
    @staticmethod
    def delete_file_contents(path: str) -> None:
        with open(path, 'wt') as f:
            f.write('')
            f.close()
    
    # Convert a dictionary to a file
    # 'events' is a dictionary, 'file_name' is the file path
    @staticmethod
    def dict_to_file(events: dict, file_name: str) -> None:
        with open(file_name, 'w') as f:
            json.dump(events, f, indent=4)
            f.close()

    # Read a file and convert each line to a set of items
    @staticmethod
    def file_to_set(file_name: str) -> set:
        results = set()
        with open(file_name, 'rt') as f:
            for line in f:
                results.add(line.replace('\n', ''))
            f.close()
        return results
    
    # Read a json file and convert it to a dictionary
    # 'file_name' is the path to the json file
    @staticmethod
    def file_to_dict(file_name: str) -> dict:
        results = {}
        with open(file_name, 'r') as f:
            results = json.load(f)
            f.close()
        return results

    # Iterate through a set of items and add each to a file
    @staticmethod
    def set_to_file(links: str, file_name: str) -> None:
        with open(file_name, 'wt') as f:
            for link in sorted(links):
                f.write(link + '\n')
            f.close()
    
    # Write to a file
    # 'data' is a string, 'path' is the file path
    @staticmethod
    def write_file(path: str, data: str) -> None:
        with open(path, 'wt') as f:
            f.write(data)
            f.close()