import os

# Core functionality for the web crawler
class Core:
    queue = ''
    crawled = ''
    def __init__(self):
        Core.queue = ''
        Core.crawled = ''

    # Each website you crawl is a separate project (folder)
    @staticmethod
    def create_project_dir(directory):
        if not os.path.exists(directory):
            print('Creating project ' + directory)
            os.makedirs(directory)

    # Create queue and crawled files (if not created)
    @staticmethod
    def create_data_files(project_name = '', base_url = ''):
        Core.queue = project_name + '/queue.txt'
        Core.crawled = project_name + '/crawled.txt'
        # Always write the homepage to the queue file if it is empty
        if not os.path.isfile(Core.queue) or os.path.getsize(Core.queue) == 0:
            Core.write_file(Core.queue, base_url)
        if not os.path.isfile(Core.crawled):
            Core.write_file(Core.crawled, '')

    # Write to a file
    # 'data' is a string, 'path' is the file path
    @staticmethod
    def write_file(path, data):
        with open(path, 'wt') as f:
            f.write(data)
            f.close()

    # Append data to a file
    # 'data' is a string, 'path' is the file path
    # This function appends data to the end of the file, creating it if it doesn't exist
    @staticmethod
    def append_to_file(path, data):
        with open(path, 'at') as f:
            f.write(data + '\n')
            f.close()

    # Delete file contents
    @staticmethod
    def delete_file_contents(path):
        with open(path, 'wt') as f:
            f.write('')
            f.close()

    # Read a file and convert each line to a set of items
    @staticmethod
    def file_to_set(file_name):
        results = set()
        with open(file_name, 'rt') as f:
            for line in f:
                results.add(line.replace('\n', ''))
            f.close()
        return results

    # Iterate through a set of items and add each to a file
    @staticmethod
    def set_to_file(links, file_name):
        with open(file_name, 'wt') as f:
            for link in sorted(links):
                f.write(link + '\n')
            f.close()