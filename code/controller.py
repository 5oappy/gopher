#controller.py
from client import GopherClient

def run():

    client = GopherClient('comp3310.ddns.net', 70)
    client.run()
    
def scan_directory(self, directory):
    self.send_request(directory)
    response = self.receive_response()
    # Parse the response and follow links to other directories
    # Download text and binary files
    pass

def scan_directory(self, directory):
    self.send_request(directory)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("Timestamp:", timestamp)
    print("Client Request:", directory)
    response = self.receive_response()
    # Parse the response and follow links to other directories
    # Download text and binary files
    pass


    """
    high key have no clue where this should be yet
# Inside the run method after scanning directories and downloading files
print("Number of Gopher directories:", num_directories)
print("Number of text files:", num_text_files)
print("Text files:", text_file_list)
print("Number of binary files:", num_binary_files)
print("Binary files:", binary_file_list)
print("Smallest text file contents:", smallest_text_file_contents)
print("Size of largest text file:", largest_text_file_size)
print("Size of smallest binary file:", smallest_binary_file_size)
print("Size of largest binary file:", largest_binary_file_size)
print("Number of unique invalid references:", num_invalid_references)
print("External servers:", external_servers_status)
    """