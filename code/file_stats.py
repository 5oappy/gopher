
import socket
import os

class FileStats:
    def __init__(self):
        self.gopher_dirs = 0 #
        self.simple_text_files = [] #
        self.binary_files = [] #
        self.smallest_text_file_content = None
        self.largest_text_file_size = float('-inf')
        self.smallest_binary_file_size = float('inf')
        self.largest_binary_file_size = float('-inf')
        self.unique_invalid_references = []
        self.external_servers = {}
    
    def add_binary_file(self, path):
        self.binary_files.append(path)
        
        
    def add_simple_text_file(self, path):
        self.simple_text_files.append(path)
        
        
    def increment_dirs(self):
        self.gopher_dirs += 1
        
        
    def add_external(self, selector, status):
        self.external_servers[selector] = status
        

    def update_text_file_stats(self, content):
        if self.smallest_text_file_content is None or len(content) < len(self.smallest_text_file_content):
            self.smallest_text_file_content = content
        
        self.largest_text_file_size = max(self.largest_text_file_size, len(content))

    def update_binary_file_stats(self, file_size):
        self.largest_binary_file_size = max(self.largest_binary_file_size, file_size)
        self.smallest_binary_file_size = min(self.smallest_binary_file_size, file_size)
        
        

    def add_invalid_references(self, path):
        if path not in self.unique_invalid_references:
            self.unique_invalid_references.append(path)

    
    def analyse_references(self):
        print("Stats: ", '\n')
        print("Number of gohper directories on the server:", self.gopher_dirs)
        
        print("Number of simple text files:", len(self.simple_text_files),"List of full paths:", self.simple_text_files)
        print("Contents of the smallest text file:", self.smallest_text_file_content)
        print("Size of the largest text file:", self.largest_text_file_size)

        print("Number of simple binary files:", len(self.binary_files),"List of full paths:",self.binary_files)
        print("Size of the smallest binary file:", self.smallest_binary_file_size)
        print("Size of the largest binary file:", self.largest_binary_file_size)
   
        
        print("Number of invalid references:", len(self.unique_invalid_references))

        print("List of external servers:", self.external_servers)