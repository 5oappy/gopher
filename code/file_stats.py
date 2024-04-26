
import socket
import os
import shutil
terminal_size = shutil.get_terminal_size().columns

class FileStats:
    """
    A class for tracking statistics of files and directories in a Gopher server.

    Attributes:
        gopher_dirs (int): Number of Gopher directories on the server.
        simple_text_files (list): List of paths of simple text files.
        binary_files (list): List of paths of binary files.
        smallest_text_file_content (str): Contents of the smallest text file.
        largest_text_file_size (int): Size of the largest text file.
        smallest_binary_file_size (int): Size of the smallest binary file.
        largest_binary_file_size (int): Size of the largest binary file.
        unique_invalid_references (list): List of unique invalid references.
        external_servers (dict): Dictionary containing external servers and their status.

    Methods:
        add_binary_file(path): Adds a binary file to the list of binary files.
        add_simple_text_file(path): Adds a simple text file to the list of simple text files.
        increment_dirs(): Increments the count of Gopher directories.
        add_external(host, port, status): Adds an external server to the list of external servers.
        update_text_file_stats(content): Updates statistics for text files.
        update_binary_file_stats(file_size): Updates statistics for binary files.
        add_invalid_references(path): Adds an invalid reference to the list of unique invalid references.
        analyse_references(): Analyzes and prints statistics for file references.
    """
    def __init__(self):
        self.gopher_dirs = 0 
        self.simple_text_files = [] 
        self.binary_files = [] 
        self.smallest_text_file_content = None
        self.largest_text_file_size = float('-inf')
        self.smallest_binary_file_size = float('inf')
        self.largest_binary_file_size = float('-inf')
        self.unique_invalid_references = []
        self.external_servers = {}
    
    def add_binary_file(self, path):
        self.binary_files.append(path)
        
        
    def add_simple_text_file(self, path):
        if path not in self.simple_text_files:
            self.simple_text_files.append(path)
        
        
    def increment_dirs(self):
        self.gopher_dirs += 1
        
        
    def add_external(self, host, port, status):
        self.external_servers[host, port] = status
        

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

        print("#" * terminal_size)
        print("Stats: ", '\n')
        print("Number of gohper directories on the server:", self.gopher_dirs,'\n')
        
        print("Number of simple text files:", len(self.simple_text_files),"List of full paths:", '\n', self.simple_text_files,'\n')

        print("Contents of the smallest text file:", self.smallest_text_file_content, '\n')
        print("Size of the largest text file:", self.largest_text_file_size, '\n')

        print("Number of simple binary files:", len(self.binary_files),"List of full paths:", '\n',self.binary_files, '\n')

        print("Size of the smallest binary file:", self.smallest_binary_file_size,'\n')
        print("Size of the largest binary file:", self.largest_binary_file_size,'\n')
   
        
        print("Number of invalid references:", len(self.unique_invalid_references), '\n')

        print("List of external servers:", self.external_servers, '\n')

        print("#" * terminal_size)