import os

# Core functionality for the web crawler
class Core:
    def __init__(self):
        pass
    # Each website you crawl is a separate project (folder)
    def create_project_dir(directory):
        if not os.path.exists(directory):
            print('Creating project ' + directory)
            os.makedirs(directory)

    # Create queue and crawled files (if not created)
    def create_data_files(self, project_name = '', base_url = ''):
        queue = project_name + '/queue.txt'
        crawled = project_name + '/crawled.txt'
        if not os.path.isfile(queue):
            self.write_file(queue, base_url)
        if not os.path.isfile(crawled):
            self.write_file(crawled, '')

    # Write to a file
    # 'data' is a string, 'path' is the file path
    def write_file(path, data):
        with open(path, 'wt') as f:
            f.write(data)
            f.close()

    # Append data to a file
    # 'data' is a string, 'path' is the file path
    # This function appends data to the end of the file, creating it if it doesn't exist
    def append_to_file(path, data):
        with open(path, 'at') as f:
            f.write(data + '\n')
            f.close()

    # Delete file contents
    def delete_file_contents(path):
        with open(path, 'wt') as f:
            f.write('')
            f.close()

    # Read a file and convert each line to a set of items
    def file_to_set(file_name):
        results = set()
        with open(file_name, 'rt') as f:
            for line in f:
                results.add(line.replace('\n', ''))
            f.close()
        return results

    # Iterate through a set of items and add each to a file
    def set_to_file(links, file_name):
        with open(file_name, 'wt') as f:
            for link in sorted(links):
                f.write(link + '\n')
            f.close()