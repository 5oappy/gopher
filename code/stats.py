
import socket
import os

class Stats:
    def __init__(self):
        self.gopher_dirs = 0
        self.simple_text_files = []
        self.binary_files = []
        self.smallest_text_file_content = None
        self.largest_text_file_size = float('-inf')
        self.smallest_binary_file_size = float('inf')
        self.largest_binary_file_size = float('-inf')
        self.unique_invalid_references = set()
        self.external_servers = {}




    def count_gopher_dirs(self, options):
        for option in options:
            if option['type'] == '1':
                self.gopher_dirs += 1

    def find_text_and_binary_files(self, selector):
            if selector.endswith('.txt'):
                self.simple_text_files.append(selector)
                return True
            else:
                self.binary_files.append(selector)
                return False

    

    def get_file_sizes(self):
        for file_path in self.simple_text_files + self.binary_files:
            file_size = os.path.getsize(file_path)
            if file_path.endswith('.txt'):
                if file_size > self.largest_text_file_size:
                    self.largest_text_file_size = file_size
                with open(file_path, 'r') as file:
                    content = file.read()
                    if self.smallest_text_file_content is None or len(content) < len(self.smallest_text_file_content):
                        self.smallest_text_file_content = content
            else:
                if file_size > self.largest_binary_file_size:
                    self.largest_binary_file_size = file_size
                if file_size < self.smallest_binary_file_size:
                    self.smallest_binary_file_size = file_size

    def check_invalid_references(self, options):
        for option in options:
            if option['type'] == 'error':
                self.unique_invalid_references.add(option['selector'])

    def check_external_servers(self, options):
        for option in options:
            host = option['host']
            port = option['port']
            if (host, port) not in self.external_servers:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(2)  # Timeout for connection attempt
                        s.connect((host, int(port)))
                    self.external_servers[(host, port)] = True  # Server is up
                except (socket.timeout, ConnectionRefusedError):
                    self.external_servers[(host, port)] = False  # Server is down

    def analyze_references(self, options):
        self.count_gopher_dirs(options)
        self.find_text_and_binary_files(options)
        self.get_file_sizes()
        self.check_invalid_references(options)
        self.check_external_servers(options)