
import socket
import os

class Statistics:
    def __init__(self):
        self.gopher_dirs = 0 #
        self.simple_text_files = [] #
        self.binary_files = [] #
        self.smallest_text_file_content = None
        self.largest_text_file_size = float('-inf')
        self.smallest_binary_file_size = float('inf')
        self.largest_binary_file_size = float('-inf')
        self.unique_invalid_references = set()
        self.external_servers = {}
    
    def add_binary_file(self, path):
        self.binary_files.append(path)
        
        
    def add_simple_text_file(self, path):
        self.simple_text_files.append(path)
        
        
    def increment_dirs(self):
        self.gopher_dirs += 1
        
        
    def add_external(self, selector, status):
        self.external_servers[selector] = status
        
    
    def get_file_sizes(self):
        # Iterate through each file path in simple_text_files and binary_files
        for file_path in self.simple_text_files + self.binary_files:
            file_size = os.path.getsize(file_path)  # Get the size of the file

            if file_path.endswith('.txt'):  # If it's a text file
                # Update largest_text_file_size if the current file size is larger
                if file_size > self.largest_text_file_size:
                    self.largest_text_file_size = file_size
                
                # Open the text file and read its content
                with open(file_path, 'r') as file:
                    content = file.read()
                    # Update smallest_text_file_content if the current content is smaller
                    if self.smallest_text_file_content is None or len(content) < len(self.smallest_text_file_content):
                        self.smallest_text_file_content = content
            else:  # If it's a binary file
                # Update largest_binary_file_size if the current file size is larger
                if file_size > self.largest_binary_file_size:
                    self.largest_binary_fileZ
                if file_size < self.smallest_binary_file_size:
                    self.smallest_binary_file_size = file_size

        # Print the results
        print("Contents of the smallest text file:", self.smallest_text_file_content)
        print("Size of the largest text file:", self.largest_text_file_size)
        print("Size of the smallest binary file:", self.smallest_binary_file_size)
        print("Size of the largest binary file:", self.largest_binary_file_size)
        

    # def check_invalid_references(self, options):
    #     for option in options:
    #         if option['type'] == 'error':
    #             self.unique_invalid_references.add(option['selector'])

    
    def analyse_references(self):
        print("Stats: ", '\n')
        print("Number of gohper directories on the server:", self.gopher_dirs)
        
        print("Number of simple text files:", len(self.simple_text_files),"List of full paths:", self.simple_text_files)
        
        print("Number of simple binary files:", len(self.binary_files),"List of full paths:",self.binary_files)
        
        self.get_file_sizes()
        #self.check_invalid_references(options)
        print("List of external servers:", self.external_servers)