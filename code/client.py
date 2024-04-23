#client.py
import socket
import time
from parser import Parser
"""
site: https://gopher.floodgap.com/gopher/gw?gopher://comp3310.ddns.net:70/1

Host is: comp3310.ddns.net
Port is 70
"""


class GopherClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None
        self.parser = None

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
            self.socket.sendall(request.encode())
            

    def receive_response(self):
        if self.socket:
            try:
                response = self.socket.recv(4096).decode()
                return response
            except socket.timeout:
                print("Response: (timeout)")
                return "empty"

            

    def scan_directory(self, directory):
        # Implement directory scanning logic here
        
        pass

    def download_file(self, file_path):
        # Implement file download logic here
        pass

    # def run(self):
    #     options = self.parser.extract_paths()
    #     print("Select from the following options:")
    #     for option in options:
    #         print(option)

    #     user_input = input("Enter your choice: ")
        
    #     if user_input:
    #         self.connect()
    #         self.send_request(user_input)
    #         response = self.receive_response()
    #         self.parser = Parser(response)
    #         print("Response:",response)

    def crawl(self, path="\r\n"):
        self.connect()
        print("Request: ",path)
        self.send_request(path)
        response = self.receive_response()
        # print("Response", response)
        self.parser = Parser(response)
        options = self.parser.parse_response()
        for option in options:
        # Print each option separately
            print("Option:", option)
            

        # for option in options:
        #     if option['type'] == '1':  # Directory
        #         print("Crawling into directory:", option['name'])
        #         self.crawl(option['selector'])
        #     elif option['type'] == '0':  # File or resource
        #         print("Downloading file:", option['name'])
        #         # Implement file download logic here

        # self.close()

        # do stuff
     
    def intialise(self):
        empty = "\r\n"
        self.send_request(empty)
        initial_response = self.receive_response()
        self.parser = Parser(initial_response)
        print(initial_response)
        
    
                
"""
empty = "\r\n"
self.send_request(empty)
initial_response = self.receive_response()
print("Initial Response:", initial_response)
"""