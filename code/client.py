#client.py
import socket
import os
import time
from parser import Parser
import file_stats as s

"""
site: https://gopher.floodgap.com/gopher/gw?gopher://comp3310.ddns.net:70/1
Host: comp3310.ddns.net
Port: 70
"""

"""A client for interacting with a Gopher server."""
class GopherClient:
  

    stats_inst = None # Class level singleton instance

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None
        self.parser = None
        self.visited = set()
        if not GopherClient.stats_inst:
            GopherClient.stats_inst = s.FileStats()
        self.stats = GopherClient.stats_inst

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_host, self.server_port))
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("Timestamp:", timestamp)
    
    def close(self):
        if self.socket:
            self.socket.close()
            print("Socket closed")
    
    def send_request(self, request):
        if self.socket:
            self.socket.sendall((request + "\r\n").encode())
            
    
    def receive_response(self, timeout):
        start_time = time.time()
        if self.socket:
            try:
                self.socket.settimeout(timeout)
                # Initialize an empty variable to store the response
                response = b""
                # Receive data in chunks until all data is received
                while True:
                    if time.time() - start_time > timeout:
                        raise TimeoutError("Response: (timeout)")
                    chunk = self.socket.recv(4096)
                    if not chunk:
                        break
                    response += chunk
                # Check if the response should be treated as text or binary
                if b'\x00' in response:  # If the null byte is present, treat it as binary
                    return response
                else:
                    return response.decode()  # Otherwise, treat it as text
            except Exception as e:
                print("Error receiving response:", e)
                return b"error"
                


    def save_path(self, selector):
        return os.path.join('downloads', os.path.basename(selector)[:100]) # Limit file names to 100 characters because thats what gpt 3.5 said
    

    def download_text_file(self, selector):
        """
        Downloads a text file from the Gopher server.

        Args:
            selector (str): The selector string for the file to be downloaded.

        Returns:
            None
        """
        try:
            self.connect()
            print("Sent request:", selector)
            self.send_request(selector)
            response = self.receive_response(2)
            print("Received response")
            print("Downloading text file...")

            with open(self.save_path(selector), 'w') as file:  # Open in text mode for text files
                file.write(response)
            print("Text file downloaded successfully")
            self.stats.add_simple_text_file(selector)
            self.stats.update_text_file_stats(response)

            print(f"File saved to: {self.save_path(selector)}")

        except Exception as e:
            print("Error:", e)
        finally:
            self.close()
            
    def download_binary_file(self, selector):
        """
        Downloads a binary file from the Gopher server.

        Args:
            selector (str): The selector string for the file to be downloaded.

        Returns:
            None
        """
        try:
            self.connect()
            self.send_request(selector)
            response = self.receive_response(2)
            print("Downloading binary file...")
            
            with open(self.save_path(selector), 'wb') as file:  # Open in binary mode for binary files
                file.write(response)  # Encode the string response to bytes
            print("Binary file downloaded successfully")
            self.stats.add_binary_file(selector)
            file_size = os.path.getsize(self.save_path(selector))
            self.stats.update_binary_file_stats(file_size)

            print(f"File saved to: {self.save_path(selector)}")
            
        except Exception as e:
            print("Error:", e)
        finally:
            self.close()
            
    def crawl(self, selector=""):
        """
        Crawls through the Gopher directories recursively.

        Args:
            selector (str, optional): The selector string for the directory to start crawling from. Defaults to "".

        Returns:
            None
        """
        self.initialise(selector)
        self.visited.add("")
        options = self.parser.parse_response()
        
        if options:
            for option in options:
                if option['type'] == '1':  # Directory
                    # Check if external server
                    if option['host'] != self.server_host:
                        status = self.check_status(option['host'], int(option['port']))
                        self.stats.add_external(option['host'], option['port'], status)
                        continue
                    # Check if external server is up
                    check = self.checkVisted(option['selector'], option['host'], option['port'])

                    if check == True: continue

                    self.visited.add(check)
                    
                    print("Crawling into directory:", option['name']) 
                    self.stats.increment_dirs()
                    self.crawl(option['selector'])
                    
                if option['type'] == '0':  # File or resource
                    print("Downloading text file:", option['name'])
                    download_client = GopherClient(option['host'], int(option['port']))
                    download_client.download_text_file(option['selector'])

                if option['type'] == '9': # Binary file
                    print("Downloading binary file:", option['name'])
                    download_client = GopherClient(option['host'], int(option['port']))
                    download_client.download_binary_file(option['selector'])

        else:
            self.stats.add_invalid_references(selector)          

        self.close()


       
    def run(self):
        """
        Runs the Gopher client, allowing user interaction.

        Returns:
            None
        """
        self.initialise("")
        options = self.parser.extract_paths()
        print("Select from the following options:")
        for option in options:
            print(option)

        while True:
            user_input = input("Enter your choice (or press 'q' to quit): ")
            if user_input:
                if user_input.lower() == 'q':
                    break  # Exit the loop if the user enters 'q'
                
                self.connect()
                self.send_request(user_input)
                response = self.receive_response(1)
                
                # Pass the client instance when initializing the Parser
                self.parser = Parser(response, self)
                print("Response:", response)
                
                if user_input.endswith('.txt'):
                    self.download_file(user_input)

    
    
    def checkVisted(self, selector, host, port):
        """
        Checks if a directory has been visited.

        Args:
            selector (str): The selector string for the directory.
            host (str): The hostname of the Gopher server.
            port (int): The port number of the Gopher server.

        Returns:
            str or bool: The identifier for the visited directory, or True if already visited.
        """
        id = host + str(port) + selector
        if id in self.visited:
            return True
        return id

        
    def initialise(self, selector):
        """
        Initializes the client and parser.

        Args:
            selector (str): The selector string for the initial request.

        Returns:
            None
        """
        self.connect()
        print("Request: ", selector)
        self.send_request(selector)
        response = self.receive_response(1)
        self.parser = Parser(response, self)
        print(response)
        
        
    def check_status(self, host, port):
        """
        Checks the status of an external server.

        Args:
            host (str): The hostname of the external server.
            port (int): The port number of the external server.

        Returns:
            bool: True if the server is external and accessible, False otherwise.
        """
        try:
            ext_client = GopherClient(host, port)
            ext_client.connect()
            ext_client.close()
            return True  # Server is external and accessible
        except ConnectionError:
            return False  # Server is down or not accessible

    
